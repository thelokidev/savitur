"""
Chart calculation endpoints
All divisional charts, special lagnas, upagrahas, arudhas
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import ChartRequest, ErrorResponse
from app.services.chart_service import ChartService
from typing import Dict, Any

router = APIRouter()
chart_service = ChartService()


@router.post("/rasi", response_model=Dict[str, Any])
async def get_rasi_chart(request: ChartRequest):
    """
    Get Rasi chart (D-1) with all planet positions
    """
    try:
        result = chart_service.get_rasi_chart(
            request.birth_details.dict(),
            request.ayanamsa
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/divisional/{varga_number}", response_model=Dict[str, Any])
async def get_divisional_chart(varga_number: int, request: ChartRequest):
    """
    Get any divisional chart (D-n)
    - D-1 to D-144 supported
    - Custom vargas up to D-300
    """
    try:
        if varga_number < 1 or varga_number > 300:
            raise HTTPException(status_code=400, detail="Varga number must be between 1 and 300")
        
        result = chart_service.get_divisional_chart(
            request.birth_details.dict(),
            varga_number,
            request.ayanamsa
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/all-divisional", response_model=Dict[str, Any])
async def get_all_divisional_charts(request: ChartRequest):
    """
    Get all standard divisional charts at once
    Returns D-1, D-2, D-3, D-4, D-5, D-6, D-7, D-8, D-9, D-10, D-11, D-12,
    D-16, D-20, D-24, D-27, D-30, D-40, D-45, D-60, D-81, D-108, D-144
    """
    try:
        result = chart_service.get_all_divisional_charts(
            request.birth_details.dict(),
            request.ayanamsa
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/special-lagnas", response_model=Dict[str, Any])
async def get_special_lagnas(request: ChartRequest):
    """
    Get all special lagnas:
    - Bhava Lagna
    - Hora Lagna
    - Ghati Lagna
    - Vighati Lagna
    - Pranapada Lagna
    - Indu Lagna
    - Sree Lagna
    """
    try:
        result = chart_service.get_special_lagnas(
            request.birth_details.dict(),
            request.ayanamsa
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upagrahas", response_model=Dict[str, Any])
async def get_upagrahas(request: ChartRequest):
    """
    Get all upagrahas (sub-planets):
    - Dhuma, Vyatipaata, Parivesha, Indrachapa, Upaketu
    - Kaala, Mrityu, Artha Praharaka, Yama Ghantaka
    - Gulika, Maandi
    """
    try:
        result = chart_service.get_upagrahas(
            request.birth_details.dict(),
            request.ayanamsa
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/arudha-padas", response_model=Dict[str, Any])
async def get_arudha_padas(request: ChartRequest):
    """
    Get all Arudha Padas (A1 to A12)
    """
    try:
        result = chart_service.get_arudha_padas(
            request.birth_details.dict(),
            request.ayanamsa
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


