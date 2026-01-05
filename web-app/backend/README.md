# PyJHora Backend API

FastAPI backend service for Vedic Astrology calculations using PyJHora library.

## Setup

### 1. Install Dependencies

```bash
cd web-app/backend
pip install -r requirements.txt
```

### 2. Run Development Server

```bash
python main.py
```

Or with uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Access API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## API Endpoints

### Panchanga

#### Calculate Panchanga
```
POST /api/v1/panchanga/calculate
```

Request:
```json
{
  "date": "2024-10-05",
  "time": "12:00:00",
  "place": {
    "name": "Chennai",
    "latitude": 13.0827,
    "longitude": 80.2707,
    "timezone": 5.5
  },
  "ayanamsa": "LAHIRI"
}
```

Response includes:
- Tithi (with paksha and end time)
- Nakshatra (with pada, lord, end time)
- Yoga (with end time)
- Karana
- Vaara (weekday)
- Sunrise/Sunset/Moonrise/Moonset
- Rahu Kala, Yamaganda, Gulika timings
- Abhijit Muhurta

#### Get Planet Positions
```
POST /api/v1/panchanga/planets
```

Request: Same as panchanga calculate

Response includes:
- All planet positions (Sun to Ketu)
- Ascendant
- Longitude, Rasi, Nakshatra for each

## Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── app/
│   ├── api/               # API endpoints
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   └── panchanga.py
│   │       └── router.py
│   ├── models/            # Pydantic models
│   │   └── schemas.py
│   └── services/          # Business logic
│       └── panchanga_service.py
```

## Development

### Adding New Endpoints

1. Create endpoint file in `app/api/v1/endpoints/`
2. Add router to `app/api/v1/router.py`
3. Create service in `app/services/` if needed
4. Define request/response models in `app/models/schemas.py`

### Testing

Use the Swagger UI at `/docs` to test all endpoints interactively.

Or use curl:

```bash
curl -X POST "http://localhost:8000/api/v1/panchanga/calculate" \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2024-10-05",
    "time": "12:00:00",
    "place": {
      "name": "Chennai",
      "latitude": 13.0827,
      "longitude": 80.2707,
      "timezone": 5.5
    }
  }'
```

## Features Implemented

### ✅ **Panchanga Calculations (100% Complete)**
- Basic panchanga (Tithi, Nakshatra, Yoga, Karana, Vaara)
- Sunrise/Sunset, Moonrise/Moonset
- Rahu Kala, Yamaganda, Gulika
- Brahma Muhurta, Abhijit Muhurta, all 30 muhurthas
- Tamil calendar, Tamil yogam, Tamil jaamam
- Extended features: Thaarabalam, Chandrabalam, Chandrashtama, Nava Thaara
- Anandhaadhi yoga, Triguna, Amrita Gadiya, Varjyam
- Karaka Tithi, Karaka Yogam, Panchaka Rahitha
- Eclipse information (solar & lunar)
- Sankranti dates (solar ingress)
- Planet conjunctions, retrograde status, Graha Yudh
- Udhaya Lagna Muhurtha
- Lunar month, Ritu, Samvatsara, Day/Night length
- Gauri Choghadiya, Shubha Hora

### ✅ **Charts (100% Complete)**
- All 27 divisional charts (D-1 to D-144, D-150)
- Special lagnas, Upagrahas, Arudha Padas
- JyotiChart integration for rendering

### ✅ **Dhasa Systems (100% Complete)**
- All 47 dhasa systems (22 Graha, 22 Raasi, 3 Annual)

### ✅ **Yogas & Doshas (100% Complete)**
- 100+ yogas with categorization
- All 8 doshas

### ✅ **Strength Calculations (90% Complete)**
- Shadbala, Ashtakavarga, Bhava Bala

### ✅ **Marriage Compatibility (100% Complete)**
- North Indian (Ashta Koota)
- South Indian (10 Porutham)

## Notes

- The backend automatically adds PyJHora src directory to Python path
- All PyJHora calculation functions are wrapped in service classes
- Error handling returns proper HTTP status codes with descriptive messages
- CORS is enabled for frontend communication

## Production Deployment

See `docker-compose.yml` in parent directory for containerized deployment.

