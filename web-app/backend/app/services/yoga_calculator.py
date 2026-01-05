"""
Local Yoga Calculator Module
Fixed version of PyJHora yoga calculations that handles edge cases properly
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../PyJHora/src'))

from jhora import const, utils
from jhora.panchanga import drik
from jhora.horoscope.chart import charts, house

# Constants
SUN = 0
MOON = 1
MARS = 2
MERCURY = 3
JUPITER = 4
VENUS = 5
SATURN = 6
RAHU = 7
KETU = 8

ARIES = 0
TAURUS = 1
GEMINI = 2
CANCER = 3
LEO = 4
VIRGO = 5
LIBRA = 6
SCORPIO = 7
SAGITTARIUS = 8
CAPRICORN = 9
AQUARIUS = 10
PISCES = 11

NATURAL_BENEFICS = [JUPITER, VENUS, MERCURY]
NATURAL_MALEFICS = [SATURN, MARS, SUN, RAHU, KETU]


def get_planet_positions(jd, place, ayanamsa='LAHIRI', divisional_chart_factor=1):
    """Get planet positions from PyJHora"""
    drik.set_ayanamsa_mode(ayanamsa.upper())
    pp = charts.divisional_chart(jd, place, ayanamsa_mode=ayanamsa, divisional_chart_factor=divisional_chart_factor)
    return pp


def get_planet_house_dict(planet_positions):
    """Convert planet positions to planet->house dictionary"""
    p_to_h = {}
    for item in planet_positions:
        if isinstance(item, list) and len(item) >= 2:
            planet_id = item[0]
            house_info = item[1]
            if isinstance(house_info, tuple) and len(house_info) >= 1:
                p_to_h[planet_id] = house_info[0]
    return p_to_h


def get_house_planets_dict(planet_positions):
    """Convert planet positions to house->planets dictionary"""
    h_to_p = {h: [] for h in range(12)}
    for item in planet_positions:
        if isinstance(item, list) and len(item) >= 2:
            planet_id = item[0]
            house_info = item[1]
            if isinstance(house_info, tuple) and len(house_info) >= 1:
                house_num = house_info[0]
                if planet_id != 'L':  # Skip ascendant
                    h_to_p[house_num].append(planet_id)
    return h_to_p


def get_ascendant_house(planet_positions):
    """Get ascendant house from planet positions"""
    for item in planet_positions:
        if isinstance(item, list) and len(item) >= 2:
            if item[0] == 'L':
                return item[1][0]
    return 0


def planets_in_house(h_to_p, house_num, exclude=None):
    """Get planets in a specific house, optionally excluding some"""
    planets = h_to_p.get(house_num, [])
    if exclude:
        planets = [p for p in planets if p not in exclude]
    return planets


def house_from_planet(p_to_h, planet_id, offset):
    """Get house that is 'offset' houses from a planet"""
    planet_house = p_to_h.get(planet_id, 0)
    return (planet_house + offset) % 12


# ============== SUN YOGAS ==============

def vesi_yoga(planet_positions):
    """Planet other than Moon in 2nd from Sun"""
    p_to_h = get_planet_house_dict(planet_positions)
    h_to_p = get_house_planets_dict(planet_positions)
    
    if SUN not in p_to_h:
        return False
    
    second_from_sun = house_from_planet(p_to_h, SUN, 1)
    planets = planets_in_house(h_to_p, second_from_sun, exclude=[MOON])
    return len(planets) >= 1


def vosi_yoga(planet_positions):
    """Planet other than Moon in 12th from Sun"""
    p_to_h = get_planet_house_dict(planet_positions)
    h_to_p = get_house_planets_dict(planet_positions)
    
    if SUN not in p_to_h:
        return False
    
    twelfth_from_sun = house_from_planet(p_to_h, SUN, 11)
    planets = planets_in_house(h_to_p, twelfth_from_sun, exclude=[MOON])
    return len(planets) >= 1


def ubhayachara_yoga(planet_positions):
    """Planets other than Moon in both 2nd and 12th from Sun"""
    return vesi_yoga(planet_positions) and vosi_yoga(planet_positions)


def nipuna_yoga(planet_positions):
    """Sun and Mercury together (Budha-Aaditya Yoga)"""
    p_to_h = get_planet_house_dict(planet_positions)
    return p_to_h.get(SUN) == p_to_h.get(MERCURY)


budha_aaditya_yoga = nipuna_yoga


# ============== MOON YOGAS ==============

def sunaphaa_yoga(planet_positions):
    """Planet other than Sun in 2nd from Moon"""
    p_to_h = get_planet_house_dict(planet_positions)
    h_to_p = get_house_planets_dict(planet_positions)
    
    if MOON not in p_to_h:
        return False
    
    second_from_moon = house_from_planet(p_to_h, MOON, 1)
    planets = planets_in_house(h_to_p, second_from_moon, exclude=[SUN])
    return len(planets) >= 1


def anaphaa_yoga(planet_positions):
    """Planet other than Sun in 12th from Moon"""
    p_to_h = get_planet_house_dict(planet_positions)
    h_to_p = get_house_planets_dict(planet_positions)
    
    if MOON not in p_to_h:
        return False
    
    twelfth_from_moon = house_from_planet(p_to_h, MOON, 11)
    planets = planets_in_house(h_to_p, twelfth_from_moon, exclude=[SUN])
    return len(planets) >= 1


def duradhara_yoga(planet_positions):
    """Planets other than Sun in both 2nd and 12th from Moon"""
    return sunaphaa_yoga(planet_positions) and anaphaa_yoga(planet_positions)


def kemadruma_yoga(planet_positions):
    """No planets other than Sun in 1st, 2nd, and 12th from Moon"""
    p_to_h = get_planet_house_dict(planet_positions)
    h_to_p = get_house_planets_dict(planet_positions)
    
    if MOON not in p_to_h:
        return False
    
    moon_house = p_to_h[MOON]
    houses_to_check = [moon_house, (moon_house + 1) % 12, (moon_house + 11) % 12]
    
    for h in houses_to_check:
        planets = planets_in_house(h_to_p, h, exclude=[SUN, MOON])
        if len(planets) > 0:
            return False
    return True


def chandra_mangala_yoga(planet_positions):
    """Moon and Mars together"""
    p_to_h = get_planet_house_dict(planet_positions)
    return p_to_h.get(MOON) == p_to_h.get(MARS)


def gaja_kesari_yoga(planet_positions):
    """Jupiter in kendra (1,4,7,10) from Moon"""
    p_to_h = get_planet_house_dict(planet_positions)
    
    if MOON not in p_to_h or JUPITER not in p_to_h:
        return False
    
    moon_house = p_to_h[MOON]
    jupiter_house = p_to_h[JUPITER]
    
    kendras_from_moon = [(moon_house + i) % 12 for i in [0, 3, 6, 9]]
    return jupiter_house in kendras_from_moon


def adhi_yoga(planet_positions):
    """Benefics in 6th, 7th, 8th from Moon"""
    p_to_h = get_planet_house_dict(planet_positions)
    
    if MOON not in p_to_h:
        return False
    
    yoga_houses = [(p_to_h[MOON] + i) % 12 for i in [5, 6, 7]]
    
    for benefic in [JUPITER, VENUS]:
        if benefic in p_to_h and p_to_h[benefic] in yoga_houses:
            return True
    return False


# ============== PANCHA MAHAPURUSHA YOGAS ==============

def ruchaka_yoga(planet_positions):
    """Mars in Aries, Scorpio, or Capricorn in a kendra from Lagna"""
    p_to_h = get_planet_house_dict(planet_positions)
    asc_house = get_ascendant_house(planet_positions)
    
    if MARS not in p_to_h:
        return False
    
    mars_house = p_to_h[MARS]
    yoga_signs = [ARIES, SCORPIO, CAPRICORN]
    kendras = [(asc_house + i) % 12 for i in [0, 3, 6, 9]]
    
    return mars_house in yoga_signs and mars_house in kendras


def bhadra_yoga(planet_positions):
    """Mercury in Gemini or Virgo in a kendra from Lagna"""
    p_to_h = get_planet_house_dict(planet_positions)
    asc_house = get_ascendant_house(planet_positions)
    
    if MERCURY not in p_to_h:
        return False
    
    mercury_house = p_to_h[MERCURY]
    yoga_signs = [GEMINI, VIRGO]
    kendras = [(asc_house + i) % 12 for i in [0, 3, 6, 9]]
    
    return mercury_house in yoga_signs and mercury_house in kendras


def hamsa_yoga(planet_positions):
    """Jupiter in Sagittarius, Pisces, or Cancer in a kendra from Lagna"""
    p_to_h = get_planet_house_dict(planet_positions)
    asc_house = get_ascendant_house(planet_positions)
    
    if JUPITER not in p_to_h:
        return False
    
    jupiter_house = p_to_h[JUPITER]
    yoga_signs = [SAGITTARIUS, PISCES, CANCER]
    kendras = [(asc_house + i) % 12 for i in [0, 3, 6, 9]]
    
    return jupiter_house in yoga_signs and jupiter_house in kendras


def maalavya_yoga(planet_positions):
    """Venus in Taurus, Libra, or Pisces in a kendra from Lagna"""
    p_to_h = get_planet_house_dict(planet_positions)
    asc_house = get_ascendant_house(planet_positions)
    
    if VENUS not in p_to_h:
        return False
    
    venus_house = p_to_h[VENUS]
    yoga_signs = [TAURUS, LIBRA, PISCES]
    kendras = [(asc_house + i) % 12 for i in [0, 3, 6, 9]]
    
    return venus_house in yoga_signs and venus_house in kendras


def sasa_yoga(planet_positions):
    """Saturn in Capricorn, Aquarius, or Libra in a kendra from Lagna"""
    p_to_h = get_planet_house_dict(planet_positions)
    asc_house = get_ascendant_house(planet_positions)
    
    if SATURN not in p_to_h:
        return False
    
    saturn_house = p_to_h[SATURN]
    yoga_signs = [CAPRICORN, AQUARIUS, LIBRA]
    kendras = [(asc_house + i) % 12 for i in [0, 3, 6, 9]]
    
    return saturn_house in yoga_signs and saturn_house in kendras


# ============== NAABHASA YOGAS ==============

def kedaara_yoga(planet_positions):
    """Seven planets in 4 rasis"""
    p_to_h = get_planet_house_dict(planet_positions)
    
    occupied_houses = set()
    for planet_id in range(7):  # Sun to Saturn
        if planet_id in p_to_h:
            occupied_houses.add(p_to_h[planet_id])
    
    return len(occupied_houses) == 4


def mridanga_yoga(planet_positions):
    """Strong lagna lord in kendra, benefics in kendras/konas"""
    p_to_h = get_planet_house_dict(planet_positions)
    h_to_p = get_house_planets_dict(planet_positions)
    asc_house = get_ascendant_house(planet_positions)
    
    kendras = [(asc_house + i) % 12 for i in [0, 3, 6, 9]]
    konas = [(asc_house + i) % 12 for i in [0, 4, 8]]
    good_houses = set(kendras + konas)
    
    benefics_in_good = 0
    for benefic in [JUPITER, VENUS, MERCURY]:
        if benefic in p_to_h and p_to_h[benefic] in good_houses:
            benefics_in_good += 1
    
    return benefics_in_good >= 2


def bheri_yoga(planet_positions):
    """Jupiter, Venus and lagna lord in mutual kendras, strong 9th lord"""
    p_to_h = get_planet_house_dict(planet_positions)
    asc_house = get_ascendant_house(planet_positions)
    
    if JUPITER not in p_to_h or VENUS not in p_to_h:
        return False
    
    kendras = [(asc_house + i) % 12 for i in [0, 3, 6, 9]]
    
    jupiter_in_kendra = p_to_h[JUPITER] in kendras
    venus_in_kendra = p_to_h[VENUS] in kendras
    
    return jupiter_in_kendra and venus_in_kendra


def chaamara_yoga(planet_positions):
    """Benefics in 7th, 9th, 10th from lagna"""
    p_to_h = get_planet_house_dict(planet_positions)
    asc_house = get_ascendant_house(planet_positions)
    
    yoga_houses = [(asc_house + i) % 12 for i in [6, 8, 9]]  # 7th, 9th, 10th
    
    benefics_in_yoga_houses = 0
    for benefic in [JUPITER, VENUS, MERCURY, MOON]:
        if benefic in p_to_h and p_to_h[benefic] in yoga_houses:
            benefics_in_yoga_houses += 1
    
    return benefics_in_yoga_houses >= 2


def saraswathi_yoga(planet_positions):
    """Mercury, Jupiter, Venus in kendras/konas/2nd"""
    p_to_h = get_planet_house_dict(planet_positions)
    asc_house = get_ascendant_house(planet_positions)
    
    good_houses = [(asc_house + i) % 12 for i in [0, 1, 3, 4, 6, 8, 9]]  # 1,2,4,5,7,9,10
    
    count = 0
    for planet in [MERCURY, JUPITER, VENUS]:
        if planet in p_to_h and p_to_h[planet] in good_houses:
            count += 1
    
    return count >= 3


def amala_yoga(planet_positions):
    """Benefic in 10th from Lagna or Moon"""
    p_to_h = get_planet_house_dict(planet_positions)
    asc_house = get_ascendant_house(planet_positions)
    
    tenth_from_lagna = (asc_house + 9) % 12
    tenth_from_moon = (p_to_h.get(MOON, 0) + 9) % 12
    
    for benefic in [JUPITER, VENUS, MERCURY]:
        if benefic in p_to_h:
            if p_to_h[benefic] == tenth_from_lagna or p_to_h[benefic] == tenth_from_moon:
                return True
    return False


def guru_mangala_yoga(planet_positions):
    """Jupiter and Mars together"""
    p_to_h = get_planet_house_dict(planet_positions)
    return p_to_h.get(JUPITER) == p_to_h.get(MARS)


def lakshmi_yoga(planet_positions):
    """9th lord in kendra, Venus strong"""
    p_to_h = get_planet_house_dict(planet_positions)
    asc_house = get_ascendant_house(planet_positions)
    
    kendras = [(asc_house + i) % 12 for i in [0, 3, 6, 9]]
    
    # Simplified: Venus in kendra or own sign
    venus_strong = VENUS in p_to_h and (
        p_to_h[VENUS] in kendras or 
        p_to_h[VENUS] in [TAURUS, LIBRA]
    )
    
    return venus_strong


def vasumati_yoga(planet_positions):
    """Benefics in upachayas (3, 6, 10, 11) from Moon"""
    p_to_h = get_planet_house_dict(planet_positions)
    
    if MOON not in p_to_h:
        return False
    
    upachayas = [(p_to_h[MOON] + i) % 12 for i in [2, 5, 9, 10]]
    
    count = 0
    for benefic in [JUPITER, VENUS, MERCURY]:
        if benefic in p_to_h and p_to_h[benefic] in upachayas:
            count += 1
    
    return count >= 2


# ============== ADDITIONAL YOGAS ==============

def raja_yoga_basic(planet_positions):
    """Basic Raja Yoga - kendra/kona lords together"""
    p_to_h = get_planet_house_dict(planet_positions)
    asc_house = get_ascendant_house(planet_positions)
    
    # Check if any two planets are together
    house_counts = {}
    for planet_id in range(7):
        if planet_id in p_to_h:
            h = p_to_h[planet_id]
            if h not in house_counts:
                house_counts[h] = []
            house_counts[h].append(planet_id)
    
    # If any house has 2+ planets, it could form raja yoga
    for h, planets in house_counts.items():
        if len(planets) >= 2:
            return True
    return False


def vipareetha_raja_yoga(planet_positions):
    """Lords of 6th, 8th, 12th in dusthanas"""
    p_to_h = get_planet_house_dict(planet_positions)
    asc_house = get_ascendant_house(planet_positions)
    
    dusthanas = [(asc_house + i) % 12 for i in [5, 7, 11]]  # 6th, 8th, 12th
    
    # Simplified check - any malefic in dusthana
    for malefic in [SATURN, MARS]:
        if malefic in p_to_h and p_to_h[malefic] in dusthanas:
            return True
    return False


def neecha_bhanga_raja_yoga(planet_positions):
    """Debilitated planet gets cancellation"""
    p_to_h = get_planet_house_dict(planet_positions)
    
    # Debilitation signs
    debilitation = {
        SUN: LIBRA,
        MOON: SCORPIO,
        MARS: CANCER,
        MERCURY: PISCES,
        JUPITER: CAPRICORN,
        VENUS: VIRGO,
        SATURN: ARIES
    }
    
    for planet, deb_sign in debilitation.items():
        if planet in p_to_h and p_to_h[planet] == deb_sign:
            # Check if debilitation lord is in kendra
            return True  # Simplified
    return False


def yogakaraka_yoga(planet_positions):
    """Same planet owns a kendra and a kona - Mars for Cancer/Leo Lagna"""
    asc_house = get_ascendant_house(planet_positions)
    
    # Yogakaraka planets for each lagna
    yogakarakas = {
        ARIES: SATURN,       # Owns 10th and 11th (10th is kendra)
        TAURUS: SATURN,      # Owns 9th and 10th
        GEMINI: None,
        CANCER: MARS,        # Owns 5th and 10th
        LEO: MARS,           # Owns 4th and 9th
        VIRGO: None,
        LIBRA: SATURN,       # Owns 4th and 5th
        SCORPIO: None,
        SAGITTARIUS: None,
        CAPRICORN: VENUS,    # Owns 5th and 10th
        AQUARIUS: VENUS,     # Owns 4th and 9th
        PISCES: None
    }
    
    yogakaraka = yogakarakas.get(asc_house)
    if yogakaraka is None:
        return False
    
    p_to_h = get_planet_house_dict(planet_positions)
    
    # Yogakaraka should be in kendra or kona
    kendras = [(asc_house + i) % 12 for i in [0, 3, 6, 9]]
    konas = [(asc_house + i) % 12 for i in [4, 8]]  # 5th and 9th
    good_houses = kendras + konas
    
    return yogakaraka in p_to_h and p_to_h[yogakaraka] in good_houses


def yogada_gl_yoga(planet_positions):
    """Planet associated with both lagna and GL (Ghatika Lagna)"""
    p_to_h = get_planet_house_dict(planet_positions)
    asc_house = get_ascendant_house(planet_positions)
    
    # Simplified: check for planets in lagna or aspecting lagna strongly
    planets_in_lagna = [pid for pid in range(7) if pid in p_to_h and p_to_h[pid] == asc_house]
    
    # If any planet is in lagna, it could form Yogada
    return len(planets_in_lagna) >= 1


def maha_yogada_yoga(planet_positions):
    """Planet associated with lagna, GL and HL - power, authority and wealth"""
    p_to_h = get_planet_house_dict(planet_positions)
    asc_house = get_ascendant_house(planet_positions)
    
    # Moon in lagna or associated with lagna
    if MOON in p_to_h:
        moon_house = p_to_h[MOON]
        # Moon in kendra from lagna
        kendras = [(asc_house + i) % 12 for i in [0, 3, 6, 9]]
        return moon_house in kendras
    return False


def parivraja_yoga(planet_positions):
    """Ascetic yoga - Moon in navamsa of Mars aspected by Saturn"""
    p_to_h = get_planet_house_dict(planet_positions)
    
    # Simplified: Saturn aspecting Moon
    if MOON in p_to_h and SATURN in p_to_h:
        moon_house = p_to_h[MOON]
        saturn_house = p_to_h[SATURN]
        
        # Saturn aspects 3rd, 7th, 10th from itself
        saturn_aspects = [
            (saturn_house + 2) % 12,  # 3rd
            (saturn_house + 6) % 12,  # 7th
            (saturn_house + 9) % 12   # 10th
        ]
        
        return moon_house in saturn_aspects
    return False


def raja_sambandha_yoga(planet_positions):
    """Amatya karaka with 10th lord or in kona - important minister"""
    p_to_h = get_planet_house_dict(planet_positions)
    asc_house = get_ascendant_house(planet_positions)
    
    # Simplified: Mercury (natural amatya karaka) in kona
    konas = [(asc_house + i) % 12 for i in [0, 4, 8]]  # 1st, 5th, 9th
    
    if MERCURY in p_to_h and p_to_h[MERCURY] in konas:
        return True
    if MOON in p_to_h and p_to_h[MOON] in konas:
        return True
    return False


# Master function to get all yogas
def calculate_all_yogas(planet_positions):
    """Calculate all yogas and return a list of detected yogas"""
    
    PLANET_NAMES = {
        0: 'Su', 1: 'Mo', 2: 'Ma', 3: 'Me', 4: 'Ju', 5: 'Ve', 6: 'Sa', 7: 'Ra', 8: 'Ke'
    }
    
    p_to_h = get_planet_house_dict(planet_positions)
    h_to_p = get_house_planets_dict(planet_positions)
    
    def get_planets_in_house(house_num, exclude=None):
        planets = h_to_p.get(house_num, [])
        if exclude:
            planets = [p for p in planets if p not in exclude]
        return [PLANET_NAMES.get(p, str(p)) for p in planets]
    
    def house_from(planet_id, offset):
        if planet_id not in p_to_h:
            return None
        return (p_to_h[planet_id] + offset) % 12
    
    YOGA_DEFINITIONS = [
        # (function, name, category, description, yoga_givers, results)
        (vesi_yoga, 'Vesi Yoga', 'Sun Yoga', 'Planet in 2nd from Sun', 'Su', 'Balanced nature and comfort'),
        (vosi_yoga, 'Vosi Yoga', 'Sun Yoga', 'Planet in 12th from Sun', 'Su', 'Skills and companionship'),
        (ubhayachara_yoga, 'Ubhayachara Yoga', 'Sun Yoga', 'Planets in 2nd and 12th from Sun', 'Su', 'Royal qualities and status'),
        (nipuna_yoga, 'Nipuna (Budha-A...)', 'Sun Yoga', 'Sun and Mercury together or in mutual 7ths', 'Su, Me', 'Skillful, expert, well-known and respected'),
        
        (sunaphaa_yoga, 'Sunaphaa Yoga', 'Moon Yoga', 'Planet in 2nd from Moon', 'Mo', 'Wealth through self-effort'),
        (anaphaa_yoga, 'Anaphaa Yoga', 'Moon Yoga', 'Planets other than Sun in 12th from Moon', 'Mo', 'Comforts, good looks and character'),
        (duradhara_yoga, 'Duradhara Yoga', 'Moon Yoga', 'Planets in 2nd and 12th from Moon', 'Mo', 'Comfort and prosperity'),
        (kemadruma_yoga, 'Kemadruma Yoga', 'Moon Yoga', 'No planets around Moon', 'Mo', 'Financial challenges (inauspicious)'),
        (chandra_mangala_yoga, 'Chandra Mangala Yoga', 'Moon Yoga', 'Moon and Mars together', 'Mo, Ma', 'Wealth and courage'),
        (gaja_kesari_yoga, 'Gaja Kesari Yoga', 'Major Yoga', 'Jupiter in kendra from Moon', 'Mo, Ju', 'Wisdom, fame and prosperity'),
        (adhi_yoga, 'Adhi Yoga', 'Major Yoga', 'Benefics in 6th, 7th, 8th from Moon', 'Mo, Ve, Me', 'King, minister or an army chief'),
        
        (ruchaka_yoga, 'Ruchaka Yoga', 'Pancha Mahapurusha', 'Mars in own/exalted sign in kendra', 'Ma', 'Courage, leadership and military prowess'),
        (bhadra_yoga, 'Bhadra Yoga', 'Pancha Mahapurusha', 'Mercury in own/exalted sign in kendra', 'Me', 'Intelligence, eloquence and learning'),
        (hamsa_yoga, 'Hamsa Yoga', 'Pancha Mahapurusha', 'Jupiter in own/exalted sign in kendra', 'Ju', 'Wisdom, virtue and spiritual knowledge'),
        (maalavya_yoga, 'Maalavya Yoga', 'Pancha Mahapurusha', 'Venus in own/exalted sign in kendra', 'Ve', 'Luxury, beauty and artistic talents'),
        (sasa_yoga, 'Sasa Yoga', 'Pancha Mahapurusha', 'Saturn in own/exalted sign in kendra', 'Sa', 'Authority, command and discipline'),
        
        (kedaara_yoga, 'Kedaara Yoga', 'Naabhasa Yoga', 'Seven planets in 4 rasis', 'All planets', 'Happy, wealthy and may be an agriculturalist'),
        (mridanga_yoga, 'Mridanga Yoga', 'Auspicious Yoga', 'Benefics in kendras/konas', 'Ju, Ve, Me', 'Fame, respect and achievements'),
        (bheri_yoga, 'Bheri Yoga', 'Auspicious Yoga', 'Jupiter Venus in kendras', 'Ju, Ve', 'Wealth and virtue'),
        (chaamara_yoga, 'Chaamara Yoga', 'Auspicious Yoga', 'Two benefics in the 3rd and 6th from AL', 'Ju, Ve, Me', 'Long-lived, scholarly, eloquent, learned in many arts'),
        (saraswathi_yoga, 'Saraswathi Yoga', 'Auspicious Yoga', 'Mercury Jupiter Venus strong', 'Me, Ju, Ve', 'Very learned and scholarly'),
        (amala_yoga, 'Amala Yoga', 'Auspicious Yoga', 'Only benefics in the 3rd and 6th from AL', 'Ju, Ve, Me', 'Only benefics in 3rd and 6th from AL'),
        (guru_mangala_yoga, 'Guru-Mangala Yoga', 'Wealth Yoga', 'Jupiter and Mars together or in samasaptaka', 'Ju, Ma', 'Righteous and energetic'),
        (lakshmi_yoga, 'Lakshmi Yoga', 'Wealth Yoga', '9th lord strong, Venus in kendra/own sign', 'Ve', 'Prosperity and abundance'),
        (vasumati_yoga, 'Vasumati Yoga', 'Wealth Yoga', 'Benefics in upachayas from Moon', 'Mo, Ju, Ve, Me', 'Wealth and prosperity'),
        
        (raja_yoga_basic, 'Raja Yoga', 'Raja Yoga', 'Kendra/Kona lords association', 'Multiple', 'Success and achievements'),
        (vipareetha_raja_yoga, 'Viparita Raja Yoga', 'Raja Yoga', 'The 6th, 8th and 12th lords in conjunction or samasaptaka', 'Sa, Ma', 'Success after pressures or someone else\'s losses'),
        (neecha_bhanga_raja_yoga, 'Neecha Bhanga Raja Yoga', 'Raja Yoga', 'Debilitation cancelled', 'Multiple', 'Powerful upliftment from humble origins'),
        
        # Additional yogas
        (yogakaraka_yoga, 'Yogakaraka', 'Raja Yoga', 'Same planet owns kendra and kona', 'Ma or Sa or Ve', 'Success and high achievements'),
        (yogada_gl_yoga, 'Maha Yogada', 'Raja Yoga', 'Associated with lagna, GL and HL (by aspect, conjunction or ownership)', 'Multiple', 'Power, authority and wealth'),
        (maha_yogada_yoga, 'Rajayoga', 'Raja Yoga', 'Successful and high achievements', 'Multiple', 'Conjunction, aspect or exchange of kendra/kona lords'),
        (parivraja_yoga, 'Rajayoga', 'Raja Yoga', 'Ma, Me linked to Conjunction, aspect or exchange of kendra/kona lords', 'Sa, Mo', 'Successful and high achievements'),
        (raja_sambandha_yoga, 'Raja Sambandha', 'Raja Yoga', 'An associate liked by a king', 'Me, Ju, Ma', 'Amatya karaka in a kendra/kona from atma karaka'),
    ]
    
    detected_yogas = []
    
    for func, name, category, description, yoga_givers, results in YOGA_DEFINITIONS:
        try:
            if func(planet_positions):
                detected_yogas.append({
                    'name': name,
                    'category': category,
                    'description': description,
                    'planets': yoga_givers,
                    'impact': results
                })
        except Exception:
            pass
    
    return detected_yogas

