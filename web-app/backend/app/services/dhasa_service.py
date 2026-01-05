"""
Dhasa calculation service
Handles all 47 types of dhasa systems
"""
import sys
import os
import inspect
from collections import OrderedDict

# Add PyJHora to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../PyJHora/src'))

from jhora.panchanga import drik
from jhora.horoscope.dhasa.graha import (
    vimsottari, ashtottari, yogini, shodasottari, dwadasottari,
    dwisatpathi, panchottari, sataatbika, chathuraaseethi_sama,
    shastihayani, shattrimsa_sama, naisargika, tara, karaka, aayu
)
from jhora.horoscope.dhasa.raasi import (
    narayana, kendradhi_rasi, sudasa, drig, nirayana, shoola,
    chara, lagnamsaka, padhanadhamsa, mandooka, sthira, tara_lagna,
    brahma, varnada, yogardha, navamsa, paryaaya, trikona, kalachakra,
    moola, chakra
)
from jhora.horoscope.dhasa.annual import mudda, patyayini
from jhora import utils, const
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta


class DhasaService:
    """Service for all Dhasa calculations"""
    
    GRAHA_DHASAS = {
        'vimsottari': ('Vimsottari', vimsottari),
        'ashtottari': ('Ashtottari', ashtottari),
        'yogini': ('Yogini', yogini),
        'shodasottari': ('Shodasottari', shodasottari),
        'dwadasottari': ('Dwadasottari', dwadasottari),
        'dwisatpathi': ('Dwisatpathi', dwisatpathi),
        'panchottari': ('Panchottari', panchottari),
        'sataatbika': ('Sataatbika', sataatbika),
        'chathuraaseethi_sama': ('Chathuraaseethi Sama', chathuraaseethi_sama),
        'shastihayani': ('Shastihayani', shastihayani),
        'shattrimsa_sama': ('Shattrimsa Sama', shattrimsa_sama),
        'naisargika': ('Naisargika', naisargika),
        'tara': ('Tara', tara),
        'karaka': ('Karaka', karaka),
        'aayu': ('Aayu', aayu),
    }
    
    RAASI_DHASAS = {
        'narayana': ('Narayana', narayana),
        'kendradhi_rasi': ('Kendradhi Rasi', kendradhi_rasi),
        'sudasa': ('Sudasa', sudasa),
        'drig': ('Drig', drig),
        'nirayana': ('Nirayana', nirayana),
        'shoola': ('Shoola', shoola),
        'chara': ('Chara', chara),
        'lagnamsaka': ('Lagnamsaka', lagnamsaka),
        'padhanadhamsa': ('Padhanadhamsa', padhanadhamsa),
        'mandooka': ('Mandooka', mandooka),
        'sthira': ('Sthira', sthira),
        'tara_lagna': ('Tara Lagna', tara_lagna),
        'brahma': ('Brahma', brahma),
        'varnada': ('Varnada', varnada),
        'yogardha': ('Yogardha', yogardha),
        'navamsa': ('Navamsa', navamsa),
        'paryaaya': ('Paryaaya', paryaaya),
        'trikona': ('Trikona', trikona),
        'kalachakra': ('Kalachakra', kalachakra),
        'moola': ('Moola', moola),
        'chakra': ('Chakra', chakra),
    }
    
    ANNUAL_DHASAS = {
        'mudda': ('Mudda', mudda),
        'patyayini': ('Patyayini', patyayini),
    }
    
    PLANET_NAMES = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']
    RASI_NAMES = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 
                  'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    DAYS_IN_YEAR = 365.25
    
    def __init__(self):
        pass
    
    def _parse_birth_details(self, birth_details: Dict[str, Any]):
        """Parse birth details"""
        date_str = birth_details['date']
        year, month, day = map(int, date_str.split('-'))
        dob = (year, month, day)
        
        time_str = birth_details['time']
        hour, minute, second = map(int, time_str.split(':'))
        tob = (hour, minute, second)
        
        place_info = birth_details['place']
        place = drik.Place(
            place_info['name'],
            place_info['latitude'],
            place_info['longitude'],
            place_info['timezone']
        )
        
        return dob, tob, place
    
    def _set_ayanamsa(self, ayanamsa: str = "LAHIRI"):
        """Set ayanamsa mode"""
        drik.set_ayanamsa_mode(ayanamsa.upper())
    
    def get_vimsottari_dhasa(self, birth_details: Dict[str, Any], 
                            include_antardhasa: bool = True,
                            ayanamsa: str = "LAHIRI",
                            max_sub_levels: int = 2,
                            focus_mahadasha_index: Optional[int] = None) -> Dict[str, Any]:
        """Calculate Vimsottari Dhasa"""
        return self._compute_graha_dhasa('vimsottari', birth_details, include_antardhasa, ayanamsa, max_sub_levels, focus_mahadasha_index)
    
    def get_any_graha_dhasa(self, birth_details: Dict[str, Any], 
                           dhasa_type: str,
                           include_antardhasa: bool = True,
                           ayanamsa: str = "LAHIRI",
                           max_sub_levels: int = 2,
                           focus_mahadasha_index: Optional[int] = None) -> Dict[str, Any]:
        """Calculate any Graha (Nakshatra) based dhasa"""
        return self._compute_graha_dhasa(dhasa_type, birth_details, include_antardhasa, ayanamsa, max_sub_levels, focus_mahadasha_index)
    
    def get_any_raasi_dhasa(self, birth_details: Dict[str, Any], 
                           dhasa_type: str,
                           include_antardhasa: bool = True,
                           ayanamsa: str = "LAHIRI",
                           max_sub_levels: int = 2) -> Dict[str, Any]:
        """Calculate any Raasi based dhasa"""
        return self._compute_raasi_dhasa(dhasa_type, birth_details, include_antardhasa, ayanamsa, max_sub_levels)
    
    def get_all_applicable_dhasas(self, birth_details: Dict[str, Any],
                                 ayanamsa: str = "LAHIRI") -> Dict[str, Any]:
        """Get list of all applicable dhasas for the chart"""
        result = {
            'graha_dhasas': list(self.GRAHA_DHASAS.keys()),
            'raasi_dhasas': list(self.RAASI_DHASAS.keys()),
            'annual_dhasas': list(self.ANNUAL_DHASAS.keys()),
            'total_count': len(self.GRAHA_DHASAS) + len(self.RAASI_DHASAS) + len(self.ANNUAL_DHASAS)
        }
        
        return result
    
    def _compute_graha_dhasa(self, dhasa_type: str, birth_details: Dict[str, Any],
                             include_antardhasa: bool, ayanamsa: str,
                             max_sub_levels: int = 2,
                             focus_mahadasha_index: Optional[int] = None) -> Dict[str, Any]:
        if dhasa_type not in self.GRAHA_DHASAS:
            return {'error': f'Unknown graha dhasa type: {dhasa_type}', 'dhasa_type': dhasa_type}
        
        dhasa_name, dhasa_module = self.GRAHA_DHASAS[dhasa_type]
        calculation = self._calculate_dhasa_periods(
            dhasa_module,
            dhasa_type,
            birth_details,
            include_antardhasa,
            ayanamsa,
            category='graha',
            max_sub_levels=max_sub_levels,
            focus_mahadasha_index=focus_mahadasha_index
        )
        
        if 'error' in calculation:
            return {
                'error': calculation['error'],
                'dhasa_type': dhasa_name
            }
        
        balance = calculation.get('balance')
        
        return {
            'dhasa_type': dhasa_name,
            'birth_date': birth_details['date'],
            'birth_time': birth_details['time'],
            'balance_at_birth': self._format_balance(balance) if balance else {},
            'periods': calculation['periods'],
            'include_antardhasa': include_antardhasa
        }
    
    def _compute_raasi_dhasa(self, dhasa_type: str, birth_details: Dict[str, Any],
                             include_antardhasa: bool, ayanamsa: str,
                             max_sub_levels: int = 2) -> Dict[str, Any]:
        if dhasa_type not in self.RAASI_DHASAS:
            return {'error': f'Unknown raasi dhasa type: {dhasa_type}', 'dhasa_type': dhasa_type}
        
        dhasa_name, dhasa_module = self.RAASI_DHASAS[dhasa_type]
        calculation = self._calculate_dhasa_periods(
            dhasa_module,
            dhasa_type,
            birth_details,
            include_antardhasa,
            ayanamsa,
            category='raasi',
            max_sub_levels=max_sub_levels
        )
        
        if 'error' in calculation:
            return {
                'error': calculation['error'],
                'dhasa_type': dhasa_name
            }
        
        return {
            'dhasa_type': dhasa_name,
            'birth_date': birth_details['date'],
            'birth_time': birth_details['time'],
            'periods': calculation['periods'],
            'include_antardhasa': include_antardhasa
        }
    
    def _calculate_dhasa_periods(self, dhasa_module, dhasa_type: str,
                                 birth_details: Dict[str, Any],
                                 include_antardhasa: bool,
                                 ayanamsa: str,
                                 category: str,
                                 max_sub_levels: int = 2,
                                 focus_mahadasha_index: Optional[int] = None) -> Dict[str, Any]:
        self._set_ayanamsa(ayanamsa)
        resolver = self._resolve_dhasa_callable(dhasa_module, dhasa_type)
        
        if resolver is None:
            return {'error': f'No calculation function found for {dhasa_type}'}
        
        execution = self._execute_dhasa_callable(resolver, birth_details, include_antardhasa)
        periods_raw = execution.get('periods_raw')
        
        if not periods_raw:
            return {'error': f'{dhasa_type} calculation returned no periods'}
        
        formatted_periods = self._format_periods_general(periods_raw, category)
        if (
            dhasa_type == 'vimsottari'
            and include_antardhasa
            and max_sub_levels
            and max_sub_levels > 2
        ):
            deep_periods = self._compute_vimsottari_multi_level(
                birth_details,
                max_sub_levels,
                focus_mahadasha_index
            )
            if deep_periods:
                formatted_periods = deep_periods
        if (
            dhasa_type == 'yogini'
            and include_antardhasa
            and max_sub_levels
            and max_sub_levels > 2
        ):
            deep_periods_y = self._compute_yogini_multi_level(
                birth_details,
                max_sub_levels,
                focus_mahadasha_index
            )
            if deep_periods_y:
                formatted_periods = deep_periods_y
        if not formatted_periods:
            return {'error': f'{dhasa_type} periods could not be formatted'}
        
        balance_data = execution.get('balance')
        needs_balance_details = (
            not balance_data or
            (isinstance(balance_data, (list, tuple)) and len(balance_data) < 4)
        )
        if needs_balance_details:
            balance_func = None
            jd = execution.get('jd')
            place = execution.get('place')
            balance_candidates = [
                f'{dhasa_type}_balance_of_dasa',
                f'{dhasa_type}_balance',
                'balance_of_dasa'
            ]
            for candidate in balance_candidates:
                if hasattr(dhasa_module, candidate):
                    balance_func = getattr(dhasa_module, candidate)
                    break
            if balance_func and jd is not None and place is not None:
                try:
                    balance_data = balance_func(jd, place)
                except Exception:
                    pass
        
        return {
            'periods': formatted_periods,
            'balance': balance_data
        }
    
    def _format_dhasa_periods(self, dhasa_periods) -> List[Dict[str, Any]]:
        """Format graha dhasa periods"""
        formatted = []
        
        try:
            for period in dhasa_periods:
                if isinstance(period, (list, tuple)) and len(period) >= 3:
                    planet_idx = period[0]
                    start_date = period[1]
                    end_date = period[2]
                    
                    period_data = {
                        'planet': self.PLANET_NAMES[planet_idx] if planet_idx < 9 else f'Planet-{planet_idx}',
                        'start_date': start_date if isinstance(start_date, str) else str(start_date),
                        'end_date': end_date if isinstance(end_date, str) else str(end_date),
                    }
                    
                    # Check for sub-periods
                    if len(period) > 3 and isinstance(period[3], list):
                        period_data['sub_periods'] = self._format_dhasa_periods(period[3])
                    
                    formatted.append(period_data)
        except Exception as e:
            formatted.append({'error': f'Formatting error: {str(e)}'})
        
        return formatted
    
    def _format_raasi_dhasa_periods(self, dhasa_periods) -> List[Dict[str, Any]]:
        """Format raasi dhasa periods"""
        formatted = []
        
        try:
            for period in dhasa_periods:
                if isinstance(period, (list, tuple)) and len(period) >= 3:
                    rasi_idx = period[0]
                    start_date = period[1]
                    end_date = period[2]
                    
                    period_data = {
                        'rasi': self.RASI_NAMES[rasi_idx] if rasi_idx < 12 else f'Rasi-{rasi_idx}',
                        'rasi_index': rasi_idx,
                        'start_date': start_date if isinstance(start_date, str) else str(start_date),
                        'end_date': end_date if isinstance(end_date, str) else str(end_date),
                    }
                    
                    # Check for sub-periods
                    if len(period) > 3 and isinstance(period[3], list):
                        period_data['sub_periods'] = self._format_raasi_dhasa_periods(period[3])
                    
                    formatted.append(period_data)
        except Exception as e:
            formatted.append({'error': f'Formatting error: {str(e)}'})
        
        return formatted
    
    def _format_balance(self, balance) -> Dict[str, Any]:
        """Format balance at birth"""
        if isinstance(balance, (list, tuple)):
            if len(balance) >= 4:
                planet_idx = balance[0] if isinstance(balance[0], int) else 0
                return {
                    'planet': self.PLANET_NAMES[planet_idx] if 0 <= planet_idx < len(self.PLANET_NAMES) else f'Planet-{planet_idx}',
                    'years': balance[1],
                    'months': balance[2],
                    'days': balance[3],
                }
            if len(balance) == 3:
                return {
                    'planet': 'Unknown',
                    'years': balance[0],
                    'months': balance[1],
                    'days': balance[2],
                }
        return {}

    def _compute_vimsottari_multi_level(self, birth_details: Dict[str, Any],
                                        max_sub_levels: int,
                                        focus_mahadasha_index: Optional[int] = None) -> List[Dict[str, Any]]:
        if max_sub_levels <= 1:
            return []
        
        dob, tob, place = self._parse_birth_details(birth_details)
        jd = utils.julian_day_number(dob, tob)
        try:
            dashas = vimsottari.vimsottari_mahadasa(jd, place)
        except Exception:
            return []
        
        periods = []
        for maha_lord, start_jd in dashas.items():
            if focus_mahadasha_index is not None and maha_lord != focus_mahadasha_index:
                continue
            
            duration_years = vimsottari.vimsottari_dict.get(maha_lord)
            if duration_years is None:
                continue
            period = {
                'planet': self._label_from_index(maha_lord, self.PLANET_NAMES, 'Planet'),
                'start_date': self._format_datetime_output(self._jd_to_datetime(start_jd)),
                'end_date': self._format_datetime_output(
                    self._jd_to_datetime(start_jd + duration_years * const.sidereal_year)
                ),
                'duration_years': duration_years,
                'planet_index': maha_lord
            }
            sub_periods = self._build_vimsottari_subperiods(
                maha_lord,
                start_jd,
                duration_years,
                current_depth=1,
                max_depth=max_sub_levels
            )
            if sub_periods:
                period['sub_periods'] = sub_periods
            periods.append(period)
        
        return periods
    
    def _build_vimsottari_subperiods(self, reference_lord: int,
                                     start_jd: float,
                                     parent_duration_years: float,
                                     current_depth: int,
                                     max_depth: int) -> List[Dict[str, Any]]:
        if current_depth >= max_depth:
            return []
        
        sub_periods = []
        lord = reference_lord
        current_start = start_jd
        human_span = vimsottari.human_life_span_for_vimsottari_dhasa
        
        for _ in range(9):
            ratio = vimsottari.vimsottari_dict.get(lord)
            if ratio is None:
                break
            duration_years = parent_duration_years * (ratio / human_span)
            end_jd = current_start + duration_years * const.sidereal_year
            period = {
                'planet': self._label_from_index(lord, self.PLANET_NAMES, 'Planet'),
                'start_date': self._format_datetime_output(self._jd_to_datetime(current_start)),
                'end_date': self._format_datetime_output(self._jd_to_datetime(end_jd)),
                'duration_years': duration_years,
                'planet_index': lord
            }
            child_periods = self._build_vimsottari_subperiods(
                lord,
                current_start,
                duration_years,
                current_depth=current_depth + 1,
                max_depth=max_depth
            )
            if child_periods:
                period['sub_periods'] = child_periods
            sub_periods.append(period)
            current_start = end_jd
            lord = vimsottari.vimsottari_next_adhipati(lord)
        
        return sub_periods

    def _compute_yogini_multi_level(self, birth_details: Dict[str, Any],
                                    max_sub_levels: int,
                                    focus_mahadasha_index: Optional[int] = None) -> List[Dict[str, Any]]:
        if max_sub_levels <= 1:
            return []
        dob, tob, place = self._parse_birth_details(birth_details)
        try:
            rows = yogini.get_dhasa_bhukthi(dob, tob, place, include_antardhasa=True)
        except Exception:
            return []
        periods: List[Dict[str, Any]] = []
        i = 0
        total_cycle = sum(yogini.dhasa_adhipathi_list.values()) if hasattr(yogini, 'dhasa_adhipathi_list') else 36.0
        while i < len(rows):
            row = rows[i]
            if not isinstance(row, (list, tuple)) or len(row) < 4:
                break
            maha_lord = int(row[0])
            if focus_mahadasha_index is not None and maha_lord != focus_mahadasha_index:
                i += 8
                continue
            maha_start_dt = self._parse_date_value(row[2])
            if maha_start_dt is None:
                i += 8
                continue
            maha_duration_years = float(yogini.dhasa_adhipathi_list.get(maha_lord, 0))
            maha_end_dt = maha_start_dt + timedelta(days=maha_duration_years * const.sidereal_year)
            period: Dict[str, Any] = {
                'planet': self._label_from_index(maha_lord, self.PLANET_NAMES, 'Planet'),
                'start_date': self._format_datetime_output(maha_start_dt),
                'end_date': self._format_datetime_output(maha_end_dt),
                'duration_years': maha_duration_years,
                'planet_index': maha_lord
            }
            sub_periods: List[Dict[str, Any]] = []
            for k in range(8):
                if i + k >= len(rows):
                    break
                sub = rows[i + k]
                if not isinstance(sub, (list, tuple)) or len(sub) < 4:
                    continue
                sub_lord = int(sub[1])
                sub_start_dt = self._parse_date_value(sub[2])
                sub_duration_years = float(sub[3])
                if sub_start_dt is None:
                    continue
                sub_end_dt = sub_start_dt + timedelta(days=sub_duration_years * const.sidereal_year)
                sub_period: Dict[str, Any] = {
                    'planet': self._label_from_index(sub_lord, self.PLANET_NAMES, 'Planet'),
                    'start_date': self._format_datetime_output(sub_start_dt),
                    'end_date': self._format_datetime_output(sub_end_dt),
                    'duration_years': sub_duration_years,
                    'planet_index': sub_lord
                }
                child_periods = self._build_yogini_subperiods(
                    sub_lord,
                    sub_start_dt,
                    sub_duration_years,
                    current_depth=2,
                    max_depth=max_sub_levels,
                    total_cycle=total_cycle
                )
                if child_periods:
                    sub_period['sub_periods'] = child_periods
                sub_periods.append(sub_period)
            if sub_periods:
                period['sub_periods'] = sub_periods
            periods.append(period)
            i += 8
            if focus_mahadasha_index is not None:
                break
        return periods

    def _build_yogini_subperiods(self, reference_lord: int,
                                  start_dt: datetime,
                                  parent_duration_years: float,
                                  current_depth: int,
                                  max_depth: int,
                                  total_cycle: float) -> List[Dict[str, Any]]:
        if current_depth >= max_depth:
            return []
        sub_periods: List[Dict[str, Any]] = []
        lord = reference_lord
        current_start = start_dt
        for _ in range(8):
            ratio = float(yogini.dhasa_adhipathi_list.get(lord, 0))
            if ratio <= 0:
                break
            duration_years = parent_duration_years * (ratio / total_cycle)
            end_dt = current_start + timedelta(days=duration_years * const.sidereal_year)
            period: Dict[str, Any] = {
                'planet': self._label_from_index(lord, self.PLANET_NAMES, 'Planet'),
                'start_date': self._format_datetime_output(current_start),
                'end_date': self._format_datetime_output(end_dt),
                'duration_years': duration_years,
                'planet_index': lord
            }
            child = self._build_yogini_subperiods(
                lord,
                current_start,
                duration_years,
                current_depth=current_depth + 1,
                max_depth=max_depth,
                total_cycle=total_cycle
            )
            if child:
                period['sub_periods'] = child
            sub_periods.append(period)
            if hasattr(yogini, '_next_adhipati') and callable(yogini._next_adhipati):
                lord = yogini._next_adhipati(lord)
            current_start = end_dt
        return sub_periods
    
    def _resolve_dhasa_callable(self, module, dhasa_type: str):
        """Find the appropriate calculation function within a dhasa module."""
        if module is None:
            return None
        
        candidates = [
            f'{dhasa_type}_dhasa_bhukthi',
            f'{dhasa_type}_dhasa_bhukti',
            f'get_{dhasa_type}_dhasa_bhukthi',
            f'get_{dhasa_type}_dhasa_bhukti',
            'get_dhasa_bhukthi',
            'get_dhasa_bhukti',
            'get_dhasa_antardhasa',
            'dhasa_bhukthi',
            'dhasa_bhukti',
        ]
        
        for name in candidates:
            if hasattr(module, name):
                attr = getattr(module, name)
                if callable(attr):
                    return attr
        
        # Fallback: search for any callable containing keywords
        for attr_name in dir(module):
            if any(keyword in attr_name.lower() for keyword in ['dhasa_bhuk', 'dhasa_antard', 'dhasa_bhukti']):
                attr = getattr(module, attr_name)
                if callable(attr):
                    return attr
        
        return None
    
    def _execute_dhasa_callable(self, func, birth_details: Dict[str, Any],
                                include_antardhasa: bool) -> Dict[str, Any]:
        """Execute the located callable with the correct parameters."""
        dob, tob, place = self._parse_birth_details(birth_details)
        jd = utils.julian_day_number(dob, tob)
        
        call_kwargs = {}
        signature = inspect.signature(func)
        birth_date_obj = datetime(dob[0], dob[1], dob[2])
        
        for name in signature.parameters:
            if name in {'dob', 'date_of_birth'}:
                call_kwargs[name] = dob
            elif name in {'tob', 'time_of_birth'}:
                call_kwargs[name] = tob
            elif name == 'dob_dt':
                call_kwargs[name] = birth_date_obj
            elif name == 'jd':
                call_kwargs[name] = jd
            elif name == 'place':
                call_kwargs[name] = place
            elif name in {'include_antardhasa', 'include_antardhasas'}:
                call_kwargs[name] = include_antardhasa
            elif name == 'birth_details':
                call_kwargs[name] = birth_details
            elif name == 'ayanamsa':
                call_kwargs[name] = birth_details.get('ayanamsa', 'LAHIRI')
        
        result = func(**call_kwargs) if call_kwargs else func()
        
        balance = None
        periods_raw = None
        if isinstance(result, tuple) and len(result) == 2 and isinstance(result[1], (list, tuple)):
            balance, periods_raw = result
        elif isinstance(result, (list, tuple)):
            periods_raw = result
        elif isinstance(result, dict) and 'periods' in result:
            periods_raw = result.get('periods')
            balance = result.get('balance')
        
        if isinstance(periods_raw, tuple):
            periods_raw = list(periods_raw)
        
        return {
            'periods_raw': list(periods_raw) if periods_raw else [],
            'balance': balance,
            'dob': dob,
            'tob': tob,
            'place': place,
            'jd': jd
        }
    
    def _format_periods_general(self, raw_periods, category: str) -> List[Dict[str, Any]]:
        if not raw_periods:
            return []
        
        first_entry = raw_periods[0]
        
        if isinstance(first_entry, dict):
            return raw_periods
        
        if isinstance(first_entry, (list, tuple)):
            string_like_count = sum(1 for value in first_entry if isinstance(value, str))
            has_nested = any(isinstance(value, (list, tuple)) and not isinstance(value, str) for value in first_entry[3:])
            if string_like_count >= 2 or has_nested:
                if category == 'raasi':
                    return self._format_raasi_dhasa_periods(raw_periods)
                return self._format_dhasa_periods(raw_periods)
            return self._format_flat_dhasa_periods(raw_periods, category)
        
        return []
    
    def _format_flat_dhasa_periods(self, raw_periods, category: str) -> List[Dict[str, Any]]:
        entries = []
        for row in raw_periods:
            parsed = self._parse_flat_period_row(row)
            if parsed:
                entries.append(parsed)
        
        if not entries:
            return []
        
        groups: List[Dict[str, Any]] = []
        for entry in entries:
            if not groups or groups[-1]['primary_index'] != entry['primary_index']:
                groups.append({'primary_index': entry['primary_index'], 'entries': []})
            groups[-1]['entries'].append(entry)
        
        names = self.PLANET_NAMES if category == 'graha' else self.RASI_NAMES
        fallback_label = 'Planet' if category == 'graha' else 'Rasi'
        formatted = []
        for idx, group in enumerate(groups):
            primary_key = group['primary_index']
            group_entries = [entry for entry in group['entries'] if entry['start'] is not None]
            if not group_entries:
                continue
            group_entries.sort(key=lambda item: item['start'])
            
            next_group_start = None
            if idx + 1 < len(groups):
                next_group_entries = [entry for entry in groups[idx + 1]['entries'] if entry['start'] is not None]
                if next_group_entries:
                    next_group_start = next_group_entries[0]['start']
            
            group_end = next_group_start or self._estimate_group_end(group_entries)
            group_label = self._label_from_index(primary_key, names, fallback_label)
            top_item = {
                'planet': group_label,
                'start_date': self._format_datetime_output(group_entries[0]['start']),
                'end_date': self._format_datetime_output(group_end) if group_end else '',
            }
            
            total_duration = sum(entry['duration_years'] for entry in group_entries if entry['duration_years'])
            if total_duration:
                top_item['duration_years'] = round(total_duration, 4)
            
            if category == 'graha':
                top_item['planet_index'] = self._safe_int(primary_key)
            else:
                top_item['rasi'] = group_label
                top_item['rasi_index'] = self._safe_int(primary_key)
            
            if any(entry['sub_index'] is not None for entry in group_entries):
                sub_periods = []
                for sub_idx, entry in enumerate(group_entries):
                    if entry['sub_index'] is None:
                        continue
                    sub_start = entry['start']
                    sub_end = None
                    if sub_idx + 1 < len(group_entries):
                        sub_end = group_entries[sub_idx + 1]['start']
                    elif group_end:
                        sub_end = group_end
                    elif entry['duration_years']:
                        sub_end = self._add_years(sub_start, entry['duration_years'])
                    
                    sub_periods.append({
                        'planet': self._label_from_index(entry['sub_index'], names, fallback_label),
                        'start_date': self._format_datetime_output(sub_start),
                        'end_date': self._format_datetime_output(sub_end) if sub_end else '',
                        'duration_years': entry['duration_years']
                    })
                if sub_periods:
                    top_item['sub_periods'] = sub_periods
            
            formatted.append(top_item)
        
        return formatted
    
    def _parse_flat_period_row(self, row) -> Optional[Dict[str, Any]]:
        if not isinstance(row, (list, tuple)) or not row:
            return None
        
        primary_index = self._safe_int(row[0])
        sub_index = None
        start_value = None
        duration_years = None
        
        for value in row[1:]:
            if isinstance(value, (list, tuple)) and not isinstance(value, str):
                # Nested structure - let other formatters handle the entire dataset
                return None
            if sub_index is None and isinstance(value, (int, float)):
                sub_index = int(value)
                continue
            parsed_date = self._parse_date_value(value)
            if start_value is None and parsed_date is not None:
                start_value = parsed_date
                continue
            if start_value is not None and duration_years is None and isinstance(value, (int, float)):
                duration_years = float(value)
        
        if start_value is None:
            return None
        
        return {
            'primary_index': primary_index,
            'sub_index': sub_index,
            'start': start_value,
            'duration_years': duration_years
        }
    
    def _parse_date_value(self, value) -> Optional[datetime]:
        if isinstance(value, datetime):
            return value
        
        if hasattr(value, 'year') and hasattr(value, 'month') and hasattr(value, 'day'):
            return datetime(value.year, value.month, value.day)
        
        if isinstance(value, str):
            cleaned = value.strip()
            if not cleaned:
                return None
            cleaned = cleaned.replace('/', '-')
            if 'T' not in cleaned and ' ' in cleaned:
                cleaned = cleaned.replace(' ', 'T', 1)
            try:
                return datetime.fromisoformat(cleaned)
            except ValueError:
                for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
                    try:
                        return datetime.strptime(cleaned, fmt)
                    except ValueError:
                        continue
        return None
    
    @staticmethod
    def _format_datetime_output(value: Optional[datetime]) -> str:
        if value is None:
            return ''
        return value.strftime('%Y-%m-%dT%H:%M:%S')
    
    @staticmethod
    def _label_from_index(index, names: List[str], fallback: str) -> str:
        idx = DhasaService._safe_int(index)
        if idx is not None and 0 <= idx < len(names):
            return names[idx]
        return f'{fallback}-{index}'
    
    @staticmethod
    def _safe_int(value) -> Optional[int]:
        try:
            return int(value)
        except (TypeError, ValueError):
            return None
    
    def _estimate_group_end(self, group_entries: List[Dict[str, Any]]) -> Optional[datetime]:
        if not group_entries:
            return None
        total_duration = sum(entry['duration_years'] for entry in group_entries if entry['duration_years'])
        if total_duration and group_entries[0]['start']:
            return self._add_years(group_entries[0]['start'], total_duration)
        last_entry = group_entries[-1]
        if last_entry['duration_years'] and last_entry['start']:
            return self._add_years(last_entry['start'], last_entry['duration_years'])
        return None
    
    def _add_years(self, start: datetime, years: float) -> datetime:
        return start + timedelta(days=years * self.DAYS_IN_YEAR)
    
    @staticmethod
    def _jd_to_datetime(jd: float) -> datetime:
        y, m, d, fractional_hours = utils.jd_to_gregorian(jd)
        return datetime(y, m, d) + timedelta(hours=fractional_hours)

