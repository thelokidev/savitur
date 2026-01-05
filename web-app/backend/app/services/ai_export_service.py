"""
AI Export Service - Generates compact formats for LLM consumption
TOON (Token-Oriented Object Notation) format for minimal context length

This service calls ALL existing backend API services to get comprehensive data
and compresses it into the TOON format.
"""
import sys
import os
from datetime import datetime
from typing import Optional, Dict, List, Any
import json

# Import all existing services
from app.services.chart_service import ChartService
from app.services.panchanga_service import PanchangaService
from app.services.dhasa_service import DhasaService
from app.services.strength_service import StrengthService
from app.services.yoga_dosha_service import YogaDoshaService
from app.services.transit_service import TransitService


class AIExportService:
    """Service for generating compact astrological data formats using all API services"""
    
    def __init__(self):
        self.chart_service = ChartService()
        self.panchanga_service = PanchangaService()
        self.dhasa_service = DhasaService()
        self.strength_service = StrengthService()
        self.yoga_service = YogaDoshaService()
        self.transit_service = TransitService()
    
    def _safe_str(self, val, default='') -> str:
        """Safely convert value to string"""
        if val is None:
            return default
        return str(val)
    
    def _format_degree(self, degrees_in_rasi) -> str:
        """Format degree value"""
        if degrees_in_rasi is None:
            return ''
        try:
            deg = float(degrees_in_rasi)
            d = int(deg)
            m = int((deg - d) * 60)
            return f"{d}°{m:02d}'"
        except:
            return str(degrees_in_rasi)
    
    def _get_all_api_data(self, birth_details: dict, ayanamsa: str = 'LAHIRI') -> dict:
        """Call ALL API services and collect comprehensive data"""
        data = {}
        
        # 1. Rasi Chart
        try:
            data['rasi_chart'] = self.chart_service.get_rasi_chart(birth_details, ayanamsa)
        except Exception as e:
            data['rasi_chart'] = {'error': str(e)}
        
        # 2. Key Divisional Charts (D9, D10)
        for div in [9, 10]:
            try:
                data[f'd{div}'] = self.chart_service.get_divisional_chart(birth_details, div, ayanamsa)
            except:
                pass
        
        # 3. Panchanga
        try:
            date_str = birth_details.get('date', '')
            time_str = birth_details.get('time', '12:00:00')
            place_data = birth_details.get('place', {})
            data['panchanga'] = self.panchanga_service.calculate_panchanga(date_str, time_str, place_data, ayanamsa)
        except Exception as e:
            data['panchanga'] = {'error': str(e)}
        
        # 4. Vimsottari Dasha
        try:
            data['vimsottari'] = self.dhasa_service.get_vimsottari_dhasa(
                birth_details, include_antardhasa=True, ayanamsa=ayanamsa, max_sub_levels=2
            )
        except Exception as e:
            data['vimsottari'] = {'error': str(e)}
        
        # 5. Shadbala
        try:
            data['shadbala'] = self.strength_service.get_shadbala(birth_details, ayanamsa)
        except Exception as e:
            data['shadbala'] = {'error': str(e)}
        
        # 6. Ashtakavarga
        try:
            data['ashtakavarga'] = self.strength_service.get_ashtakavarga(birth_details, ayanamsa)
        except Exception as e:
            data['ashtakavarga'] = {'error': str(e)}
        
        # 7. Yogas
        try:
            data['yogas'] = self.yoga_service.get_all_yogas(birth_details, ayanamsa)
        except Exception as e:
            data['yogas'] = {'error': str(e)}
        
        # 8. Doshas
        try:
            data['doshas'] = self.yoga_service.get_all_doshas(birth_details, ayanamsa)
        except Exception as e:
            data['doshas'] = {'error': str(e)}
        
        # 9. Current Transits
        try:
            data['transits'] = self.transit_service.get_transit_vs_natal(birth_details)
        except:
            pass
        
        return data
    
    def generate_toon_format(self, birth_details: dict, sections: List[str] = None) -> str:
        """Generate TOON (Token-Oriented Object Notation) format from full API data"""
        if sections is None:
            sections = ['chart', 'divisional', 'panchanga', 'dasha', 'strength', 'yogas', 'doshas', 'transits']
        
        ayanamsa = birth_details.get('ayanamsa', 'LAHIRI')
        
        # Get ALL API data
        api_data = self._get_all_api_data(birth_details, ayanamsa)
        
        lines = []
        
        # === BIRTH SECTION ===
        lines.append("birth:")
        lines.append(f"  date: {birth_details.get('date', '')}")
        lines.append(f"  time: {birth_details.get('time', '')[:5]}")
        lines.append(f"  location: {birth_details.get('place', {}).get('name', 'Unknown')}")
        lines.append(f"  ayanamsa: {ayanamsa}")
        
        # === RASI CHART SECTION ===
        if 'chart' in sections and api_data.get('rasi_chart'):
            chart = api_data['rasi_chart']
            if isinstance(chart, dict) and 'error' not in chart:
                
                # Ascendant
                if chart.get('ascendant'):
                    asc = chart['ascendant']
                    if isinstance(asc, dict):
                        lines.append("")
                        lines.append("ascendant:")
                        lines.append(f"  rasi: {asc.get('rasi_name', asc.get('rasi', ''))}")
                        lines.append(f"  degree: {self._format_degree(asc.get('degrees_in_rasi', asc.get('longitude', '')))}")
                        lines.append(f"  nakshatra: {asc.get('nakshatra_name', '')} pada {asc.get('nakshatra_pada', '')}")
                
                # Planets - TOON tabular format
                planets = chart.get('planets', [])
                if planets and isinstance(planets, list):
                    valid_planets = [p for p in planets if isinstance(p, dict)]
                    if valid_planets:
                        lines.append("")
                        lines.append(f"planets[{len(valid_planets)}]:")
                        
                        names = []
                        rasis = []
                        degrees = []
                        nakshatras = []
                        retros = []
                        
                        for p in valid_planets:
                            names.append(self._safe_str(p.get('name', '')))
                            rasis.append(self._safe_str(p.get('rasi_name', '')))
                            degrees.append(self._format_degree(p.get('degrees_in_rasi', '')))
                            nak_name = self._safe_str(p.get('nakshatra_name', ''))
                            nak_pada = self._safe_str(p.get('nakshatra_pada', ''))
                            nakshatras.append(f"{nak_name}-{nak_pada}" if nak_pada else nak_name)
                            retros.append('R' if p.get('retrograde') else '-')
                        
                        lines.append(f"  name: {', '.join(names)}")
                        lines.append(f"  rasi: {', '.join(rasis)}")
                        lines.append(f"  degree: {', '.join(degrees)}")
                        lines.append(f"  nakshatra: {', '.join(nakshatras)}")
                        lines.append(f"  retrograde: {', '.join(retros)}")
                
                # Houses
                houses = chart.get('houses', {})
                if houses and isinstance(houses, dict):
                    house_lines = []
                    for h in range(12):
                        planets_in_house = houses.get(str(h), houses.get(h, []))
                        if planets_in_house:
                            house_lines.append(f"H{h+1}: {', '.join(planets_in_house)}")
                    if house_lines:
                        lines.append("")
                        lines.append("houses:")
                        for hl in house_lines:
                            lines.append(f"  {hl}")
                
                # Special Lagnas
                special_lagnas = chart.get('special_lagnas', [])
                if special_lagnas:
                    lines.append("")
                    lines.append(f"special_lagnas[{len(special_lagnas)}]:")
                    sl_names = []
                    sl_rasis = []
                    for sl in special_lagnas:
                        if isinstance(sl, dict):
                            sl_names.append(self._safe_str(sl.get('name', '')))
                            sl_rasis.append(self._safe_str(sl.get('rasi_name', '')))
                    lines.append(f"  name: {', '.join(sl_names)}")
                    lines.append(f"  rasi: {', '.join(sl_rasis)}")
                
                # Upagrahas
                upagrahas = chart.get('upagrahas', [])
                if upagrahas:
                    lines.append("")
                    lines.append(f"upagrahas[{len(upagrahas)}]:")
                    u_names = []
                    u_rasis = []
                    for u in upagrahas:
                        if isinstance(u, dict):
                            u_names.append(self._safe_str(u.get('name', '')))
                            u_rasis.append(self._safe_str(u.get('rasi_name', '')))
                    lines.append(f"  name: {', '.join(u_names)}")
                    lines.append(f"  rasi: {', '.join(u_rasis)}")
        
        # === NAVAMSA D9 ===
        if 'divisional' in sections and api_data.get('d9'):
            d9 = api_data['d9']
            if isinstance(d9, dict) and 'error' not in d9:
                planets = d9.get('planets', [])
                valid_planets = [p for p in planets if isinstance(p, dict)]
                if valid_planets:
                    lines.append("")
                    lines.append(f"navamsa[{len(valid_planets)}]:")
                    names = [self._safe_str(p.get('name', '')) for p in valid_planets]
                    rasis = [self._safe_str(p.get('rasi_name', '')) for p in valid_planets]
                    lines.append(f"  name: {', '.join(names)}")
                    lines.append(f"  rasi: {', '.join(rasis)}")
        
        # === PANCHANGA ===
        if 'panchanga' in sections and api_data.get('panchanga'):
            panch = api_data['panchanga']
            if isinstance(panch, dict) and 'error' not in panch:
                lines.append("")
                lines.append("panchanga:")
                
                # Tithi
                if panch.get('tithi'):
                    t = panch['tithi']
                    if isinstance(t, dict):
                        lines.append(f"  tithi: {t.get('name', '')} ({t.get('paksha', '')})")
                    else:
                        lines.append(f"  tithi: {t}")
                
                # Nakshatra
                if panch.get('nakshatra'):
                    n = panch['nakshatra']
                    if isinstance(n, dict):
                        lines.append(f"  nakshatra: {n.get('name', '')} pada {n.get('pada', '')} (lord: {n.get('lord', '')})")
                    else:
                        lines.append(f"  nakshatra: {n}")
                
                # Yoga
                if panch.get('yoga'):
                    y = panch['yoga']
                    if isinstance(y, dict):
                        lines.append(f"  yoga: {y.get('name', '')}")
                    else:
                        lines.append(f"  yoga: {y}")
                
                # Karana
                if panch.get('karana'):
                    k = panch['karana']
                    if isinstance(k, dict):
                        lines.append(f"  karana: {k.get('name', '')}")
                    else:
                        lines.append(f"  karana: {k}")
                
                # Vaara
                if panch.get('vaara'):
                    lines.append(f"  vaara: {panch['vaara']}")
                
                # Sun/Moon times
                if panch.get('sunrise'):
                    lines.append(f"  sunrise: {panch['sunrise']}")
                if panch.get('sunset'):
                    lines.append(f"  sunset: {panch['sunset']}")
                
                # Rahu Kala
                if panch.get('rahu_kala'):
                    rk = panch['rahu_kala']
                    if isinstance(rk, dict):
                        lines.append(f"  rahu_kala: {rk.get('start', '')} - {rk.get('end', '')}")
        
        # === DASHA ===
        if 'dasha' in sections and api_data.get('vimsottari'):
            vim = api_data['vimsottari']
            if isinstance(vim, dict) and 'error' not in vim:
                lines.append("")
                lines.append("dasha:")
                
                # Balance at birth
                if vim.get('balance_at_birth'):
                    bal = vim['balance_at_birth']
                    if isinstance(bal, dict):
                        lines.append(f"  balance: {bal.get('planet', 'Unknown')} - {bal.get('years', 0)}y {bal.get('months', 0)}m {bal.get('days', 0)}d")
                
                # Main periods (Mahadasha)
                periods = vim.get('periods', [])
                if isinstance(periods, list) and periods:
                    valid_periods = [p for p in periods if isinstance(p, dict)][:9]
                    if valid_periods:
                        lines.append(f"  periods[{len(valid_periods)}]:")
                        for p in valid_periods:
                            planet = p.get('planet', '')
                            start = self._safe_str(p.get('start_date', ''))[:10]
                            end = self._safe_str(p.get('end_date', ''))[:10]
                            duration = p.get('duration_years')
                            dur_str = f" ({duration:.1f}y)" if duration else ""
                            lines.append(f"    {planet}: {start} to {end}{dur_str}")
                            
                            # Antardasha (AD) - show all with dates
                            sub_periods = p.get('sub_periods', [])
                            if sub_periods:
                                valid_subs = [sp for sp in sub_periods if isinstance(sp, dict)]
                                if valid_subs:
                                    # Summary line showing all AD lords
                                    sub_planets = [sp.get('planet', '') for sp in valid_subs]
                                    lines.append(f"      AD[{len(valid_subs)}]: {', '.join(sub_planets)}")
                                    
                                    # Detailed AD periods with dates
                                    for sp in valid_subs:
                                        sp_planet = sp.get('planet', '')
                                        sp_start = self._safe_str(sp.get('start_date', ''))[:10]
                                        sp_end = self._safe_str(sp.get('end_date', ''))[:10]
                                        sp_dur = sp.get('duration_years')
                                        # Smart duration formatting
                                        if sp_dur:
                                            if sp_dur < 0.1:
                                                sp_dur_days = int(sp_dur * 365.25)
                                                sp_dur_str = f" ({sp_dur_days}d)"
                                            elif sp_dur < 1:
                                                sp_dur_months = sp_dur * 12
                                                sp_dur_str = f" ({sp_dur_months:.1f}m)"
                                            else:
                                                sp_dur_str = f" ({sp_dur:.2f}y)"
                                        else:
                                            sp_dur_str = ""
                                        lines.append(f"        {sp_planet}: {sp_start} to {sp_end}{sp_dur_str}")
        
        # === STRENGTH ===
        if 'strength' in sections:
            strength_added = False
            
            # Shadbala
            if api_data.get('shadbala') and isinstance(api_data['shadbala'], dict):
                sb = api_data['shadbala']
                if 'error' not in sb and sb.get('planets'):
                    planets_data = sb['planets']
                    if isinstance(planets_data, dict):
                        if not strength_added:
                            lines.append("")
                            lines.append("strength:")
                            strength_added = True
                        
                        lines.append("  shadbala:")
                        for planet, data in planets_data.items():
                            if isinstance(data, dict):
                                total = data.get('total_shadbala', data.get('total', 0))
                                pct = data.get('percent_strength', 0)
                                lines.append(f"    {planet}: {total:.2f} ({pct:.0f}%)")
            
            # Ashtakavarga SAV
            if api_data.get('ashtakavarga') and isinstance(api_data['ashtakavarga'], dict):
                av = api_data['ashtakavarga']
                if 'error' not in av and av.get('sarvashtakavarga'):
                    sav = av['sarvashtakavarga']
                    if isinstance(sav, list):
                        if not strength_added:
                            lines.append("")
                            lines.append("strength:")
                            strength_added = True
                        lines.append(f"  sav[12]: {', '.join(str(v) for v in sav)}")
                        lines.append(f"  sav_total: {sum(sav)}")
        
        # === YOGAS ===
        if 'yogas' in sections and api_data.get('yogas'):
            yogas = api_data['yogas']
            if isinstance(yogas, dict) and 'error' not in yogas:
                lines.append("")
                lines.append("yogas:")
                
                # Summary
                if yogas.get('total_yogas'):
                    lines.append(f"  total: {yogas['total_yogas']}")
                
                if yogas.get('chart_strength'):
                    cs = yogas['chart_strength']
                    if isinstance(cs, dict):
                        lines.append(f"  rating: {cs.get('rating', '')}")
                
                # By category
                for cat in ['excellent', 'good', 'neutral', 'inauspicious']:
                    cat_data = yogas.get('yogas_by_category', {}).get(cat, [])
                    if not cat_data:
                        cat_data = yogas.get(cat, [])
                    if cat_data and isinstance(cat_data, list):
                        yoga_names = [y.get('name', str(y)) if isinstance(y, dict) else str(y) for y in cat_data[:5]]
                        if yoga_names:
                            lines.append(f"  {cat}: {', '.join(yoga_names)}")
                
                # All yogas list
                all_yogas = yogas.get('all_yogas', [])
                if all_yogas:
                    lines.append(f"  all_yogas[{len(all_yogas)}]:")
                    for y in all_yogas[:10]:
                        if isinstance(y, dict):
                            lines.append(f"    {y.get('name', '')}: {y.get('category', '')}")
        
        # === DOSHAS ===
        if 'doshas' in sections and api_data.get('doshas'):
            doshas_data = api_data['doshas']
            if isinstance(doshas_data, dict) and 'error' not in doshas_data:
                lines.append("")
                lines.append("doshas:")
                
                # Summary
                if doshas_data.get('dosha_summary'):
                    ds = doshas_data['dosha_summary']
                    if isinstance(ds, dict):
                        lines.append(f"  total: {ds.get('total_doshas', 0)}")
                        lines.append(f"  high: {ds.get('high_severity', 0)}, medium: {ds.get('medium_severity', 0)}, low: {ds.get('low_severity', 0)}")
                
                if doshas_data.get('overall_dosha_impact'):
                    lines.append(f"  impact: {doshas_data['overall_dosha_impact']}")
                
                # Individual doshas
                doshas_dict = doshas_data.get('doshas', {})
                if isinstance(doshas_dict, dict):
                    for dosha_name, dosha_info in doshas_dict.items():
                        if isinstance(dosha_info, dict) and dosha_info.get('present'):
                            sev = dosha_info.get('severity', 'Unknown')
                            desc = dosha_info.get('description', '')[:50]
                            lines.append(f"  {dosha_name}: {sev} - {desc}")
        
        # === TRANSITS ===
        if 'transits' in sections and api_data.get('transits'):
            trans = api_data['transits']
            if isinstance(trans, dict) and 'error' not in trans and trans.get('transit_planets'):
                transit_planets = trans['transit_planets']
                if isinstance(transit_planets, dict):
                    lines.append("")
                    lines.append(f"transits ({trans.get('transit_date', 'now')}):")
                    
                    for name, data in transit_planets.items():
                        if isinstance(data, dict):
                            rasi = data.get('rasi_name', '')
                            h_l = data.get('house_from_lagna', '')
                            h_m = data.get('house_from_moon', '')
                            retro = ' (R)' if data.get('is_retrograde') else ''
                            lines.append(f"  {name}: {rasi}{retro} -> H{h_l} from Lagna, H{h_m} from Moon")
        
        return "\n".join(lines)
    
    def generate_markdown_format(self, birth_details: dict, sections: List[str] = None) -> str:
        """Generate readable Markdown format from full API data"""
        if sections is None:
            sections = ['chart', 'divisional', 'panchanga', 'dasha', 'strength', 'yogas', 'doshas', 'transits']
        
        ayanamsa = birth_details.get('ayanamsa', 'LAHIRI')
        api_data = self._get_all_api_data(birth_details, ayanamsa)
        
        lines = []
        
        # Header
        date_str = birth_details.get('date', '')
        time_str = birth_details.get('time', '')
        place_name = birth_details.get('place', {}).get('name', 'Unknown')
        
        lines.append("# Vedic Horoscope")
        lines.append("")
        lines.append(f"**Birth:** {date_str} at {time_str}")
        lines.append(f"**Location:** {place_name}")
        lines.append(f"**Ayanamsa:** {ayanamsa}")
        lines.append("")
        
        # === CHART ===
        if 'chart' in sections and api_data.get('rasi_chart'):
            chart = api_data['rasi_chart']
            if isinstance(chart, dict) and 'error' not in chart:
                
                # Ascendant
                if chart.get('ascendant') and isinstance(chart['ascendant'], dict):
                    asc = chart['ascendant']
                    lines.append("## Ascendant")
                    lines.append("")
                    lines.append(f"**{asc.get('rasi_name', '')}** at {self._format_degree(asc.get('degrees_in_rasi', ''))}")
                    lines.append(f"- Nakshatra: {asc.get('nakshatra_name', '')} Pada {asc.get('nakshatra_pada', '')}")
                    lines.append("")
                
                # Planets Table
                lines.append("## Planets")
                lines.append("")
                lines.append("| Planet | Rasi | Degree | Nakshatra | Pada | R |")
                lines.append("|--------|------|--------|-----------|------|---|")
                
                for p in chart.get('planets', []):
                    if isinstance(p, dict):
                        retro = '℞' if p.get('retrograde') else ''
                        lines.append(f"| {p.get('name', '')} | {p.get('rasi_name', '')} | {self._format_degree(p.get('degrees_in_rasi', ''))} | {p.get('nakshatra_name', '')} | {p.get('nakshatra_pada', '')} | {retro} |")
                lines.append("")
                
                # Houses
                houses = chart.get('houses', {})
                if houses:
                    lines.append("## Houses")
                    lines.append("")
                    for h in range(12):
                        planets_in_house = houses.get(str(h), houses.get(h, []))
                        if planets_in_house:
                            lines.append(f"- **House {h+1}:** {', '.join(planets_in_house)}")
                    lines.append("")
                
                # Special Lagnas
                special_lagnas = chart.get('special_lagnas', [])
                if special_lagnas:
                    lines.append("## Special Lagnas")
                    lines.append("")
                    lines.append("| Lagna | Rasi | Nakshatra |")
                    lines.append("|-------|------|-----------|")
                    for sl in special_lagnas:
                        if isinstance(sl, dict):
                            lines.append(f"| {sl.get('name', '')} | {sl.get('rasi_name', '')} | {sl.get('nakshatra_name', '')} |")
                    lines.append("")
        
        # === PANCHANGA ===
        if 'panchanga' in sections and api_data.get('panchanga'):
            panch = api_data['panchanga']
            if isinstance(panch, dict) and 'error' not in panch:
                lines.append("## Panchanga")
                lines.append("")
                
                if panch.get('tithi'):
                    t = panch['tithi']
                    name = t.get('name', '') if isinstance(t, dict) else str(t)
                    paksha = t.get('paksha', '') if isinstance(t, dict) else ''
                    lines.append(f"- **Tithi:** {name} ({paksha})")
                
                if panch.get('nakshatra'):
                    n = panch['nakshatra']
                    name = n.get('name', '') if isinstance(n, dict) else str(n)
                    pada = n.get('pada', '') if isinstance(n, dict) else ''
                    lord = n.get('lord', '') if isinstance(n, dict) else ''
                    lines.append(f"- **Nakshatra:** {name} Pada {pada} (Lord: {lord})")
                
                if panch.get('yoga'):
                    y = panch['yoga']
                    name = y.get('name', '') if isinstance(y, dict) else str(y)
                    lines.append(f"- **Yoga:** {name}")
                
                if panch.get('karana'):
                    k = panch['karana']
                    name = k.get('name', '') if isinstance(k, dict) else str(k)
                    lines.append(f"- **Karana:** {name}")
                
                if panch.get('vaara'):
                    lines.append(f"- **Vaara:** {panch['vaara']}")
                
                if panch.get('sunrise'):
                    lines.append(f"- **Sunrise:** {panch['sunrise']}")
                if panch.get('sunset'):
                    lines.append(f"- **Sunset:** {panch['sunset']}")
                
                lines.append("")
        
        # === DASHA ===
        if 'dasha' in sections and api_data.get('vimsottari'):
            vim = api_data['vimsottari']
            if isinstance(vim, dict) and 'error' not in vim:
                lines.append("## Vimsottari Dasha")
                lines.append("")
                
                if vim.get('balance_at_birth'):
                    bal = vim['balance_at_birth']
                    if isinstance(bal, dict):
                        lines.append(f"**Balance at Birth:** {bal.get('planet', 'Unknown')} - {bal.get('years', 0)}y {bal.get('months', 0)}m {bal.get('days', 0)}d")
                        lines.append("")
                
                # Mahadasha overview table
                lines.append("### Mahadasha Periods")
                lines.append("")
                lines.append("| Planet | Start | End | Duration |")
                lines.append("|--------|-------|-----|----------|")
                
                periods = vim.get('periods', [])
                for p in periods[:9]:
                    if isinstance(p, dict):
                        start = self._safe_str(p.get('start_date', ''))[:10]
                        end = self._safe_str(p.get('end_date', ''))[:10]
                        dur = p.get('duration_years')
                        dur_str = f"{dur:.1f}y" if dur else ""
                        lines.append(f"| {p.get('planet', '')} | {start} | {end} | {dur_str} |")
                lines.append("")
                
                # Detailed breakdown for each Mahadasha
                for p in periods[:9]:
                    if isinstance(p, dict):
                        planet = p.get('planet', '')
                        start = self._safe_str(p.get('start_date', ''))[:10]
                        end = self._safe_str(p.get('end_date', ''))[:10]
                        dur = p.get('duration_years')
                        dur_str = f" ({dur:.1f}y)" if dur else ""
                        lines.append(f"### {planet} Mahadasha{dur_str}")
                        lines.append(f"*{start} to {end}*")
                        lines.append("")
                        
                        # Antardasha table
                        sub_periods = p.get('sub_periods', [])
                        if sub_periods:
                            valid_subs = [sp for sp in sub_periods if isinstance(sp, dict)]
                            if valid_subs:
                                lines.append("| Antardasha | Start | End | Duration |")
                                lines.append("|------------|-------|-----|----------|")
                                
                                for sp in valid_subs:
                                    sp_planet = sp.get('planet', '')
                                    sp_start = self._safe_str(sp.get('start_date', ''))[:10]
                                    sp_end = self._safe_str(sp.get('end_date', ''))[:10]
                                    sp_dur = sp.get('duration_years')
                                    if sp_dur:
                                        if sp_dur < 0.1:
                                            sp_dur_str = f"{int(sp_dur * 365.25)}d"
                                        elif sp_dur < 1:
                                            sp_dur_str = f"{sp_dur * 12:.1f}m"
                                        else:
                                            sp_dur_str = f"{sp_dur:.2f}y"
                                    else:
                                        sp_dur_str = ""
                                    lines.append(f"| {sp_planet} | {sp_start} | {sp_end} | {sp_dur_str} |")
                                lines.append("")
        
        # === STRENGTH ===
        if 'strength' in sections:
            if api_data.get('shadbala') and isinstance(api_data['shadbala'], dict):
                sb = api_data['shadbala']
                if 'error' not in sb and sb.get('planets'):
                    lines.append("## Shadbala Strength")
                    lines.append("")
                    lines.append("| Planet | Total | Strength % |")
                    lines.append("|--------|-------|------------|")
                    
                    for planet, data in sb['planets'].items():
                        if isinstance(data, dict):
                            total = data.get('total_shadbala', 0)
                            pct = data.get('percent_strength', 0)
                            lines.append(f"| {planet} | {total:.2f} | {pct:.0f}% |")
                    lines.append("")
            
            if api_data.get('ashtakavarga') and isinstance(api_data['ashtakavarga'], dict):
                av = api_data['ashtakavarga']
                if 'error' not in av and av.get('sarvashtakavarga'):
                    sav = av['sarvashtakavarga']
                    if isinstance(sav, list):
                        lines.append("## Sarvashtakavarga")
                        lines.append("")
                        rasi_names = ['Ari', 'Tau', 'Gem', 'Can', 'Leo', 'Vir', 'Lib', 'Sco', 'Sag', 'Cap', 'Aqu', 'Pis']
                        lines.append("| " + " | ".join(rasi_names) + " | Total |")
                        lines.append("|" + "------|" * 13)
                        lines.append("| " + " | ".join(str(v) for v in sav) + f" | {sum(sav)} |")
                        lines.append("")
        
        # === YOGAS ===
        if 'yogas' in sections and api_data.get('yogas'):
            yogas = api_data['yogas']
            if isinstance(yogas, dict) and 'error' not in yogas:
                lines.append("## Yogas")
                lines.append("")
                
                if yogas.get('chart_strength'):
                    cs = yogas['chart_strength']
                    if isinstance(cs, dict):
                        lines.append(f"**Overall Rating:** {cs.get('rating', '')}")
                        lines.append("")
                
                for cat in ['excellent', 'good', 'neutral']:
                    cat_data = yogas.get('yogas_by_category', {}).get(cat, [])
                    if not cat_data:
                        cat_data = yogas.get(cat, [])
                    if cat_data:
                        lines.append(f"### {cat.title()} Yogas")
                        lines.append("")
                        for y in cat_data[:5]:
                            if isinstance(y, dict):
                                lines.append(f"- **{y.get('name', '')}**")
                            else:
                                lines.append(f"- {y}")
                        lines.append("")
        
        # === DOSHAS ===
        if 'doshas' in sections and api_data.get('doshas'):
            doshas_data = api_data['doshas']
            if isinstance(doshas_data, dict) and 'error' not in doshas_data:
                doshas_dict = doshas_data.get('doshas', {})
                active_doshas = []
                if isinstance(doshas_dict, dict):
                    for name, info in doshas_dict.items():
                        if isinstance(info, dict) and info.get('present'):
                            active_doshas.append((name, info))
                
                if active_doshas:
                    lines.append("## Doshas")
                    lines.append("")
                    if doshas_data.get('overall_dosha_impact'):
                        lines.append(f"**Impact:** {doshas_data['overall_dosha_impact']}")
                        lines.append("")
                    
                    for name, info in active_doshas:
                        lines.append(f"### {name.replace('_', ' ').title()}")
                        lines.append(f"- **Severity:** {info.get('severity', 'Unknown')}")
                        if info.get('description'):
                            lines.append(f"- **Description:** {info['description']}")
                        if info.get('remedies'):
                            lines.append(f"- **Remedies:** {', '.join(info['remedies'])}")
                        lines.append("")
        
        # === TRANSITS ===
        if 'transits' in sections and api_data.get('transits'):
            trans = api_data['transits']
            if isinstance(trans, dict) and 'error' not in trans and trans.get('transit_planets'):
                lines.append("## Current Transits")
                lines.append(f"*As of {trans.get('transit_date', 'today')}*")
                lines.append("")
                lines.append("| Planet | Rasi | House (Lagna) | House (Moon) | R |")
                lines.append("|--------|------|---------------|--------------|---|")
                
                for name, data in trans['transit_planets'].items():
                    if isinstance(data, dict):
                        retro = '℞' if data.get('is_retrograde') else ''
                        lines.append(f"| {name} | {data.get('rasi_name', '')} | {data.get('house_from_lagna', '')} | {data.get('house_from_moon', '')} | {retro} |")
                lines.append("")
        
        return "\n".join(lines)
    
    def generate_json_minimal(self, birth_details: dict, sections: List[str] = None) -> Dict:
        """Generate minified JSON from full API data"""
        if sections is None:
            sections = ['chart', 'panchanga', 'dasha', 'strength', 'yogas', 'doshas', 'transits']
        
        ayanamsa = birth_details.get('ayanamsa', 'LAHIRI')
        api_data = self._get_all_api_data(birth_details, ayanamsa)
        
        result = {
            'birth': {
                'date': birth_details.get('date', ''),
                'time': birth_details.get('time', ''),
                'place': birth_details.get('place', {}).get('name', ''),
                'aya': ayanamsa
            }
        }
        
        if 'chart' in sections and api_data.get('rasi_chart'):
            result['chart'] = api_data['rasi_chart']
        
        if 'divisional' in sections and api_data.get('d9'):
            result['d9'] = api_data['d9']
        
        if 'panchanga' in sections and api_data.get('panchanga'):
            result['panch'] = api_data['panchanga']
        
        if 'dasha' in sections and api_data.get('vimsottari'):
            result['dasha'] = api_data['vimsottari']
        
        if 'strength' in sections:
            if api_data.get('shadbala'):
                result['sb'] = api_data['shadbala']
            if api_data.get('ashtakavarga'):
                result['av'] = api_data['ashtakavarga']
        
        if 'yogas' in sections and api_data.get('yogas'):
            result['yoga'] = api_data['yogas']
        
        if 'doshas' in sections and api_data.get('doshas'):
            result['dosha'] = api_data['doshas']
        
        if 'transits' in sections and api_data.get('transits'):
            result['transit'] = api_data['transits']
        
        return result


# Singleton
_ai_export_service = None

def get_ai_export_service() -> AIExportService:
    global _ai_export_service
    if _ai_export_service is None:
        _ai_export_service = AIExportService()
    return _ai_export_service
