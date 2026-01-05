import { apiClient } from './client';
import { BirthDetails } from './charts';

export interface DhasaRequest {
  birth_details: BirthDetails;
  dhasa_type: string;
  include_antardhasa?: boolean;
  ayanamsa?: string;
  max_sub_level?: number;
  focus_mahadasha_index?: number;
}

export interface DhasaPeriod {
  planet: string; // or rasi
  planet_index?: number;
  start_date: string;
  end_date: string;
  duration_years?: number;
  sub_periods?: DhasaPeriod[];
}

export interface DhasaResponse {
  birth_details: BirthDetails;
  dhasa_type: string;
  balance_at_birth: any;
  periods: DhasaPeriod[];
}

const GRAHA_DHASAS = [
  'vimsottari', 'ashtottari', 'yogini', 'shodasottari', 'dwadasottari',
  'dwisatpathi', 'panchottari', 'sataatbika', 'chathuraaseethi_sama',
  'shastihayani', 'shattrimsa_sama', 'naisargika', 'tara', 'karaka', 'aayu'
];

const RAASI_DHASAS = [
  'narayana', 'kendradhi_rasi', 'sudasa', 'drig', 'nirayana', 'shoola',
  'chara', 'lagnamsaka', 'padhanadhamsa', 'mandooka', 'sthira', 'tara_lagna',
  'brahma', 'varnada', 'yogardha', 'navamsa', 'paryaaya', 'trikona',
  'kalachakra', 'moola', 'chakra'
];

export const dhasaApi = {
  calculateVimsottari: async (data: Omit<DhasaRequest, 'dhasa_type'>): Promise<DhasaResponse> => {
    const response = await apiClient.post<DhasaResponse>('/api/v1/dhasa/vimsottari', {
      ...data,
      dhasa_type: 'vimsottari'
    });
    return response.data;
  },

  calculateDhasa: async (data: DhasaRequest): Promise<DhasaResponse> => {
    const { dhasa_type, ...rest } = data;
    let category = 'graha';

    if (GRAHA_DHASAS.includes(dhasa_type)) {
      category = 'graha';
    } else if (RAASI_DHASAS.includes(dhasa_type)) {
      category = 'raasi';
    } else {
      // Default or Annual fallback
      category = 'graha';
    }

    const response = await apiClient.post<DhasaResponse>(`/api/v1/dhasa/${category}/${dhasa_type}`, data);
    return response.data;
  },

  getApplicableDhasas: async (data: Omit<DhasaRequest, 'dhasa_type'>) => {
    const response = await apiClient.post('/api/v1/dhasa/applicable', data);
    return response.data;
  },
};
