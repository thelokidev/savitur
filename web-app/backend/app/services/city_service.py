"""
City search and lookup service - OPTIMIZED VERSION
Uses in-memory indexing with binary search for fast autocomplete
Loads ~193k cities (31k US + 162k World) into memory on startup
"""
import sys
import os
import csv
import bisect
import time
from typing import List, Dict, Any, Optional, Tuple
from functools import lru_cache

# Add PyJHora to path
PYJHORA_PATH = os.path.join(os.path.dirname(__file__), '../../../../PyJHora/src')
sys.path.insert(0, PYJHORA_PATH)

from jhora import const

# Timezone name to offset mapping (common US timezones)
TZ_OFFSETS = {
    'America/New_York': -5, 'America/Chicago': -6, 'America/Denver': -7,
    'America/Los_Angeles': -8, 'America/Phoenix': -7, 'America/Anchorage': -9,
    'America/Honolulu': -10, 'America/Detroit': -5, 'America/Indianapolis': -5,
    'America/Boise': -7, 'America/Juneau': -9, 'America/Adak': -10,
    'America/Puerto_Rico': -4, 'Pacific/Guam': 10, 'Pacific/Samoa': -11,
}


class CityService:
    """Optimized city search service with in-memory binary search indexing"""
    
    _initialized = False
    _cities_data: List[Dict[str, Any]] = []  # All city details
    _usa_index: List[Tuple[str, int]] = []  # (lowercase_name, data_index) for USA
    _world_index: List[Tuple[str, int]] = []  # (lowercase_name, data_index) for World
    _name_to_index: Dict[str, int] = {}  # O(1) lookup by exact name
    _load_time_ms: float = 0
    
    # File paths
    US_CITIES_FILE = os.path.join(PYJHORA_PATH, 'jhora/data/uscities.csv')
    WORLD_CITIES_FILE = os.path.join(PYJHORA_PATH, 'jhora/data/world_cities_with_tz.csv')
    
    @classmethod
    def _get_tz_offset(cls, tz_name: str) -> float:
        """Get timezone offset from timezone name"""
        return TZ_OFFSETS.get(tz_name, -5.0)  # Default to EST
    
    @classmethod
    def initialize(cls):
        """Load all cities into memory - called once on startup"""
        if cls._initialized:
            return
        
        start_time = time.time()
        
        # Clear any existing data
        cls._cities_data = []
        cls._usa_index = []
        cls._world_index = []
        cls._name_to_index = {}
        
        usa_names_set = set()  # Track US cities to avoid duplicates
        
        # 1. Load US cities FIRST (higher priority, cleaner format)
        try:
            with open(cls.US_CITIES_FILE, encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) < 5:
                        continue
                    
                    name = row[1].strip()  # "New York, NY"
                    name_lower = name.lower()
                    
                    city = {
                        "country": "United States",
                        "name": name,
                        "latitude": round(float(row[2]), 4),
                        "longitude": round(float(row[3]), 4),
                        "timezone_name": row[4],
                        "timezone": cls._get_tz_offset(row[4]),
                        "is_usa": True
                    }
                    
                    idx = len(cls._cities_data)
                    cls._cities_data.append(city)
                    cls._usa_index.append((name_lower, idx))
                    cls._name_to_index[name_lower] = idx
                    usa_names_set.add(name_lower)
                    
        except Exception as e:
            print(f"Warning: Could not load US cities: {e}")
        
        # 2. Load World cities (skip duplicates that exist in US file)
        try:
            with open(cls.WORLD_CITIES_FILE, encoding='ISO-8859-1') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) < 6:
                        continue
                    
                    name = row[1].strip()
                    name_lower = name.lower()
                    
                    # Skip if already in US cities
                    if name_lower in usa_names_set:
                        continue
                    
                    try:
                        city = {
                            "country": row[0],
                            "name": name,
                            "latitude": round(float(row[2]), 4),
                            "longitude": round(float(row[3]), 4),
                            "timezone_name": row[4],
                            "timezone": round(float(row[5]), 2),
                            "is_usa": False
                        }
                        
                        idx = len(cls._cities_data)
                        cls._cities_data.append(city)
                        cls._world_index.append((name_lower, idx))
                        cls._name_to_index[name_lower] = idx
                        
                    except (ValueError, IndexError):
                        continue  # Skip malformed rows
                        
        except Exception as e:
            print(f"Warning: Could not load World cities: {e}")
        
        # 3. Sort indices for binary search
        cls._usa_index.sort(key=lambda x: x[0])
        cls._world_index.sort(key=lambda x: x[0])
        
        cls._load_time_ms = (time.time() - start_time) * 1000
        cls._initialized = True
        
        print(f"✅ CityService initialized: {len(cls._cities_data):,} cities loaded in {cls._load_time_ms:.0f}ms")
        print(f"   └─ USA: {len(cls._usa_index):,} | World: {len(cls._world_index):,}")
    
    @classmethod
    def _binary_search_prefix(cls, index: List[Tuple[str, int]], prefix: str, limit: int) -> List[Dict]:
        """Binary search for prefix matches in sorted index"""
        if not prefix:
            return []
        
        prefix_lower = prefix.lower()
        
        # Find first match using binary search
        left = bisect.bisect_left(index, (prefix_lower,))
        
        results = []
        for i in range(left, min(left + limit * 3, len(index))):  # Scan ahead
            name, data_idx = index[i]
            if not name.startswith(prefix_lower):
                break
            results.append(cls._cities_data[data_idx])
            if len(results) >= limit:
                break
        
        return results
    
    @classmethod
    def autocomplete(cls, query: str, limit: int = 10) -> Dict[str, Any]:
        """
        Fast autocomplete with grouped results (USA / International)
        
        Returns:
            {
                "usa": [{"name": "New York, NY", ...}, ...],
                "international": [{"name": "New Delhi, India", ...}, ...],
                "total": 15,
                "query": "new"
            }
        """
        cls.initialize()
        
        if not query or len(query) < 1:
            return {"usa": [], "international": [], "total": 0, "query": query}
        
        # Search both indices
        usa_results = cls._binary_search_prefix(cls._usa_index, query, limit)
        world_results = cls._binary_search_prefix(cls._world_index, query, limit)
        
        return {
            "usa": usa_results[:limit],
            "international": world_results[:limit],
            "total": len(usa_results) + len(world_results),
            "query": query
        }
    
    @classmethod
    def search_cities(cls, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Legacy search method - returns flat list with USA first
        """
        result = cls.autocomplete(query, limit)
        return result["usa"] + result["international"]
    
    @classmethod
    def get_city_details(cls, city_name: str) -> Optional[Dict[str, Any]]:
        """O(1) lookup by exact city name"""
        cls.initialize()
        
        idx = cls._name_to_index.get(city_name.lower())
        if idx is not None:
            return cls._cities_data[idx].copy()
        return None
    
    @classmethod
    def get_location(cls, place_name: str) -> Optional[Dict[str, Any]]:
        """
        Get location info - tries local DB first, then falls back to PyJHora
        """
        # Try exact match first
        result = cls.get_city_details(place_name)
        if result:
            return {
                "name": result["name"],
                "latitude": result["latitude"],
                "longitude": result["longitude"],
                "timezone": result["timezone"]
            }
        
        # Try partial match
        results = cls.search_cities(place_name, limit=1)
        if results:
            r = results[0]
            return {
                "name": r["name"],
                "latitude": r["latitude"],
                "longitude": r["longitude"],
                "timezone": r["timezone"]
            }
        
        # Fallback to PyJHora's get_location (Google/OSM)
        try:
            from jhora import utils
            result = utils.get_location(place_name)
            if result and len(result) >= 4:
                return {
                    "name": result[0],
                    "latitude": result[1],
                    "longitude": result[2],
                    "timezone": result[3]
                }
        except Exception as e:
            print(f"Error in PyJHora fallback for {place_name}: {e}")
        
        return None
    
    @classmethod
    def get_stats(cls) -> Dict[str, Any]:
        """Get service statistics"""
        cls.initialize()
        return {
            "total_cities": len(cls._cities_data),
            "usa_cities": len(cls._usa_index),
            "world_cities": len(cls._world_index),
            "load_time_ms": cls._load_time_ms,
            "initialized": cls._initialized
        }


# Initialize on module load for faster first request
CityService.initialize()
