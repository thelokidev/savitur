import { apiClient } from './client';
import { BirthDetails } from './charts';

export interface StrengthRequest {
    birth_details: BirthDetails;
    calculation_type: string;
    ayanamsa?: string;
}

export const strengthApi = {
    getShadbala: async (data: Omit<StrengthRequest, 'calculation_type'>) => {
        const response = await apiClient.post('/api/v1/strength/shadbala', {
            ...data,
            calculation_type: 'shadbala'
        });
        return response.data;
    },

    getAshtakavarga: async (data: Omit<StrengthRequest, 'calculation_type'>) => {
        const response = await apiClient.post('/api/v1/strength/ashtakavarga', {
            ...data,
            calculation_type: 'ashtakavarga'
        });
        return response.data;
    },

    getShodhayaPinda: async (data: Omit<StrengthRequest, 'calculation_type'>) => {
        const response = await apiClient.post('/api/v1/strength/shodhaya-pinda', {
            ...data,
            calculation_type: 'shodhaya_pinda'
        });
        return response.data;
    },

    getBhavaBala: async (data: Omit<StrengthRequest, 'calculation_type'>) => {
        const response = await apiClient.post('/api/v1/strength/bhava-bala', {
            ...data,
            calculation_type: 'bhava_bala'
        });
        return response.data;
    },

    getVimsopakaBala: async (data: Omit<StrengthRequest, 'calculation_type'>) => {
        const response = await apiClient.post('/api/v1/strength/vimsopaka-bala', {
            ...data,
            calculation_type: 'vimsopaka_bala'
        });
        return response.data;
    },

    getPanchaVargeeyaBala: async (data: Omit<StrengthRequest, 'calculation_type'>) => {
        const response = await apiClient.post('/api/v1/strength/pancha-vargeeya-bala', {
            ...data,
            calculation_type: 'pancha_vargeeya_bala'
        });
        return response.data;
    },

    getDwadasaVargeeyaBala: async (data: Omit<StrengthRequest, 'calculation_type'>) => {
        const response = await apiClient.post('/api/v1/strength/dwadasa-vargeeya-bala', {
            ...data,
            calculation_type: 'dwadasa_vargeeya_bala'
        });
        return response.data;
    },

    getHarshaBala: async (data: Omit<StrengthRequest, 'calculation_type'>) => {
        const response = await apiClient.post('/api/v1/strength/harsha-bala', {
            ...data,
            calculation_type: 'harsha_bala'
        });
        return response.data;
    },

    getIshtaKashtaPhala: async (data: Omit<StrengthRequest, 'calculation_type'>) => {
        const response = await apiClient.post('/api/v1/strength/ishta-kashta-phala', {
            ...data,
            calculation_type: 'ishta_kashta_phala'
        });
        return response.data;
    },

    getAllStrengths: async (data: Omit<StrengthRequest, 'calculation_type'>) => {
        const response = await apiClient.post('/api/v1/strength/all', {
            ...data,
            calculation_type: 'all'
        });
        return response.data;
    },

    getAllYogas: async (data: Omit<StrengthRequest, 'calculation_type'>, divisionalChart: number = 1) => {
        const response = await apiClient.post(`/api/v1/yogas/all-yogas?divisional_chart=${divisionalChart}`, {
            birth_details: data.birth_details,
            ayanamsa: data.ayanamsa || 'LAHIRI'
        });
        return response.data;
    },
};

