"""
JyotiChart API Endpoints

FastAPI endpoints for generating Vedic astrology charts using the JyotiChart library.
"""

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response
from pydantic import BaseModel, Field
from typing import Optional, List
import sys
from pathlib import Path

from app.services.jyotichart_integration import JyotiChartIntegration
from app.services.chart_service import ChartService

router = APIRouter()


class BirthDetails(BaseModel):
    """Birth details for chart calculation."""
    year: int = Field(..., description="Birth year")
    month: int = Field(..., description="Birth month (1-12)")
    day: int = Field(..., description="Birth day")
    hour: int = Field(..., description="Birth hour (0-23)")
    minute: int = Field(..., description="Birth minute (0-59)")
    second: int = Field(default=0, description="Birth second (0-59)")
    latitude: float = Field(..., description="Birth place latitude")
    longitude: float = Field(..., description="Birth place longitude")
    timezone: float = Field(..., description="Timezone offset from UTC")


class JyotiChartRequest(BaseModel):
    """Request model for JyotiChart generation."""
    birth_details: BirthDetails
    ayanamsa: str = Field(default="Lahiri", description="Ayanamsa system to use")
    chart_style: str = Field(default="north", description="Chart style: north, south, or east")
    chart_name: str = Field(default="D1", description="Chart name/division")
    person_name: Optional[str] = Field(default="Native", description="Person's name")
    show_aspects: bool = Field(default=False, description="Show planetary aspects")
    background_color: str = Field(default="#1a1a1a", description="Background color")
    line_color: str = Field(default="#ffd60a", description="Line color")
    sign_color: str = Field(default="#06ffa5", description="Sign/Ascendant color")


class JyotiChartResponse(BaseModel):
    """Response model for JyotiChart generation."""
    success: bool
    svg_content: Optional[str] = None
    error: Optional[str] = None
    chart_info: Optional[dict] = None


@router.post("/generate", response_model=JyotiChartResponse)
async def generate_jyoti_chart(request: JyotiChartRequest):
    """
    Generate a Vedic astrology chart using JyotiChart library.
    
    This endpoint:
    1. Calculates planetary positions using our chart service
    2. Converts data to JyotiChart format
    3. Generates SVG chart using JyotiChart library
    4. Returns SVG as string
    
    Args:
        request: JyotiChartRequest with birth details and chart preferences
        
    Returns:
        JyotiChartResponse with SVG content or error message
    """
    try:
        # Step 1: Calculate chart data using our existing service
        chart_service = ChartService()
        
        # Determine which chart to calculate based on chart_name
        if request.chart_name.upper() == 'D1':
            chart_data = chart_service.get_rasi_chart(
                request.birth_details.dict(),
                request.ayanamsa
            )
        elif request.chart_name.upper() == 'D9':
            chart_data = chart_service.get_navamsa_chart(
                request.birth_details.dict(),
                request.ayanamsa
            )
        else:
            # For other divisions, try to get divisional chart
            division_num = int(request.chart_name.upper().replace('D', ''))
            chart_data = chart_service.get_divisional_chart(
                request.birth_details.dict(),
                request.ayanamsa,
                division_num
            )
        
        # Step 2: Convert to JyotiChart format and generate
        jyoti_integration = JyotiChartIntegration()
        
        # Custom configuration
        custom_config = {
            'show_aspects': request.show_aspects,
            'background_color': request.background_color,
            'line_color': request.line_color,
            'sign_color': request.sign_color
        }
        
        success, svg_content, error = jyoti_integration.generate_chart_svg(
            chart_data,
            chart_style=request.chart_style,
            chart_name=request.chart_name,
            person_name=request.person_name or "Native",
            custom_config=custom_config
        )
        
        if success:
            return JyotiChartResponse(
                success=True,
                svg_content=svg_content,
                chart_info={
                    'chart_name': request.chart_name,
                    'chart_style': request.chart_style,
                    'person_name': request.person_name,
                    'ayanamsa': request.ayanamsa
                }
            )
        else:
            return JyotiChartResponse(
                success=False,
                error=error
            )
            
    except Exception as e:
        return JyotiChartResponse(
            success=False,
            error=f"Chart generation failed: {str(e)}"
        )


