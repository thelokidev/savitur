"""
Marriage Compatibility endpoints
North Indian (Ashta Koota) and South Indian (10 Porutham) methods
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import MatchRequest, ErrorResponse
from app.services.compatibility_service import CompatibilityService
from typing import Dict, Any

router = APIRouter()
compatibility_service = CompatibilityService()


@router.post("/north-indian", response_model=Dict[str, Any])
async def get_north_indian_compatibility(request: MatchRequest):
    """
    Calculate North Indian compatibility (Ashta Koota - 8 factors, 36 points):
    1. Varna Koota (1 point) - Spiritual compatibility
    2. Vashya Koota (2 points) - Mutual attraction
    3. Tara Koota (3 points) - Birth star compatibility
    4. Yoni Koota (4 points) - Sexual compatibility
    5. Graha Maitri Koota (5 points) - Mental compatibility
    6. Gana Koota (6 points) - Temperament compatibility
    7. Rasi Koota (7 points) - Moon sign compatibility
    8. Nadi Koota (8 points) - Health and progeny (most important)
    
    Minimum 18 points required for compatibility
    """
    try:
        result = compatibility_service.get_north_indian_compatibility(
            request.boy.dict(),
            request.girl.dict(),
            request.ayanamsa
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/south-indian", response_model=Dict[str, Any])
async def get_south_indian_compatibility(request: MatchRequest):
    """
    Calculate South Indian compatibility (10 Porutham - Tamil method):
    1. Dina Porutham - Birth star compatibility
    2. Gana Porutham - Nature/character compatibility
    3. Yoni Porutham - Sexual compatibility
    4. Rasi Porutham - Moon sign compatibility
    5. Rasi Adhipati Porutham - Moon sign lord compatibility
    6. Vasya Porutham - Mutual attraction
    7. Rajju Porutham - Longevity compatibility
    8. Vedha Porutham - Affliction check
    9. Mahendra Porutham - Progeny and prosperity
    10. Stree Deergha Porutham - Prosperity for woman
    
    Minimum 6 poruthams required for compatibility
    """
    try:
        result = compatibility_service.get_south_indian_compatibility(
            request.boy.dict(),
            request.girl.dict(),
            request.ayanamsa
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/both-methods", response_model=Dict[str, Any])
async def get_both_compatibilities(request: MatchRequest):
    """
    Get both North and South Indian compatibility analysis
    """
    try:
        result = compatibility_service.get_both_compatibilities(
            request.boy.dict(),
            request.girl.dict(),
            request.ayanamsa
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


