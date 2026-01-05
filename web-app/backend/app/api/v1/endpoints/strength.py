"""
Strength (Bala) calculation endpoints
Shadbala, Ashtakavarga, Bhava Bala, etc.
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import StrengthRequest, ErrorResponse
from app.services.strength_service import StrengthService
from typing import Dict, Any

router = APIRouter()
strength_service = StrengthService()


@router.post("/shadbala", response_model=Dict[str, Any])
async def get_shadbala(request: StrengthRequest):
    """
    Calculate Shadbala (six-fold strength) for all planets:
    - Sthana Bala (positional strength)
    - Dig Bala (directional strength)
    - Kaala Bala (temporal strength)
    - Cheshta Bala (motional strength)
    - Naisargika Bala (natural strength)
    - Drik Bala (aspectual strength)
    """
    try:
        result = strength_service.get_shadbala(
            request.birth_details.dict(),
            request.ayanamsa
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ashtakavarga", response_model=Dict[str, Any])
async def get_ashtakavarga(request: StrengthRequest):
    """
    Calculate Ashtakavarga:
    - Bhinnashtakavarga (BAV) - individual planet contributions
    - Prastarashtakavarga (PAV) - spread of contributions
    - Sarvashtakavarga (SAV) - total of all planets
    """
    try:
        chart_type = "rasi" if request.calculation_type == "ashtakavarga" else "navamsa"
        result = strength_service.get_ashtakavarga(
            request.birth_details.dict(),
            request.ayanamsa,
            chart_type
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/shodhaya-pinda", response_model=Dict[str, Any])
async def get_shodhaya_pinda(request: StrengthRequest):
    """
    Calculate Shodhaya Pinda:
    - Rasi Pinda
    - Graha Pinda
    - Shodhaya Pinda (combined)
    """
    try:
        result = strength_service.get_shodhaya_pinda(
            request.birth_details.dict(),
            request.ayanamsa
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/bhava-bala", response_model=Dict[str, Any])
async def get_bhava_bala(request: StrengthRequest):
    """
    Calculate Bhava Bala (house strength):
    - Bhava Adhipathi Bala
    - Bhava Dig Bala
    - Bhava Drik Bala
    - Bhava Drishti Bala
    """
    try:
        result = strength_service.get_bhava_bala(
            request.birth_details.dict(),
            request.ayanamsa
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/vimsopaka-bala", response_model=Dict[str, Any])
async def get_vimsopaka_bala(request: StrengthRequest):
    """
    Calculate Vimsopaka Bala (all 4 variants):
    - Shadvarga (6 divisions)
    - Sapthavarga (7 divisions)
    - Dhasavarga (10 divisions)
    - Shodhasavarga (16 divisions)
    """
    try:
        result = strength_service.get_vimsopaka_bala(
            request.birth_details.dict(),
            request.ayanamsa
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/pancha-vargeeya-bala", response_model=Dict[str, Any])
async def get_pancha_vargeeya_bala(request: StrengthRequest):
    """
    Calculate Pancha Vargeeya Bala (five-source strength):
    - Kshetra Bala (sign placement)
    - Uchcha Bala (exaltation)
    - Hadda Bala (term strength)
    - Drekkana Bala (decanate)
    - Navamsa Bala (D-9 strength)
    """
    try:
        result = strength_service.get_pancha_vargeeya_bala(
            request.birth_details.dict(),
            request.ayanamsa
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/dwadasa-vargeeya-bala", response_model=Dict[str, Any])
async def get_dwadasa_vargeeya_bala(request: StrengthRequest):
    """
    Calculate Dwadasa Vargeeya Bala (twelve divisional chart strength):
    Returns strength score based on placement in first 12 divisional charts
    """
    try:
        result = strength_service.get_dwadasa_vargeeya_bala(
            request.birth_details.dict(),
            request.ayanamsa
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/harsha-bala", response_model=Dict[str, Any])
async def get_harsha_bala(request: StrengthRequest):
    """
    Calculate Harsha Bala (positional happiness strength):
    Measures planetary strength based on house placement from ascendant
    """
    try:
        result = strength_service.get_harsha_bala(
            request.birth_details.dict(),
            request.ayanamsa
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ishta-kashta-phala", response_model=Dict[str, Any])
async def get_ishta_kashta_phala(request: StrengthRequest):
    """
    Calculate Ishta Phala and Kashta Phala:
    - Ishta Phala: Auspicious results potential
    - Kashta Phala: Inauspicious results (60 - Ishta Phala)
    """
    try:
        result = strength_service.get_ishta_kashta_phala(
            request.birth_details.dict(),
            request.ayanamsa
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/all", response_model=Dict[str, Any])
async def get_all_strengths(request: StrengthRequest):
    """
    Calculate all 7 strength metrics in one call:
    - Shadbala (six-fold planetary strength)
    - Bhava Bala (house strength)
    - Vimsopaka Bala (divisional strength)
    - Pancha Vargeeya Bala (five-source strength)
    - Dwadhasa Vargeeya Bala (12 divisional chart strength)
    - Harsha Bala (positional happiness)
    - Ishta/Kashta Phala (auspicious/inauspicious results)
    """
    try:
        birth_dict = request.birth_details.dict()
        ayanamsa = request.ayanamsa
        
        shadbala = strength_service.get_shadbala(birth_dict, ayanamsa)
        bhava_bala = strength_service.get_bhava_bala(birth_dict, ayanamsa)
        vimsopaka = strength_service.get_vimsopaka_bala(birth_dict, ayanamsa)
        pancha_vargeeya = strength_service.get_pancha_vargeeya_bala(birth_dict, ayanamsa)
        dwadhasa_vargeeya = strength_service.get_dwadasa_vargeeya_bala(birth_dict, ayanamsa)
        harsha_bala = strength_service.get_harsha_bala(birth_dict, ayanamsa)
        ishta_kashta = strength_service.get_ishta_kashta_phala(birth_dict, ayanamsa)
        
        return {
            'birth_date': birth_dict['date'],
            'birth_time': birth_dict['time'],
            'shadbala': shadbala,
            'bhava_bala': bhava_bala,
            'vimsopaka_bala': vimsopaka,
            'pancha_vargeeya_bala': pancha_vargeeya,
            'dwadhasa_vargeeya_bala': dwadhasa_vargeeya,
            'harsha_bala': harsha_bala,
            'ishta_kashta_phala': ishta_kashta
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))