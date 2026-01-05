"""
Yoga and Dosha calculation endpoints
100+ Yogas and 8 types of Doshas
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import YogaRequest, ErrorResponse
from app.services.yoga_dosha_service import YogaDoshaService
from typing import Dict, Any

router = APIRouter()
yoga_dosha_service = YogaDoshaService()


@router.post("/all-yogas", response_model=Dict[str, Any])
async def get_all_yogas(request: YogaRequest, divisional_chart: int = 1):
    """
    Calculate all yogas present in the chart:
    - Pancha Mahapurusha Yogas (5)
    - Moon Yogas (Sunaphaa, Anaphaa, Duradhara, Kemadruma)
    - Sun Yogas (Vesi, Vosi, Ubhayachara)
    - Raja Yogas (various types)
    - Dhana Yogas (wealth yogas)
    - Other important yogas (Gaja Kesari, Adhi, etc.)
    
    Query Parameters:
    - divisional_chart: Divisional chart number (1-60), default is 1 (Rasi chart)
    """
    try:
        result = yoga_dosha_service.get_all_yogas(
            request.birth_details.dict(),
            request.ayanamsa,
            divisional_chart_factor=divisional_chart
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/all-doshas", response_model=Dict[str, Any])
async def get_all_doshas(request: YogaRequest):
    """
    Calculate all doshas (afflictions) in the chart:
    - Kala Sarpa Dosha
    - Manglik/Sevvay Dosha
    - Pitru Dosha
    - Guru Chandala Dosha
    - Ganda Moola Dosha
    - Kalathra Dosha
    - Ghata Dosha
    - Shrapit Dosha
    """
    try:
        result = yoga_dosha_service.get_all_doshas(
            request.birth_details.dict(),
            request.ayanamsa
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


