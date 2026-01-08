import { apiClient } from './client';

export interface ConsolidatedRequest {
    date: string;
    time: string;
    place: {
        name: string;
        latitude: number;
        longitude: number;
        timezone: number;
    };
    ayanamsa?: string;
}

export interface ConsolidatedResponse {
    panchanga: any;
    extended: any;
    charts: {
        rasi: any;
        navamsa: any;
    };
    ashtakavarga: any;
}

export const consolidatedApi = {
    /**
     * Get ALL chart data in a single request
     * This is much faster than making 12+ individual API calls
     */
    calculateAll: async (request: ConsolidatedRequest): Promise<ConsolidatedResponse> => {
        const response = await apiClient.post<ConsolidatedResponse>('/api/v1/calculate-all', request);
        return response.data;
    },
};
