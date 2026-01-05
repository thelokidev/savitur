"""
AI Export API Endpoints
Generate compact formats for LLM consumption
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import json
import traceback

from app.services.ai_export_service import get_ai_export_service

router = APIRouter()


class PlaceDetails(BaseModel):
    name: str = "Unknown"
    latitude: float = 0.0
    longitude: float = 0.0
    timezone: float = 5.5


class BirthDetails(BaseModel):
    date: str  # YYYY-MM-DD
    time: str = "12:00:00"
    place: PlaceDetails
    ayanamsa: Optional[str] = "LAHIRI"


class AIExportRequest(BaseModel):
    birth_details: BirthDetails
    format: Optional[str] = "toon"  # toon, markdown, json
    sections: Optional[List[str]] = None


@router.post("/export")
async def export_horoscope(request: AIExportRequest) -> Dict[str, Any]:
    """
    Export horoscope data in compact format for LLM consumption.
    
    Formats:
    - toon: TOON (Token-Oriented Object Notation) - most compact
    - markdown: Readable markdown format
    - json: Minified JSON
    
    Sections (all included by default):
    - chart: Planet positions
    - divisional: Navamsa D9
    - panchanga: Tithi, Nakshatra, Yoga, Karana
    - dasha: Vimsottari Dasha periods
    - strength: Shadbala and Ashtakavarga
    - yogas: Active yogas
    - doshas: Active doshas
    - transits: Current transits
    """
    try:
        service = get_ai_export_service()
        birth_details = request.birth_details.model_dump()
        sections = request.sections or ['chart', 'divisional', 'panchanga', 'dasha', 'strength', 'yogas', 'doshas', 'transits']
        format_type = request.format or 'toon'
        
        if format_type == 'toon':
            output = service.generate_toon_format(birth_details, sections)
            return {
                'format': 'toon',
                'output': output,
                'chars': len(output),
                'tokens_est': len(output) // 4  # Rough estimate: ~4 chars per token
            }
        elif format_type == 'markdown':
            output = service.generate_markdown_format(birth_details, sections)
            return {
                'format': 'markdown',
                'output': output,
                'chars': len(output),
                'tokens_est': len(output) // 4
            }
        elif format_type == 'json':
            output = service.generate_json_minimal(birth_details, sections)
            output_str = json.dumps(output, separators=(',', ':'))
            return {
                'format': 'json',
                'output': output_str,
                'data': output,
                'chars': len(output_str),
                'tokens_est': len(output_str) // 4
            }
        else:
            return {'error': f'Unknown format: {format_type}'}
    
    except Exception as e:
        return {'error': f'Export failed: {str(e)}', 'trace': traceback.format_exc()}


@router.post("/toon")
async def export_toon(request: AIExportRequest) -> Dict[str, Any]:
    """Generate TOON format output"""
    request.format = 'toon'
    return await export_horoscope(request)


@router.post("/markdown")
async def export_markdown(request: AIExportRequest) -> Dict[str, Any]:
    """Generate Markdown format output"""
    request.format = 'markdown'
    return await export_horoscope(request)


@router.post("/json")
async def export_json(request: AIExportRequest) -> Dict[str, Any]:
    """Generate minified JSON format output"""
    request.format = 'json'
    return await export_horoscope(request)
