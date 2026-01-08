"""
Consolidated API endpoint - Single call for all chart data
Reduces 12+ API calls to 1 for blazing fast performance
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import PanchangaRequest
from app.services.panchanga_service import PanchangaService
from app.services.chart_service import ChartService
from app.services.strength_service import StrengthService
from typing import Dict, Any
import asyncio
from concurrent.futures import ThreadPoolExecutor

router = APIRouter()

# Thread pool for parallel computation
executor = ThreadPoolExecutor(max_workers=4)


def _calculate_panchanga(request: PanchangaRequest) -> Dict[str, Any]:
    """Calculate basic panchanga"""
    return PanchangaService.calculate_panchanga(
        date_str=request.date,
        time_str=request.time,
        place_data=request.place.model_dump(),
        ayanamsa=request.ayanamsa or "LAHIRI"
    )


def _calculate_extended(request: PanchangaRequest) -> Dict[str, Any]:
    """Calculate extended panchanga"""
    return PanchangaService.get_extended_panchanga(
        date_str=request.date,
        time_str=request.time,
        place_data=request.place.model_dump(),
        ayanamsa=request.ayanamsa or "LAHIRI"
    )


def _calculate_rasi_chart(request: PanchangaRequest) -> Dict[str, Any]:
    """Calculate Rasi (D1) chart"""
    service = ChartService()
    birth_details = {
        "date": request.date,
        "time": request.time,
        "place": request.place.model_dump()
    }
    return service.get_rasi_chart(birth_details, ayanamsa=request.ayanamsa or "LAHIRI")


def _calculate_navamsa_chart(request: PanchangaRequest) -> Dict[str, Any]:
    """Calculate Navamsa (D9) chart"""
    service = ChartService()
    birth_details = {
        "date": request.date,
        "time": request.time,
        "place": request.place.model_dump()
    }
    return service.get_divisional_chart(birth_details, divisional_factor=9, ayanamsa=request.ayanamsa or "LAHIRI")


def _calculate_ashtakavarga(request: PanchangaRequest) -> Dict[str, Any]:
    """Calculate Ashtakavarga"""
    service = StrengthService()
    birth_details = {
        "date": request.date,
        "time": request.time,
        "place": request.place.model_dump()
    }
    return service.get_ashtakavarga(birth_details, ayanamsa=request.ayanamsa or "LAHIRI")


@router.post("/calculate-all", response_model=Dict[str, Any])
async def calculate_all(request: PanchangaRequest):
    """
    Consolidated endpoint - Returns ALL chart data in a single request.
    
    Combines:
    - Basic panchanga (tithi, nakshatra, yoga, karana)
    - Extended panchanga (Tamil, muhurtha, etc.)
    - Rasi chart (D1) with planets, special lagnas, upagrahas
    - Navamsa chart (D9)  
    - Ashtakavarga
    
    This reduces 12+ API calls to 1 for blazing fast performance.
    """
    try:
        loop = asyncio.get_event_loop()
        
        # Run all calculations in parallel using thread pool
        panchanga_task = loop.run_in_executor(executor, _calculate_panchanga, request)
        extended_task = loop.run_in_executor(executor, _calculate_extended, request)
        rasi_task = loop.run_in_executor(executor, _calculate_rasi_chart, request)
        navamsa_task = loop.run_in_executor(executor, _calculate_navamsa_chart, request)
        ashtakavarga_task = loop.run_in_executor(executor, _calculate_ashtakavarga, request)
        
        # Wait for all to complete
        panchanga, extended, rasi, navamsa, ashtakavarga = await asyncio.gather(
            panchanga_task, extended_task, rasi_task, navamsa_task, ashtakavarga_task
        )
        
        return {
            "panchanga": panchanga,
            "extended": extended,
            "charts": {
                "rasi": rasi,
                "navamsa": navamsa
            },
            "ashtakavarga": ashtakavarga
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")