@router.post("/generate-svg", response_class=Response)
async def generate_jyoti_chart_svg(request: JyotiChartRequest):
    """
    Generate chart and return raw SVG (for direct embedding).
    
    Returns SVG with proper content-type header for direct browser rendering.
    """
    try:
        # Use the main generation endpoint logic
        result = await generate_jyoti_chart(request)
        
        if result.success and result.svg_content:
            return Response(
                content=result.svg_content,
                media_type="image/svg+xml",
                headers={
                    "Content-Disposition": f"inline; filename={request.chart_name}.svg"
                }
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=result.error or "Chart generation failed"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Chart generation failed: {str(e)}"
        )


@router.post("/generate-multiple")
async def generate_multiple_charts(
    birth_details: BirthDetails,
    ayanamsa: str = "Lahiri",
    chart_style: str = "north",
    divisions: List[str] = Query(default=["D1", "D9", "D10"])
):
    """
    Generate multiple divisional charts at once.
    
    Useful for generating a complete chart set (e.g., D1, D9, D10).
    
    Args:
        birth_details: Birth information
        ayanamsa: Ayanamsa system
        chart_style: Chart rendering style
        divisions: List of divisions to generate (e.g., ["D1", "D9", "D10"])
        
    Returns:
        Dictionary with chart_name as key and SVG content as value
    """
    try:
        chart_service = ChartService()
        jyoti_integration = JyotiChartIntegration()
        
        results = {}
        errors = {}
        
        for division in divisions:
            try:
                # Calculate chart data
                if division.upper() == 'D1':
                    chart_data = chart_service.get_rasi_chart(
                        birth_details.dict(),
                        ayanamsa
                    )
                elif division.upper() == 'D9':
                    chart_data = chart_service.get_navamsa_chart(
                        birth_details.dict(),
                        ayanamsa
                    )
                else:
                    division_num = int(division.upper().replace('D', ''))
                    chart_data = chart_service.get_divisional_chart(
                        birth_details.dict(),
                        ayanamsa,
                        division_num
                    )
                
                # Generate chart
                success, svg_content, error = jyoti_integration.generate_chart_svg(
                    chart_data,
                    chart_style=chart_style,
                    chart_name=division,
                    person_name="Native"
                )
                
                if success:
                    results[division] = svg_content
                else:
                    errors[division] = error
                    
            except Exception as e:
                errors[division] = str(e)
        
        return {
            "success": len(results) > 0,
            "charts": results,
            "errors": errors if errors else None,
            "total_generated": len(results),
            "total_requested": len(divisions)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Multiple chart generation failed: {str(e)}"
        )


@router.get("/supported-styles")
async def get_supported_styles():
    """Get list of supported chart styles."""
    jyoti_integration = JyotiChartIntegration()
    return {
        "styles": jyoti_integration.get_supported_chart_types(),
        "description": {
            "north": "North Indian style (diamond with triangular houses)",
            "south": "South Indian style (square grid)"
        }
    }


@router.get("/supported-divisions")
async def get_supported_divisions():
    """Get list of supported divisional charts."""
    jyoti_integration = JyotiChartIntegration()
    return {
        "divisions": jyoti_integration.get_supported_divisions(),
        "description": {
            "D1": "Rasi - Birth Chart",
            "D9": "Navamsa - Marriage & Dharma",
            "D10": "Dasamsa - Career & Status",
            "D12": "Dwadasamsa - Parents",
            "D16": "Shodasamsa - Vehicles & Happiness",
            "D20": "Vimsamsa - Spiritual Progress",
            "D24": "Chaturvimsamsa - Education",
            "D27": "Nakshatramsa - Strengths & Weaknesses",
            "D30": "Trimsamsa - Evils & Misfortunes",
            "D60": "Shashtiamsa - Past Life & Karma"
        }
    }


@router.get("/health")
async def health_check():
    """Health check endpoint for JyotiChart service."""
    try:
        # Try to import and initialize
        jyoti_integration = JyotiChartIntegration()
        return {
            "status": "healthy",
            "service": "jyotichart",
            "available": True
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "service": "jyotichart",
            "available": False,
            "error": str(e)
        }

