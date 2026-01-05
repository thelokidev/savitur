"""
Panchanga API endpoints
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import (
    PanchangaRequest, PanchangaResponse,
    ChartRequest, ChartResponse,
    ErrorResponse
)
from app.services.panchanga_service import PanchangaService
from typing import Dict, Any
import json
import time

_AGENT_DEBUG_LOG_PATH = r"o:\savitur\.cursor\debug.log"

def _agent_write_log(payload: Dict[str, Any]) -> None:
    try:
        payload.setdefault("timestamp", int(time.time() * 1000))
        with open(_AGENT_DEBUG_LOG_PATH, "a", encoding="utf-8") as log_file:
            log_file.write(json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n")
    except Exception:
        return

router = APIRouter()


@router.post("/calculate", response_model=Dict[str, Any])
async def calculate_panchanga(request: PanchangaRequest):
    """
    Calculate complete panchanga for given date, time and place
    
    Returns tithi, nakshatra, yoga, karana, sunrise, sunset, and special timings
    """
    try:
        result = PanchangaService.calculate_panchanga(
            date_str=request.date,
            time_str=request.time,
            place_data=request.place.model_dump(),
            ayanamsa=request.ayanamsa or "LAHIRI"
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")


@router.post("/planets", response_model=Dict[str, Any])
async def get_planet_positions(request: PanchangaRequest):
    """
    Get positions of all planets for given date, time and place

    Returns longitude, rasi, nakshatra for each planet
    """
    try:
        result = PanchangaService.get_planet_positions(
            date_str=request.date,
            time_str=request.time,
            place_data=request.place.model_dump(),
            ayanamsa=request.ayanamsa or "LAHIRI"
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")


@router.post("/muhurtha", response_model=Dict[str, Any])
async def get_additional_timings(request: PanchangaRequest):
    """
    Get additional auspicious and inauspicious timings
    
    Returns brahma muhurta, durmuhurta, nishita kala, vijaya muhurta, 
    godhuli muhurta, and all 30 muhurthas of the day
    """
    try:
        result = PanchangaService.get_additional_timings(
            date_str=request.date,
            time_str=request.time,
            place_data=request.place.model_dump(),
            ayanamsa=request.ayanamsa or "LAHIRI"
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")


@router.post("/extended", response_model=Dict[str, Any])
async def get_extended_panchanga(request: PanchangaRequest):
    """
    Get extended panchanga features including:
    - Tamil calendar (month, date, year)
    - Tamil yogam and jaamam
    - Anandhaadhi yoga, Triguna
    - Amrita Gadiya, Varjyam
    - Thaarabalam, Chandrabalam, Chandrashtama
    - Nava Thaara, Special Thaara
    - Karaka Tithi, Karaka Yogam
    - Panchaka Rahitha, Vivaha Chakra Palan
    - Lunar month, Ritu (season), Samvatsara
    - Midday, Midnight, Day/Night length
    - Gauri Choghadiya, Shubha Hora
    """
    try:
        # region agent log
        place_payload = request.place.model_dump() if request.place else {}
        _agent_write_log({
            "sessionId": "debug-session",
            "runId": "pre-fix",
            "hypothesisId": "H1",
            "location": "panchanga.py:get_extended_panchanga:request",
            "message": "Incoming /panchanga/extended request payload (subset)",
            "data": {
                "date": request.date,
                "time": request.time,
                "ayanamsa": request.ayanamsa,
                "place": {
                    "name": place_payload.get("name"),
                    "latitude": place_payload.get("latitude"),
                    "longitude": place_payload.get("longitude"),
                    "timezone": place_payload.get("timezone"),
                },
            },
        })
        # endregion
        result = PanchangaService.get_extended_panchanga(
            date_str=request.date,
            time_str=request.time,
            place_data=request.place.model_dump(),
            ayanamsa=request.ayanamsa or "LAHIRI"
        )
        # region agent log
        _agent_write_log({
            "sessionId": "debug-session",
            "runId": "pre-fix",
            "hypothesisId": "H1",
            "location": "panchanga.py:get_extended_panchanga:response",
            "message": "Outgoing /panchanga/extended response (subset)",
            "data": {
                "extended_features_subset": {
                    "samvatsara": (result.get("extended_features") or {}).get("samvatsara") if isinstance(result, dict) else None,
                    "lunar_month": (result.get("extended_features") or {}).get("lunar_month") if isinstance(result, dict) else None,
                    "gauri_choghadiya": (result.get("extended_features") or {}).get("gauri_choghadiya") if isinstance(result, dict) else None,
                    "mahakala_hora": (result.get("extended_features") or {}).get("mahakala_hora") if isinstance(result, dict) else None,
                    "kaala_lord": (result.get("extended_features") or {}).get("kaala_lord") if isinstance(result, dict) else None,
                }
            },
        })
        # endregion
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")


@router.post("/eclipses", response_model=Dict[str, Any])
async def get_eclipse_info(request: PanchangaRequest):
    """
    Get solar and lunar eclipse information
    
    Returns:
    - Is there a solar eclipse today
    - Next solar eclipse date
    - Next lunar eclipse date
    """
    try:
        result = PanchangaService.get_eclipse_info(
            date_str=request.date,
            time_str=request.time,
            place_data=request.place.model_dump(),
            ayanamsa=request.ayanamsa or "LAHIRI"
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")


@router.post("/sankranti", response_model=Dict[str, Any])
async def get_sankranti_dates(request: PanchangaRequest):
    """
    Get previous and next sankranti (solar ingress) dates
    
    Sankranti is when Sun enters a new rasi (zodiac sign)
    """
    try:
        result = PanchangaService.get_sankranti_dates(
            date_str=request.date,
            time_str=request.time,
            place_data=request.place.model_dump(),
            ayanamsa=request.ayanamsa or "LAHIRI"
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")


@router.post("/conjunctions", response_model=Dict[str, Any])
async def get_planet_conjunctions(
    request: PanchangaRequest,
    planet1: int = 0,
    planet2: int = 1
):
    """
    Get next and previous conjunction dates between two planets
    
    Planet indices: 0=Sun, 1=Moon, 2=Mars, 3=Mercury, 4=Jupiter, 5=Venus, 6=Saturn, 7=Rahu, 8=Ketu
    """
    try:
        result = PanchangaService.get_planet_conjunctions(
            date_str=request.date,
            time_str=request.time,
            place_data=request.place.model_dump(),
            planet1_index=planet1,
            planet2_index=planet2,
            ayanamsa=request.ayanamsa or "LAHIRI"
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")


@router.post("/retrograde", response_model=Dict[str, Any])
async def get_retrograde_info(request: PanchangaRequest):
    """
    Get retrograde information for all planets
    
    Returns:
    - Which planets are currently retrograde
    - Planet speed information
    - Graha Yudh (planetary war) status
    """
    try:
        result = PanchangaService.get_planet_retrograde_info(
            date_str=request.date,
            time_str=request.time,
            place_data=request.place.model_dump(),
            ayanamsa=request.ayanamsa or "LAHIRI"
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")


@router.post("/udhaya-lagna", response_model=Dict[str, Any])
async def get_udhaya_lagna(request: PanchangaRequest):
    """
    Get Udhaya Lagna Muhurtha timings
    
    Udhaya Lagna is the rising sign at sunrise - an auspicious timing
    """
    try:
        result = PanchangaService.get_udhaya_lagna_muhurtha(
            date_str=request.date,
            time_str=request.time,
            place_data=request.place.model_dump(),
            ayanamsa=request.ayanamsa or "LAHIRI"
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")