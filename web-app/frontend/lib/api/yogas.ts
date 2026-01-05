import { apiClient } from './client';
import { BirthDetails } from './charts';

export interface YogaRequest {
  birth_details: BirthDetails;
  ayanamsa?: string;
}

export interface YogaItem {
  name: string;
  description: string;
  category?: string;
  quality?: string;
  strength?: string;
  impact?: string;
  score?: number;
  planet?: string;
  planets?: string[];
}

export interface YogaSummary {
  excellent: number;
  good: number;
  neutral: number;
  inauspicious: number;
}

export interface ChartStrength {
  total_score: number;
  average_score: number;
  rating: string;
}

export interface YogaResponse {
  birth_date: string;
  birth_time: string;
  divisional_chart: string;
  total_yogas: number;
  yogas?: YogaItem[];
  yoga_summary?: YogaSummary;
  chart_strength?: ChartStrength;
  yogas_by_category?: {
    excellent: YogaItem[];
    good: YogaItem[];
    neutral: YogaItem[];
    inauspicious: YogaItem[];
  };
  all_yogas?: YogaItem[];
  raja_yogas: YogaItem[];
  doshas: any[];
}

export const yogasApi = {
  getAllYogasAndDoshas: async (data: YogaRequest, divisionalChart: number = 1): Promise<YogaResponse> => {
    console.log('DEBUG: API Call getAllYogasAndDoshas:', data);
    const response = await apiClient.post<YogaResponse>(
      `/api/v1/yogas/all-yogas?divisional_chart=${divisionalChart}`,
      data
    );
    return response.data;
  },

  getAllDoshas: async (data: YogaRequest) => {
    const response = await apiClient.post('/api/v1/yogas/all-doshas', data);
    return response.data;
  },
};


