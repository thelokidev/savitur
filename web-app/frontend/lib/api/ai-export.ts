import { apiClient } from './client';
import { BirthDetails } from './charts';

export interface AIExportRequest {
    birth_details: BirthDetails;
    format?: 'toon' | 'markdown' | 'json';
    sections?: string[];
}

export interface AIExportResponse {
    format: string;
    output: string;
    data?: Record<string, any>;
    chars: number;
    tokens_est: number;
    error?: string;
}

export const aiExportApi = {
    export: async (data: AIExportRequest): Promise<AIExportResponse> => {
        const response = await apiClient.post('/api/v1/ai-export/export', data);
        return response.data;
    },

    exportToon: async (data: AIExportRequest): Promise<AIExportResponse> => {
        const response = await apiClient.post('/api/v1/ai-export/toon', data);
        return response.data;
    },

    exportMarkdown: async (data: AIExportRequest): Promise<AIExportResponse> => {
        const response = await apiClient.post('/api/v1/ai-export/markdown', data);
        return response.data;
    },

    exportJson: async (data: AIExportRequest): Promise<AIExportResponse> => {
        const response = await apiClient.post('/api/v1/ai-export/json', data);
        return response.data;
    },
};

