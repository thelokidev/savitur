# PyJHora - Quick Start Guide

## ✓ Installation Complete!

PyJHora has been successfully set up at: **O:\vhora\PyJHora**

All dependencies are installed and the package is ready to use!

## Quick Commands

### 1. Activate Virtual Environment
```powershell
cd O:\vhora\PyJHora
.\venv\Scripts\Activate.ps1
```

### 2. Verify Installation
```powershell
python test_installation.py
```

### 3. Run Basic Examples
```powershell
python example_usage.py
```

## Launch GUI Applications

### Main Application (Comprehensive Charts)
```powershell
python -m jhora.ui.horo_chart_tabs
```
Features: Multiple tabs with Panchanga, Rasi/Divisional charts, Dhasa systems, Yogas, Doshas, Ashtakavarga, etc.

### Panchangam (One-Page View)
```powershell
python -m jhora.ui.panchangam
```
Features: Daily panchanga information

### Vedic Calendar
```powershell
python -m jhora.ui.vedic_calendar
```
Features: Monthly calendar with festivals and panchangam

### Marriage Compatibility
```powershell
python -m jhora.ui.match_ui
```
Features: Boy-Girl compatibility based on birth stars

### Vratha Finder
```powershell
python -m jhora.ui.vratha_finder
```
Features: Find special vratha dates

## Simple Python Usage

```python
from jhora.panchanga import drik
from jhora import utils

# Create a place
place = drik.Place('Chennai', 13.0827, 80.2707, +5.5)

# Define date and time
dob = (2024, 10, 5)  # Year, Month, Day  
tob = (12, 0, 0)     # Hour, Minute, Second

# Convert to Julian Day
jd = utils.julian_day_number(dob, tob)

# Calculate sunrise
sunrise = drik.sunrise(jd, place)
print(f"Sunrise: {sunrise[1]}")

# Calculate tithi
tithi_info = drik.tithi(jd, place)
print(f"Tithi: {tithi_info[0]}")

# Calculate nakshatra
nak_info = drik.nakshatra(jd, place)
print(f"Nakshatra: {nak_info[0]}")

# Get planet longitude
from jhora import const
sun_long = drik.sidereal_longitude(jd, const._SUN)
moon_long = drik.sidereal_longitude(jd, const._MOON)
print(f"Sun: {sun_long:.2f}°, Moon: {moon_long:.2f}°")
```

## Key Features Available

### Panchanga (Daily Almanac)
- Tithi, Nakshatra, Yoga, Karana, Vaara
- Sunrise, Sunset, Moonrise, Moonset
- Rahu Kala, Yamaganda, Gulika
- Abhijit Muhurta, Durmuhurtams

### Charts
- Rasi Chart (D-1) + all Divisional Charts (D-2 to D-300)
- Multiple styles: South Indian, North Indian, East Indian, Western
- Bhava Chart with 17 house systems
- Special Lagnas, Upagrahas, Arudhas

### Dhasa Systems (44 total)
- **Graha Dhasas**: Vimsottari, Ashtottari, Yogini, Shodasottari, etc.
- **Raasi Dhasas**: Narayana, Chara, Kalachakra, Brahma, etc.
- **Annual Dhasas**: Mudda, Patyayini, Varsha Vimsottari

### Strength Calculations
- Shadbala (Six-fold strength)
- Bhava Bala (House strength)
- Ashtakavarga (Sarvashtakavarga & Bhinnastakavarga)

### Yogas & Doshas
- 100+ Yogas (Raja, Dhana, Pancha Mahapurusha, etc.)
- 8 Doshas (Kala Sarpa, Manglik, Pitru, etc.)

### Marriage Compatibility
- North Indian: Ashta Koota (8 types)
- South Indian: Tamil Porutham (10 types)

### Languages
English, Tamil, Telugu, Hindi, Kannada, Malayalam

## Configuration

### Change Ayanamsa
Edit `src/jhora/const.py`:
```python
_DEFAULT_AYANAMSA_MODE = 'LAHIRI'  # or 'KP', 'RAMAN', etc.
```

Available ayanamsa modes:
- LAHIRI (default)
- KP
- RAMAN  
- KRISHNAMURTI
- YUKTESHWAR
- TRUE_CHITRA
- And 15+ more...

## Project Structure

```
PyJHora/
├── src/jhora/              # Main package
│   ├── panchanga/          # Daily panchanga calculations
│   ├── horoscope/          # Charts, dhasa, yogas, strength
│   ├── ui/                 # GUI applications  
│   ├── data/               # Data files
│   │   └── ephe/           # Swiss ephemeris data (required!)
│   └── lang/               # Language resources
├── venv/                   # Virtual environment
├── test_installation.py    # Installation verification
├── example_usage.py        # Usage examples
└── SETUP_INSTRUCTIONS.md   # Detailed documentation
```

## Troubleshooting

### Virtual environment not activating
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

### GUI not starting
- Ensure PyQt6 is installed: `pip install PyQt6`
- Check virtual environment is activated

### Import errors
```powershell
pip install -e .
```

### "No module named 'jhora'"
Make sure you're in the PyJHora directory and virtual environment is activated.

## Documentation

- **SETUP_INSTRUCTIONS.md**: Comprehensive setup guide
- **README.md**: Original package documentation
- **src/jhora/panchanga/README.md**: Panchanga module API
- **src/jhora/horoscope/README.md**: Horoscope module API

## Test Suite

Run comprehensive tests (6300+ tests):
```powershell
pytest src/jhora/tests/pvr_tests.py
```

## Support & Credits

- **GitHub**: https://github.com/naturalstupid/PyJHora
- **Author**: Inspired by Shri. P.V.R Narasimha Rao's book "Vedic Astrology - An Integrated Approach"
- **License**: AGPL-3.0

## Next Steps

1. ✓ Installation verified
2. ✓ Basic examples working
3. **Try the GUI**: `python -m jhora.ui.horo_chart_tabs`
4. **Explore features**: Use different tabs, right-click menus
5. **Read documentation**: Check README files
6. **Write your own scripts**: Use `example_usage.py` as template

---

**Enjoy exploring Vedic Astrology with PyJHora!** 🌟

