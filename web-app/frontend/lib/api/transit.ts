import { apiClient } from './client';
import { BirthDetails } from './charts';

export interface TransitRequest {
    birth_details: BirthDetails;
    transit_datetime?: string; // ISO datetime string
    reference?: 'lagna' | 'moon';
}

export interface PlanetPosition {
    planet: string;
    planet_index: number;
    longitude: number;
    rasi: number;
    rasi_name: string;
    rasi_short: string;
    degree: number;
    minute: number;
    degree_str: string;
    nakshatra: string;
    nakshatra_num: number;
    pada: number;
    nakshatra_pada: string;
    is_retrograde?: boolean;
    house_from_lagna?: number;
    house_from_moon?: number;
}

export interface TransitCurrentResponse {
    transit_date: string;
    transit_time: string;
    planets: Record<string, PlanetPosition>;
    error?: string;
}

export interface TransitOverlayResponse {
    birth_date: string;
    birth_time: string;
    transit_date: string;
    transit_time: string;
    natal_lagna_rasi: number;
    natal_lagna_name: string;
    natal_moon_rasi: number;
    natal_moon_name: string;
    natal_planets: Record<string, PlanetPosition>;
    transit_planets: Record<string, PlanetPosition>;
    error?: string;
}

export interface SignEntry {
    planet: string;
    planet_index: number;
    entering_rasi: number;
    entering_rasi_name: string;
    entry_date: string;
    entry_time: string;
    entry_datetime: string;
}

export interface SignEntriesResponse {
    from_date: string;
    entries: SignEntry[];
    error?: string;
}

export const transitApi = {
    getCurrentTransit: async (data: TransitRequest): Promise<TransitCurrentResponse> => {
        const response = await apiClient.post('/api/v1/transit/current', data);
        return response.data;
    },

    getTransitOverlay: async (data: TransitRequest): Promise<TransitOverlayResponse> => {
        const response = await apiClient.post('/api/v1/transit/overlay', data);
        return response.data;
    },

    getSignEntries: async (data: TransitRequest): Promise<SignEntriesResponse> => {
        const response = await apiClient.post('/api/v1/transit/entries', data);
        return response.data;
    },
};
