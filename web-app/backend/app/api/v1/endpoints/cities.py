"""
City search and lookup endpoints - OPTIMIZED VERSION
Provides fast autocomplete with grouped results (USA / International)
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any
from pydantic import BaseModel
from app.services.city_service import CityService

router = APIRouter()


class CityResult(BaseModel):
    country: str
    name: str
    latitude: float
    longitude: float
    timezone_name: str
    timezone: float
    is_usa: bool = False


class AutocompleteResponse(BaseModel):
    usa: List[Dict[str, Any]]
    international: List[Dict[str, Any]]
    total: int
    query: str


@router.get("/search", response_model=List[Dict[str, Any]])
async def search_cities(
    query: str = Query(..., min_length=2, description="Search query (minimum 2 characters)"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of results")
):
    """
    Search for cities by name (flat list, USA first)
    """
    try:
        results = CityService.search_cities(query, limit)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")


@router.get("/lookup/{city_name:path}", response_model=Dict[str, Any])
async def lookup_city(city_name: str):
    """
    Get detailed information for a specific city by exact name
    """
    try:
        result = CityService.get_city_details(city_name)
        if result is None:
            # Try partial match
            result = CityService.get_location(city_name)
        if result is None:
            raise HTTPException(status_code=404, detail=f"City '{city_name}' not found")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lookup error: {str(e)}")


@router.get("/autocomplete", response_model=AutocompleteResponse)
async def autocomplete_cities(
    q: str = Query(..., min_length=1, description="Search prefix"),
    limit: int = Query(10, ge=1, le=50, description="Maximum suggestions per group")
):
    """
    Fast autocomplete with grouped results (USA / International)
    
    Returns:
        - usa: List of US city matches
        - international: List of international city matches
        - total: Total number of matches found
        - query: Original search query
    """
    try:
        result = CityService.autocomplete(q, limit)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Autocomplete error: {str(e)}")


@router.get("/stats", response_model=Dict[str, Any])
async def get_city_stats():
    """
    Get city service statistics (total cities loaded, load time, etc.)
    """
    try:
        return CityService.get_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stats error: {str(e)}")
