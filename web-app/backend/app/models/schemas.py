"""
Pydantic models for request/response validation
"""
from typing import Optional, List, Tuple, Dict, Any
from pydantic import BaseModel, Field, field_validator
from datetime import date, time


class PlaceModel(BaseModel):
    """Location details"""
    name: str = Field(..., description="Place name", example="Chennai")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude", example=13.0827)
    longitude: float = Field(..., ge=-180, le=180, description="Longitude", example=80.2707)
    timezone: float = Field(..., ge=-12, le=14, description="Timezone offset", example=5.5)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Chennai",
                "latitude": 13.0827,
                "longitude": 80.2707,
                "timezone": 5.5
            }
        }


class BirthDetailsModel(BaseModel):
    """Birth details for horoscope calculation"""
    name: Optional[str] = Field(None, description="Person's name", example="John Doe")
    date: str = Field(..., description="Birth date (YYYY-MM-DD)", example="1990-01-15")
    time: str = Field(..., description="Birth time (HH:MM:SS)", example="10:30:00")
    place: PlaceModel

    @field_validator('date')
    @classmethod
    def validate_date(cls, v: str) -> str:
        try:
            year, month, day = v.split('-')
            year_int = int(year)

            # Validate ephemeris range: 13000 BCE to 16800 CE
            if year_int < -13000 or year_int > 16800:
                raise ValueError(f'Year must be between 13000 BCE and 16800 CE, got {year_int}')

            return f"{year_int:04d}-{int(month):02d}-{int(day):02d}"
        except ValueError as e:
            if 'must be between' in str(e):
                raise e
            raise ValueError('Date must be in YYYY-MM-DD format')

    @field_validator('time')
    @classmethod
    def validate_time(cls, v: str) -> str:
        try:
            parts = v.split(':')
            if len(parts) != 3:
                raise ValueError
            h, m, s = parts
            return f"{int(h):02d}:{int(m):02d}:{int(s):02d}"
        except:
            raise ValueError('Time must be in HH:MM:SS format')


class PanchangaRequest(BaseModel):
    """Request for Panchanga calculations"""
    date: str = Field(..., description="Date (YYYY-MM-DD)")
    time: str = Field(default="12:00:00", description="Time (HH:MM:SS)")
    place: PlaceModel
    ayanamsa: Optional[str] = Field(default="LAHIRI", description="Ayanamsa mode")

    @field_validator('ayanamsa')
    @classmethod
    def normalize_ayanamsa(cls, v: Optional[str]) -> str:
        """Normalize ayanamsa to uppercase"""
        if v is None:
            return "LAHIRI"
        return v.upper()


class ChartRequest(BaseModel):
    """Request for chart calculations"""
    birth_details: BirthDetailsModel
    ayanamsa: Optional[str] = Field(default="LAHIRI", description="Ayanamsa mode")
    chart_style: Optional[str] = Field(default="south_indian", description="Chart style")
    include_uranus: Optional[bool] = Field(default=False, description="Include outer planets")

    @field_validator('ayanamsa')
    @classmethod
    def normalize_ayanamsa(cls, v: Optional[str]) -> str:
        """Normalize ayanamsa to uppercase"""
        if v is None:
            return "LAHIRI"
        return v.upper()


class DhasaRequest(BaseModel):
    """Request for Dhasa calculations"""
    birth_details: BirthDetailsModel
    dhasa_type: str = Field(..., description="Type of dhasa", example="vimsottari")
    ayanamsa: Optional[str] = Field(default="LAHIRI", description="Ayanamsa mode")
    include_antardhasa: Optional[bool] = Field(default=True, description="Include sub-periods")
    max_sub_level: Optional[int] = Field(
        default=2,
        ge=1,
        le=6,
        description="Maximum nested dhasa level (1=Mahadasa … 6=Deha)"
    )
    focus_mahadasha_index: Optional[int] = Field(
        default=None,
        description="If provided, only returns the tree for this specific Mahadasha index (0-8 for Vimsottari)"
    )


