import { apiClient } from './client';

export interface City {
  country: string;
  name: string;
  latitude: number;
  longitude: number;
  timezone_name: string;
  timezone: number;
  is_usa?: boolean;
}

export interface AutocompleteResponse {
  usa: City[];
  international: City[];
  total: number;
  query: string;
}

export const citiesApi = {
  /**
   * Search cities (flat list, USA first)
   */
  search: async (query: string, limit: number = 20): Promise<City[]> => {
    const response = await apiClient.get<City[]>(`/api/v1/cities/search`, {
      params: { query, limit }
    });
    return response.data;
  },

  /**
   * Lookup city by exact name
   */
  lookup: async (cityName: string): Promise<City> => {
    const response = await apiClient.get<City>(`/api/v1/cities/lookup/${encodeURIComponent(cityName)}`);
    return response.data;
  },

  /**
   * Fast autocomplete with grouped results (USA / International)
   */
  autocomplete: async (q: string, limit: number = 10): Promise<AutocompleteResponse> => {
    const response = await apiClient.get<AutocompleteResponse>(`/api/v1/cities/autocomplete`, {
      params: { q, limit }
    });
    return response.data;
  },

  /**
   * Get city service statistics
   */
  getStats: async (): Promise<{ total_cities: number; usa_cities: number; world_cities: number; load_time_ms: number }> => {
    const response = await apiClient.get(`/api/v1/cities/stats`);
    return response.data;
  }
};
