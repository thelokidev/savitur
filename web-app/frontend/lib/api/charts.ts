import { apiClient } from './client';
import { Place } from './panchanga';

export interface BirthDetails {
  name?: string;
  date: string;
  time: string;
  place: Place;
  ayanamsa?: string;
}

export interface ChartRequest {
  birth_details: BirthDetails;
  ayanamsa?: string;
}

export interface PlanetPosition {
  name: string;
  rasi: number;
  rasi_name: string;
  longitude: number;
  degrees_in_rasi: number;
  nakshatra?: number;
  nakshatra_name?: string;
  retrograde?: boolean;
}

export interface ChartResponse {
  chart_type: string;
  divisional_factor: number;
  julian_day: number;
  ayanamsa: string;
  ascendant: PlanetPosition;
  planets: PlanetPosition[];
  houses: { [key: number]: string[] };
  // Optional enrichments returned by Rasi chart endpoint
  special_lagnas?: PlanetPosition[];
  upagrahas?: PlanetPosition[];
}

export const chartsApi = {
  getRasiChart: async (data: ChartRequest): Promise<ChartResponse> => {
    console.log('DEBUG: API Call getRasiChart:', data);
    const response = await apiClient.post<ChartResponse>('/api/v1/charts/rasi', data);
    return response.data;
  },

  getDivisionalChart: async (varga: number, data: ChartRequest): Promise<ChartResponse> => {
    const response = await apiClient.post<ChartResponse>(`/api/v1/charts/divisional/${varga}`, data);
    return response.data;
  },

  getSpecialLagnas: async (data: ChartRequest) => {
    const response = await apiClient.post('/api/v1/charts/special-lagnas', data);
    return response.data;
  },

  getUpagrahas: async (data: ChartRequest) => {
    const response = await apiClient.post('/api/v1/charts/upagrahas', data);
    return response.data;
  },

  getArudhaPadas: async (data: ChartRequest) => {
    const response = await apiClient.post('/api/v1/charts/arudha-padas', data);
    return response.data;
  },
};


