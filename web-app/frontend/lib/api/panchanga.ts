import { apiClient } from './client';

export interface Place {
  name: string;
  latitude: number;
  longitude: number;
  timezone: number;
}

export interface PanchangaRequest {
  date: string;
  time: string;
  place: Place;
  ayanamsa?: string;
}

export interface PanchangaResponse {
  place: Place;
  date: string;
  time: string;
  julian_day: number;
  sunrise: string;
  sunset: string;
  moonrise?: string;
  moonset?: string;
  tithi: {
    number: number;
    name: string;
    paksha: string;
    end_time?: string;
  };
  nakshatra: {
    number: number;
    name: string;
    pada: number;
    lord: string;
    end_time?: string;
  };
  yoga: {
    number: number;
    name: string;
    end_time?: string;
  };
  karana: {
    number: number;
    name: string;
    lord: string;
    start_time?: string;
    end_time?: string;
  };
  tithi_details?: {
    deity?: string;
    lord?: string;
  };
  nakshatra_details?: {
    deity?: string;
  };
  yoga_details?: {
    quality?: string;
  };
  karana_details?: {
    lord?: string;
  };
  vaara: string;
  rahu_kala: {
    start: string;
    end: string;
  };
  yamaganda: {
    start: string;
    end: string;
  };
  gulika: {
    start: string;
    end: string;
  };
  abhijit_muhurta?: {
    start: string;
    end: string;
  };
  ayanamsa_value: number;
  sidereal_time?: string;
  hora_lord?: string;
}

export const panchangaApi = {
  calculate: async (data: PanchangaRequest): Promise<PanchangaResponse> => {
    const response = await apiClient.post<PanchangaResponse>('/api/v1/panchanga/calculate', data);
    return response.data;
  },

  getPlanetPositions: async (data: PanchangaRequest) => {
    const response = await apiClient.post('/api/v1/panchanga/planets', data);
    return response.data;
  },

  getPlanets: async (data: PanchangaRequest) => {
    const response = await apiClient.post('/api/v1/panchanga/planets', data);
    return response.data;
  },

  getMuhurtha: async (data: PanchangaRequest) => {
    const response = await apiClient.post('/api/v1/panchanga/muhurtha', data);
    return response.data;
  },

  getExtended: async (data: PanchangaRequest) => {
    const response = await apiClient.post('/api/v1/panchanga/extended', data);
    return response.data;
  },

  getEclipses: async (data: PanchangaRequest) => {
    const response = await apiClient.post('/api/v1/panchanga/eclipses', data);
    return response.data;
  },

  getSankranti: async (data: PanchangaRequest) => {
    const response = await apiClient.post('/api/v1/panchanga/sankranti', data);
    return response.data;
  },

  getRetrograde: async (data: PanchangaRequest) => {
    const response = await apiClient.post('/api/v1/panchanga/retrograde', data);
    return response.data;
  },

  getUdhayaLagna: async (data: PanchangaRequest) => {
    const response = await apiClient.post('/api/v1/panchanga/udhaya-lagna', data);
    return response.data;
  },

  getConjunctions: async (data: PanchangaRequest & { planet1: number; planet2: number }) => {
    const response = await apiClient.post('/api/v1/panchanga/conjunctions', data);
    return response.data;
  },
};


