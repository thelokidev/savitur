'use client';

import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { strengthApi } from '@/lib/api/strength';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Loader2, Star, CheckCircle, Circle, AlertTriangle } from 'lucide-react';
import { BirthDetails } from '@/lib/api/charts';

interface StrengthTabProps {
    birthData: BirthDetails;
}

// Planet abbreviations for chart display
const PLANET_SHORT = ['Su', 'Mo', 'Ma', 'Me', 'Ju', 'Ve', 'Sa'];
const PLANET_NAMES = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'];

// Bar Chart Component - Black and White
interface BarChartProps {
    title: string;
    data: { label: string; value: number }[];
    maxValue?: number;
    unit?: string;
}

function BarChart({ title, data, maxValue, unit = '' }: BarChartProps) {
    const max = maxValue || Math.max(...data.map(d => d.value), 1);

    return (
        <Card className="border border-black/20 dark:border-white/20 h-full bg-white dark:bg-black">
            <CardHeader className="py-2 px-3 border-b border-black/10 dark:border-white/10">
                <CardTitle className="text-xs font-semibold text-black dark:text-white tracking-wide uppercase">
                    {title}
                </CardTitle>
            </CardHeader>
            <CardContent className="p-3">
                <div className="flex items-end justify-between gap-1.5 h-32">
                    {data.map((item, idx) => {
                        const heightPercent = (item.value / max) * 100;
                        return (
                            <div key={idx} className="flex flex-col items-center flex-1 h-full">
                                <span className="text-[10px] font-mono font-medium text-black dark:text-white mb-1">
                                    {item.value.toFixed(1)}{unit}
                                </span>
                                <div className="flex-1 w-full flex items-end justify-center">
                                    <div
                                        className="w-full max-w-[22px] transition-all duration-300 bg-black dark:bg-white"
                                        style={{
                                            height: `${Math.max(heightPercent, 3)}%`,
                                        }}
                                    />
                                </div>
                                <span className="text-[10px] font-semibold text-black/70 dark:text-white/70 mt-1.5 border-t border-black/20 dark:border-white/20 pt-1 w-full text-center">
                                    {item.label}
                                </span>
                            </div>
                        );
                    })}
                </div>
            </CardContent>
        </Card>
    );
}

// House Bar Chart Component (for Bhava Bala) - Black and White
interface HouseBarChartProps {
    title: string;
    data: { label: string; value: number }[];
}

function HouseBarChart({ title, data }: HouseBarChartProps) {
    const max = Math.max(...data.map(d => d.value), 1);

    return (
        <Card className="border border-black/20 dark:border-white/20 bg-white dark:bg-black">
            <CardHeader className="py-2 px-3 border-b border-black/10 dark:border-white/10">
                <CardTitle className="text-xs font-semibold text-black dark:text-white tracking-wide uppercase">
                    {title}
                </CardTitle>
            </CardHeader>
            <CardContent className="p-3">
                <div className="flex items-end justify-between gap-0.5 h-28">
                    {data.map((item, idx) => {
                        const heightPercent = (item.value / max) * 100;
                        return (
                            <div key={idx} className="flex flex-col items-center flex-1 h-full">
                                <span className="text-[8px] font-mono font-medium text-black dark:text-white mb-0.5">
                                    {item.value.toFixed(0)}
                                </span>
                                <div className="flex-1 w-full flex items-end justify-center">
                                    <div
                                        className="w-full max-w-[16px] transition-all duration-300 bg-black dark:bg-white"
                                        style={{
                                            height: `${Math.max(heightPercent, 3)}%`,
                                        }}
                                    />
                                </div>
                                <span className="text-[8px] font-semibold text-black/70 dark:text-white/70 mt-1 border-t border-black/20 dark:border-white/20 pt-0.5 w-full text-center">
                                    {item.label}
                                </span>
                            </div>
                        );
                    })}
                </div>
            </CardContent>
        </Card>
    );
}

// Yoga Section Component
interface YogaSectionProps {
    yogaData: any;
    isLoading: boolean;
}