class MatchRequest(BaseModel):
    """Request for marriage compatibility"""
    boy: BirthDetailsModel
    girl: BirthDetailsModel
    compatibility_type: str = Field(default="north", description="north or south")
    ayanamsa: Optional[str] = Field(default="LAHIRI", description="Ayanamsa mode")


class YogaRequest(BaseModel):
    """Request for Yoga calculations"""
    birth_details: BirthDetailsModel
    ayanamsa: Optional[str] = Field(default="LAHIRI", description="Ayanamsa mode")
    chart_number: Optional[int] = Field(default=1, description="Divisional chart number")


class StrengthRequest(BaseModel):
    """Request for strength calculations"""
    birth_details: BirthDetailsModel
    calculation_type: Optional[str] = Field(default="all", description="Type: shadbala, ashtakavarga, or all")
    ayanamsa: Optional[str] = Field(default="LAHIRI", description="Ayanamsa mode")


# Response Models

class TithiResponse(BaseModel):
    """Tithi information"""
    number: int
    name: str
    paksha: str
    end_time: Optional[str] = None


class NakshatraResponse(BaseModel):
    """Nakshatra information"""
    number: int
    name: str
    pada: int
    lord: str
    end_time: Optional[str] = None


class YogaResponse(BaseModel):
    """Yoga information"""
    number: int
    name: str
    end_time: Optional[str] = None


class KaranaResponse(BaseModel):
    """Karana information"""
    number: int
    name: str
    lord: str


class PanchangaResponse(BaseModel):
    """Panchanga calculation response"""
    place: PlaceModel
    date: str
    time: str
    julian_day: float
    sunrise: str
    sunset: str
    moonrise: Optional[str] = None
    moonset: Optional[str] = None
    tithi: TithiResponse
    nakshatra: NakshatraResponse
    yoga: YogaResponse
    karana: KaranaResponse
    vaara: str
    rahu_kala: Dict[str, str]
    yamaganda: Dict[str, str]
    gulika: Dict[str, str]
    abhijit_muhurta: Optional[Dict[str, str]] = None
    ayanamsa_value: float


class PlanetPosition(BaseModel):
    """Planet position information"""
    name: str
    longitude: float
    rasi: int
    rasi_name: str
    degrees_in_rasi: float
    nakshatra: int
    nakshatra_name: str
    retrograde: bool = False


class ChartResponse(BaseModel):
    """Chart calculation response"""
    birth_details: BirthDetailsModel
    julian_day: float
    ayanamsa_value: float
    ascendant: PlanetPosition
    planets: List[PlanetPosition]
    houses: Dict[int, List[str]]
    chart_type: str


class DhasaPeriod(BaseModel):
    """Dhasa period information"""
    planet: str
    start_date: str
    end_date: str
    duration_years: float
    sub_periods: Optional[List['DhasaPeriod']] = None


class DhasaResponse(BaseModel):
    """Dhasa calculation response"""
    birth_details: BirthDetailsModel
    dhasa_type: str
    balance_at_birth: Dict[str, Any]
    periods: List[DhasaPeriod]


class YogaItem(BaseModel):
    """Individual yoga"""
    name: str
    description: str
    category: Optional[str] = None


class YogaListResponse(BaseModel):
    """Yoga calculations response"""
    birth_details: BirthDetailsModel
    total_yogas: int
    yogas: List[YogaItem]
    raja_yogas: List[YogaItem]
    doshas: List[YogaItem]


class CompatibilityScore(BaseModel):
    """Compatibility factor score"""
    name: str
    score: float
    max_score: float
    description: str
    compatible: bool


class MatchResponse(BaseModel):
    """Marriage compatibility response"""
    boy: BirthDetailsModel
    girl: BirthDetailsModel
    compatibility_type: str
    total_score: float
    max_score: float
    percentage: float
    compatible: bool
    factors: List[CompatibilityScore]
    recommendation: str


class ErrorResponse(BaseModel):
    """Error response"""
    error: str
    detail: Optional[str] = None
    code: Optional[int] = None

