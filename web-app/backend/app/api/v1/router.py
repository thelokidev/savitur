"""
API v1 router
Comprehensive Vedic Astrology API with ALL features
"""
from fastapi import APIRouter
from app.api.v1.endpoints import (
    panchanga,
    charts,
    dhasa,
    yogas,
    strength,
    compatibility,
    jyotichart,
    cities,
    transit,
    ai_export,
    consolidated
)

api_router = APIRouter()

# Panchanga - Daily calculations
api_router.include_router(
    panchanga.router,
    prefix="/panchanga",
    tags=["Panchanga"]
)

# Charts - All divisional charts, lagnas, upagrahas, arudhas
api_router.include_router(
    charts.router,
    prefix="/charts",
    tags=["Charts"]
)

# Dhasa - All 47 dhasa systems
api_router.include_router(
    dhasa.router,
    prefix="/dhasa",
    tags=["Dhasa Systems"]
)

# Yogas & Doshas - 100+ yogas and 8 doshas
api_router.include_router(
    yogas.router,
    prefix="/yogas",
    tags=["Yogas & Doshas"]
)

# Strength - Shadbala, Ashtakavarga, Bhava Bala
api_router.include_router(
    strength.router,
    prefix="/strength",
    tags=["Strength Calculations"]
)

# Compatibility - Marriage matching
api_router.include_router(
    compatibility.router,
    prefix="/compatibility",
    tags=["Marriage Compatibility"]
)

# JyotiChart - Traditional chart rendering
api_router.include_router(
    jyotichart.router,
    prefix="/jyotichart",
    tags=["JyotiChart Rendering"]
)

# Cities - City search and lookup
api_router.include_router(
    cities.router,
    prefix="/cities",
    tags=["City Search"]
)

# Transit - Planetary transits (Gochar)
api_router.include_router(
    transit.router,
    prefix="/transit",
    tags=["Transits"]
)

# AI Export - Compact formats for LLM consumption
api_router.include_router(
    ai_export.router,
    prefix="/ai-export",
    tags=["AI Export"]
)

# Consolidated - Single endpoint for all chart data (FAST!)
api_router.include_router(
    consolidated.router,
    prefix="",
    tags=["Consolidated"]
)
