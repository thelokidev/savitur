"""
Dhasa calculation endpoints
All 47 types of dhasa systems
"""
from fastapi import APIRouter, HTTPException, Query
from app.models.schemas import DhasaRequest, ErrorResponse
from app.services.dhasa_service import DhasaService
from typing import Dict, Any

router = APIRouter()
dhasa_service = DhasaService()


@router.post("/vimsottari", response_model=Dict[str, Any])
async def get_vimsottari_dhasa(request: DhasaRequest):
    """
    Calculate Vimsottari Dhasa (most popular)
    120-year cycle based on Moon's nakshatra
    """
    try:
        result = dhasa_service.get_vimsottari_dhasa(
            request.birth_details.dict(),
            request.include_antardhasa,
            request.ayanamsa,
            request.max_sub_level or 2,
            request.focus_mahadasha_index
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/graha/{dhasa_type}", response_model=Dict[str, Any])
async def get_graha_dhasa(dhasa_type: str, request: DhasaRequest):
    """
    Calculate any Graha/Nakshatra based dhasa:
    - vimsottari, ashtottari, yogini, shodasottari
    - dwadasottari, dwisapathi, panchottari, sataatbika
    - chathuraaseethi_sama, shastihayani, shattrimsa_sama
    - naisargika, tara, karaka, aayu
    """
    try:
        result = dhasa_service.get_any_graha_dhasa(
            request.birth_details.dict(),
            dhasa_type,
            request.include_antardhasa,
            request.ayanamsa,
            request.max_sub_level or 2,
            request.focus_mahadasha_index
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/raasi/{dhasa_type}", response_model=Dict[str, Any])
async def get_raasi_dhasa(dhasa_type: str, request: DhasaRequest):
    """
    Calculate any Raasi based dhasa:
    - narayana, kendradhi_rasi, sudasa, drig, nirayana
    - shoola, chara, lagnamsaka, padhanadhamsa, mandooka
    - sthira, tara_lagna, brahma, varnada, yogardha
    - navamsa, paryaaya, trikona, kalachakra, moola, chakra
    """
    try:
        result = dhasa_service.get_any_raasi_dhasa(
            request.birth_details.dict(),
            dhasa_type,
            request.include_antardhasa,
            request.ayanamsa,
            request.max_sub_level or 2
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/applicable", response_model=Dict[str, Any])
async def get_applicable_dhasas(request: DhasaRequest):
    """
    Get list of all applicable dhasa systems for the chart
    """
    try:
        result = dhasa_service.get_all_applicable_dhasas(
            request.birth_details.dict(),
            request.ayanamsa
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


