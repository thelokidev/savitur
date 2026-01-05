import pytest
from app.services.strength_service import StrengthService

# Sample birth details for testing
birth_details = {
    "date": "1990-01-01",
    "time": "12:00:00",
    "place": {
        "name": "Chennai",
        "latitude": 13.0827,
        "longitude": 80.2707,
        "timezone": 5.5
    }
}

strength_service = StrengthService()

def test_get_vimsopaka_bala():
    data = strength_service.get_vimsopaka_bala(birth_details, "LAHIRI")
    assert "shadvarga" in data
    assert "dhasavarga" in data
    assert "Sun" in data["dhasavarga"]
    # JHora-style charts include nodes for Vimsopaka/Vaiseshikamsa; backend should expose them too.
    assert "Rahu" in data["dhasavarga"]
    assert "Ketu" in data["dhasavarga"]

def test_get_pancha_vargeeya_bala():
    data = strength_service.get_pancha_vargeeya_bala(birth_details, "LAHIRI")
    assert "planets" in data
    assert "Sun" in data["planets"]

def test_get_dwadasa_vargeeya_bala():
    data = strength_service.get_dwadasa_vargeeya_bala(birth_details, "LAHIRI")
    assert "planets" in data
    assert "Sun" in data["planets"]

def test_get_harsha_bala():
    data = strength_service.get_harsha_bala(birth_details, "LAHIRI")
    assert "planets" in data
    assert "Sun" in data["planets"]

def test_get_ishta_kashta_phala():
    data = strength_service.get_ishta_kashta_phala(birth_details, "LAHIRI")
    assert "ishta_phala" in data
    assert "kashta_phala" in data
    assert "Sun" in data["ishta_phala"]
