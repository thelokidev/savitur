import { apiClient } from './client';
import { BirthDetails } from './charts';

export interface CompatibilityRequest {
  boy: BirthDetails;
  girl: BirthDetails;
  compatibility_type: string;
  ayanamsa?: string;
}

export interface CompatibilityScore {
  name: string;
  score: number;
  max_score: number;
  description: string;
  compatible: boolean;
}

export interface CompatibilityResponse {
  boy: BirthDetails;
  girl: BirthDetails;
  compatibility_type: string;
  total_score: number;
  max_score: number;
  percentage: number;
  compatible: boolean;
  factors: CompatibilityScore[];
  recommendation: string;
}

export const compatibilityApi = {
  getNorthIndian: async (data: Omit<CompatibilityRequest, 'compatibility_type'>): Promise<CompatibilityResponse> => {
    const response = await apiClient.post<CompatibilityResponse>('/api/v1/compatibility/north-indian', {
      ...data,
      compatibility_type: 'north'
    });
    return response.data;
  },

  getSouthIndian: async (data: Omit<CompatibilityRequest, 'compatibility_type'>): Promise<CompatibilityResponse> => {
    const response = await apiClient.post<CompatibilityResponse>('/api/v1/compatibility/south-indian', {
      ...data,
      compatibility_type: 'south'
    });
    return response.data;
  },

  getBothMethods: async (data: Omit<CompatibilityRequest, 'compatibility_type'>) => {
    const response = await apiClient.post('/api/v1/compatibility/both-methods', data);
    return response.data;
  },
};