function YogaSection({ yogaData, isLoading }: YogaSectionProps) {
    if (isLoading) {
        return (
            <Card className="border border-black/20 dark:border-white/20 bg-white dark:bg-black">
                <CardHeader className="py-2 px-3 border-b border-black/10 dark:border-white/10">
                    <CardTitle className="text-xs font-semibold text-black dark:text-white tracking-wide uppercase">
                        Yogas
                    </CardTitle>
                </CardHeader>
                <CardContent className="p-3">
                    <div className="flex items-center justify-center gap-2 py-4">
                        <Loader2 className="w-4 h-4 animate-spin text-black/50 dark:text-white/50" />
                        <span className="text-xs text-black/50 dark:text-white/50">Loading yogas...</span>
                    </div>
                </CardContent>
            </Card>
        );
    }

    const allYogas = yogaData?.all_yogas || [];
    const rajaYogas = yogaData?.raja_yogas || [];
    const totalYogas = yogaData?.total_yogas || 0;
    const chartStrength = yogaData?.chart_strength || {};
    const yogasByCategory = yogaData?.yogas_by_category || {};

    // Get yogas by category (these are arrays of yoga objects)
    const excellent = yogasByCategory.excellent || [];
    const good = yogasByCategory.good || [];
    const neutral = yogasByCategory.neutral || [];
    const inauspicious = yogasByCategory.inauspicious || [];

    const hasYogas = totalYogas > 0 || rajaYogas.length > 0;

    return (
        <Card className="border border-black/20 dark:border-white/20 bg-white dark:bg-black">
            <CardHeader className="py-2 px-3 border-b border-black/10 dark:border-white/10">
                <div className="flex items-center justify-between">
                    <CardTitle className="text-xs font-semibold text-black dark:text-white tracking-wide uppercase">
                        Yogas ({totalYogas + rajaYogas.length} found)
                    </CardTitle>
                    {chartStrength.rating && (
                        <span className="text-[10px] font-medium px-2 py-0.5 rounded bg-black/10 dark:bg-white/10 text-black/70 dark:text-white/70">
                            {chartStrength.rating}
                        </span>
                    )}
                </div>
            </CardHeader>
            <CardContent className="p-3">
                {!hasYogas ? (
                    <p className="text-xs text-black/50 dark:text-white/50 text-center py-4">
                        No significant yogas detected in this chart
                    </p>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
                        {/* Excellent Yogas */}
                        <div className="space-y-1.5">
                            <div className="flex items-center gap-1.5 text-xs font-semibold text-black dark:text-white">
                                <Star className="w-3 h-3" />
                                <span>Excellent ({excellent.length})</span>
                            </div>
                            <div className="space-y-1 max-h-40 overflow-y-auto">
                                {excellent.length === 0 ? (
                                    <p className="text-[10px] text-black/40 dark:text-white/40 italic">None</p>
                                ) : (
                                    excellent.map((yoga: any, idx: number) => (
                                        <div key={idx} className="text-[10px] text-black/70 dark:text-white/70 pl-4">
                                            • {yoga.name || yoga}
                                        </div>
                                    ))
                                )}
                            </div>
                        </div>

                        {/* Good Yogas */}
                        <div className="space-y-1.5">
                            <div className="flex items-center gap-1.5 text-xs font-semibold text-black dark:text-white">
                                <CheckCircle className="w-3 h-3" />
                                <span>Good ({good.length})</span>
                            </div>
                            <div className="space-y-1 max-h-40 overflow-y-auto">
                                {good.length === 0 ? (
                                    <p className="text-[10px] text-black/40 dark:text-white/40 italic">None</p>
                                ) : (
                                    good.map((yoga: any, idx: number) => (
                                        <div key={idx} className="text-[10px] text-black/70 dark:text-white/70 pl-4">
                                            • {yoga.name || yoga}
                                        </div>
                                    ))
                                )}
                            </div>
                        </div>

                        {/* Neutral Yogas */}
                        <div className="space-y-1.5">
                            <div className="flex items-center gap-1.5 text-xs font-semibold text-black dark:text-white">
                                <Circle className="w-3 h-3" />
                                <span>Neutral ({neutral.length})</span>
                            </div>
                            <div className="space-y-1 max-h-40 overflow-y-auto">
                                {neutral.length === 0 ? (
                                    <p className="text-[10px] text-black/40 dark:text-white/40 italic">None</p>
                                ) : (
                                    neutral.map((yoga: any, idx: number) => (
                                        <div key={idx} className="text-[10px] text-black/70 dark:text-white/70 pl-4">
                                            • {yoga.name || yoga}
                                        </div>
                                    ))
                                )}
                            </div>
                        </div>

                        {/* Inauspicious Yogas */}
                        <div className="space-y-1.5">
                            <div className="flex items-center gap-1.5 text-xs font-semibold text-black dark:text-white">
                                <AlertTriangle className="w-3 h-3" />
                                <span>Challenging ({inauspicious.length})</span>
                            </div>
                            <div className="space-y-1 max-h-40 overflow-y-auto">
                                {inauspicious.length === 0 ? (
                                    <p className="text-[10px] text-black/40 dark:text-white/40 italic">None</p>
                                ) : (
                                    inauspicious.map((yoga: any, idx: number) => (
                                        <div key={idx} className="text-[10px] text-black/70 dark:text-white/70 pl-4">
                                            • {yoga.name || yoga}
                                        </div>
                                    ))
                                )}
                            </div>
                        </div>
                    </div>
                )}

                {/* Raja Yogas Section */}
                {rajaYogas.length > 0 && (
                    <div className="mt-3 pt-3 border-t border-black/10 dark:border-white/10">
                        <div className="flex items-center gap-1.5 text-xs font-semibold text-black dark:text-white mb-2">
                            <Star className="w-3 h-3 fill-current" />
                            <span>Raja Yogas ({rajaYogas.length})</span>
                        </div>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                            {rajaYogas.map((yoga: any, idx: number) => (
                                <div key={idx} className="text-[10px] text-black/70 dark:text-white/70 bg-black/5 dark:bg-white/5 rounded px-2 py-1">
                                    <span className="font-medium">{yoga.name || yoga}</span>
                                    {yoga.description && (
                                        <span className="block text-black/50 dark:text-white/50 mt-0.5">
                                            {yoga.description}
                                        </span>
                                    )}
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </CardContent>
        </Card>
    );
}

// Loading skeleton component - Black and White
function LoadingSkeleton() {
    return (
        <div className="flex flex-col items-center justify-center h-full gap-3">
            <Loader2 className="w-6 h-6 animate-spin text-black dark:text-white" />
            <span className="text-sm text-black/60 dark:text-white/60">Calculating strength metrics...</span>
        </div>
    );
}

// Helper to extract planet data from various formats
function extractPlanetData(data: any, valueKey?: string): { label: string; value: number }[] {
    return PLANET_NAMES.map((planet, idx) => {
        let value = 0;
        if (data && data[planet] !== undefined) {
            value = valueKey ? (data[planet]?.[valueKey] ?? 0) : (typeof data[planet] === 'number' ? data[planet] : 0);
        }
        return { label: PLANET_SHORT[idx], value: Number(value) || 0 };
    });
}

export function StrengthTab({ birthData }: StrengthTabProps) {
    const birthDetailsReady = Boolean(
        birthData.date && birthData.time && birthData.place?.name && typeof birthData.place.latitude === 'number'
    );

    const requestData = { birth_details: birthData, ayanamsa: birthData.ayanamsa };

    // Single query for all strength data
    const { data, isLoading, isError, error } = useQuery({
        queryKey: ['all-strengths', birthData.date, birthData.time, birthData.place?.latitude, birthData.place?.longitude, birthData.ayanamsa],
        queryFn: () => strengthApi.getAllStrengths(requestData),
        enabled: birthDetailsReady,
        refetchOnWindowFocus: false,
    });

    // Query for yoga data
    const { data: yogaData, isLoading: yogaLoading } = useQuery({
        queryKey: ['all-yogas', birthData.date, birthData.time, birthData.place?.latitude, birthData.place?.longitude, birthData.ayanamsa],
        queryFn: () => strengthApi.getAllYogas(requestData),
        enabled: birthDetailsReady,
        refetchOnWindowFocus: false,
    });

    if (!birthDetailsReady) {
        return (
            <div className="flex items-center justify-center h-full text-sm text-black/50 dark:text-white/50 p-4 text-center">
                Enter birth details to view strength calculations
            </div>
        );
    }

    if (isLoading) {
        return <LoadingSkeleton />;
    }

    if (isError) {
        return (
            <div className="flex items-center justify-center h-full text-sm text-black dark:text-white p-4 text-center">
                Error loading strength data: {(error as Error)?.message || 'Unknown error'}
            </div>
        );
    }

    // Extract data for charts
    const shadbalaPercent = extractPlanetData(data?.shadbala?.planets, 'percent_strength');
    const vimsopakaDasa = extractPlanetData(data?.vimsopaka_bala?.dhasavarga);
    const ishtaPhala = extractPlanetData(data?.ishta_kashta_phala?.ishta_phala);
    const panchaVargeeya = extractPlanetData(data?.pancha_vargeeya_bala?.planets);
    const dwadhasaVargeeya = extractPlanetData(data?.dwadhasa_vargeeya_bala?.planets);
    const harshaBala = extractPlanetData(data?.harsha_bala?.planets);

    // Bhava Bala data (12 houses)
    const bhavaData = Array.from({ length: 12 }, (_, i) => {
        const house = data?.bhava_bala?.houses?.[`House_${i + 1}`];
        return {
            label: `${i + 1}`,
            value: house?.total_rupas ?? 0,
        };
    });

    return (
        <div className="h-full flex flex-col overflow-hidden">
            <div className="flex-1 overflow-y-auto p-3">
                {/* First Row: 3 charts */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mb-3">
                    <BarChart
                        title="Shadbala (% Strength)"
                        data={shadbalaPercent}
                        unit="%"
                    />
                    <BarChart
                        title="Vimsopaka Bala (Dasa)"
                        data={vimsopakaDasa}
                        maxValue={20}
                    />
                    <BarChart
                        title="Ishta Phala"
                        data={ishtaPhala}
                        maxValue={60}
                    />
                </div>

                {/* Second Row: 3 charts */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mb-3">
                    <BarChart
                        title="Pancha Vargeeya Bala"
                        data={panchaVargeeya}
                    />
                    <BarChart
                        title="Dwadhasa Vargeeya Bala"
                        data={dwadhasaVargeeya}
                        maxValue={12}
                    />
                    <BarChart
                        title="Harsha Bala"
                        data={harshaBala}
                        maxValue={25}
                    />
                </div>

                {/* Third Row: Bhava Bala (full width) */}
                <div className="grid grid-cols-1 gap-3 mb-3">
                    <HouseBarChart
                        title="Bhava Bala (Rupas) - Houses 1-12"
                        data={bhavaData}
                    />
                </div>

                {/* Fourth Row: Yogas (full width) */}
                <div className="grid grid-cols-1 gap-3">
                    <YogaSection yogaData={yogaData} isLoading={yogaLoading} />
                </div>
            </div>
        </div>
    );
}

