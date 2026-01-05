"""
Transit API Endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

from app.services.transit_service import get_transit_service

router = APIRouter()



class PlaceDetails(BaseModel):
    name: str = "Unknown"
    latitude: float = 0.0
    longitude: float = 0.0
    timezone: float = 5.5


class BirthDetails(BaseModel):
    date: str  # YYYY-MM-DD
    time: str = "12:00:00"  # HH:MM:SS
    place: PlaceDetails
    ayanamsa: Optional[str] = "LAHIRI"


class TransitRequest(BaseModel):
    birth_details: BirthDetails
    transit_datetime: Optional[str] = None  # ISO datetime or YYYY-MM-DD HH:MM:SS
    reference: Optional[str] = "lagna"  # 'lagna' or 'moon'


@router.post("/current")
async def get_current_transit(request: TransitRequest) -> Dict[str, Any]:
    """
    Get current planetary transit positions.
    
    If transit_datetime is not provided, uses current time.
    """
    try:
        service = get_transit_service()
        result = service.get_current_transit(
            birth_details=request.birth_details.model_dump(),
            transit_datetime=request.transit_datetime
        )
        
        if 'error' in result:
            return result
        
        return result
    except Exception as e:
        return {"error": f"Transit calculation failed: {str(e)}"}


@router.post("/overlay")
async def get_transit_overlay(request: TransitRequest) -> Dict[str, Any]:
    """
    Get both natal and transit positions for side-by-side display.
    
    Returns natal planet positions and transit positions with house calculations
    from both Lagna and Moon references.
    """
    try:
        service = get_transit_service()
        result = service.get_transit_vs_natal(
            birth_details=request.birth_details.model_dump(),
            transit_datetime=request.transit_datetime
        )
        
        if 'error' in result:
            return result
        
        return result
    except Exception as e:
        return {"error": f"Transit overlay calculation failed: {str(e)}"}


@router.post("/entries")
async def get_planet_entries(request: TransitRequest) -> Dict[str, Any]:
    """
    Get upcoming sign entry dates for planets.
    
    Returns a list of upcoming sign changes sorted by date.
    """
    try:
        service = get_transit_service()
        result = service.get_planet_entry_dates(
            birth_details=request.birth_details.model_dump(),
            transit_datetime=request.transit_datetime
        )
        
        if 'error' in result:
            return result
        
        return result
    except Exception as e:
        return {"error": f"Planet entries calculation failed: {str(e)}"}
