'use client';

import React, { useState, useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import { transitApi, TransitOverlayResponse, SignEntriesResponse } from '@/lib/api/transit';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Loader2, ChevronLeft, ChevronRight, Calendar } from 'lucide-react';
import { BirthDetails } from '@/lib/api/charts';
import { format, addDays, subDays } from 'date-fns';

interface TransitTabProps {
    birthData: BirthDetails;
}

const PLANET_ORDER = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu'];
const RASI_SHORT = ['Ari', 'Tau', 'Gem', 'Can', 'Leo', 'Vir', 'Lib', 'Sco', 'Sag', 'Cap', 'Aqu', 'Pis'];

// Simple South Indian Chart SVG component
function MiniChart({
    planets,
    lagnaRasi,
    title,
    isTransit = false
}: {
    planets: Record<string, { rasi: number; is_retrograde?: boolean }>;
    lagnaRasi: number;
    title: string;
    isTransit?: boolean;
}) {
    // House positions in South Indian style (fixed signs)
    const housePositions: Record<number, { x: number; y: number }> = {
        11: { x: 0, y: 0 }, 0: { x: 1, y: 0 }, 1: { x: 2, y: 0 }, 2: { x: 3, y: 0 },
        10: { x: 0, y: 1 }, 3: { x: 3, y: 1 },
        9: { x: 0, y: 2 }, 4: { x: 3, y: 2 },
        8: { x: 0, y: 3 }, 7: { x: 1, y: 3 }, 6: { x: 2, y: 3 }, 5: { x: 3, y: 3 },
    };

    // Group planets by rasi
    const planetsByRasi: Record<number, string[]> = {};
    Object.entries(planets).forEach(([name, data]) => {
        const rasi = data.rasi;
        if (!planetsByRasi[rasi]) planetsByRasi[rasi] = [];
        const symbol = name.substring(0, 2);
        const displayName = data.is_retrograde ? `(${symbol})` : symbol;
        planetsByRasi[rasi].push(displayName);
    });

    // Doubled cell size for "much bigger" charts (was 40)
    const cellSize = 80;
    const width = cellSize * 4;
    const height = cellSize * 4;

    return (
        <div className="flex flex-col items-center">
            <span className="text-sm font-bold text-black/70 dark:text-white/70 mb-3 uppercase tracking-wider">
                {title}
            </span>
            <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`} className="border-2 border-black/30 dark:border-white/30 text-black dark:text-white bg-white dark:bg-black shadow-sm">
                {/* Background */}
                <rect width={width} height={height} className="fill-white dark:fill-black" />

                {/* Grid lines */}
                {[1, 2, 3].map(i => (
                    <React.Fragment key={i}>
                        <line x1={i * cellSize} y1={0} x2={i * cellSize} y2={height} stroke="currentColor" strokeWidth="1" className="opacity-30" />
                        <line x1={0} y1={i * cellSize} x2={width} y2={i * cellSize} stroke="currentColor" strokeWidth="1" className="opacity-30" />
                    </React.Fragment>
                ))}

                {/* Center box (empty in South Indian) */}
                <rect x={cellSize} y={cellSize} width={cellSize * 2} height={cellSize * 2} className="fill-white dark:fill-black stroke-current opacity-30" strokeWidth="1" />

                {/* Rasi numbers and planets */}
                {Object.entries(housePositions).map(([rasiStr, pos]) => {
                    const rasi = parseInt(rasiStr);
                    const isLagna = rasi === lagnaRasi;
                    const planetsInRasi = planetsByRasi[rasi] || [];
                    const x = pos.x * cellSize;
                    const y = pos.y * cellSize;

                    return (
                        <g key={rasi}>
                            {/* Rasi short name - Larger font */}
                            <text
                                x={x + 6}
                                y={y + 18}
                                fontSize="14"
                                className={`font-bold uppercase opacity-60 fill-current ${isLagna ? "text-primary opacity-100" : ""}`}
                                fill={isLagna ? "var(--primary)" : "currentColor"}
                            >
                                {RASI_SHORT[rasi]}
                            </text>

                            {/* Lagna marker - Much clearer */}
                            {isLagna && (
                                <text x={x + cellSize - 20} y={y + 18} fontSize="14" fontWeight="bold" fill="var(--primary)" className="fill-primary">
                                    As
                                </text>
                            )}

                            {/* Planets - Grid layout for better fit with large size */}
                            <foreignObject x={x} y={y + 24} width={cellSize} height={cellSize - 24}>
                                <div className="w-full h-full p-1 flex flex-wrap content-start items-center justify-center gap-x-2 gap-y-0.5 pointer-events-none">
                                    {planetsInRasi.map((planet, idx) => (
                                        <span
                                            key={idx}
                                            className="text-[13px] font-medium leading-tight text-black dark:text-white"
                                        >
                                            {planet}
                                        </span>
                                    ))}
                                </div>
                            </foreignObject>
                        </g>
                    );
                })}
            </svg>
        </div>
    );
}

export function TransitTab({ birthData }: TransitTabProps) {
    const [transitDate, setTransitDate] = useState(() => format(new Date(), 'yyyy-MM-dd'));
    const [transitTime, setTransitTime] = useState(() => format(new Date(), 'HH:mm'));

    const birthDetailsReady = Boolean(
        birthData.date && birthData.time && birthData.place?.name && typeof birthData.place.latitude === 'number'
    );

    const transitDatetime = `${transitDate}T${transitTime}:00`;

    // Fetch transit overlay data
    const { data: overlayData, isLoading: overlayLoading, error: overlayError } = useQuery({
        queryKey: ['transit-overlay', birthData.date, birthData.time, birthData.place?.latitude, birthData.place?.longitude, birthData.ayanamsa, transitDatetime],
        queryFn: () => transitApi.getTransitOverlay({
            birth_details: birthData,
            transit_datetime: transitDatetime
        }),
        enabled: birthDetailsReady,
        refetchOnWindowFocus: false,
    });

    // Fetch sign entries
    const { data: entriesData, isLoading: entriesLoading } = useQuery({
        queryKey: ['transit-entries', birthData.date, birthData.time, birthData.place?.latitude, birthData.place?.longitude, birthData.ayanamsa, transitDatetime],
        queryFn: () => transitApi.getSignEntries({
            birth_details: birthData,
            transit_datetime: transitDatetime,
        }),
        enabled: birthDetailsReady,
        refetchOnWindowFocus: false,
    });

    const handlePrevDay = () => {
        const d = new Date(transitDate);
        setTransitDate(format(subDays(d, 1), 'yyyy-MM-dd'));
    };

    const handleNextDay = () => {
        const d = new Date(transitDate);
        setTransitDate(format(addDays(d, 1), 'yyyy-MM-dd'));
    };

    const handleToday = () => {
        setTransitDate(format(new Date(), 'yyyy-MM-dd'));
        setTransitTime(format(new Date(), 'HH:mm'));
    };

    if (!birthDetailsReady) {
        return (
            <div className="flex items-center justify-center h-full text-sm text-black/50 dark:text-white/50 p-4 text-center">
                Enter birth details to view transit positions
            </div>
        );
    }

    if (overlayLoading) {
        return (
            <div className="flex flex-col items-center justify-center h-full gap-3">
                <Loader2 className="w-6 h-6 animate-spin text-black dark:text-white" />
                <span className="text-sm text-black/60 dark:text-white/60">Calculating transits...</span>
            </div>
        );
    }

    if (overlayError || overlayData?.error) {
        return (
            <div className="flex items-center justify-center h-full text-sm text-black dark:text-white p-4 text-center">
                Error: {overlayData?.error || (overlayError as Error)?.message || 'Unknown error'}
            </div>
        );
    }

    const transitPlanets = overlayData?.transit_planets || {};
    const natalPlanets = overlayData?.natal_planets || {};
    const natalLagnaRasi = overlayData?.natal_lagna_rasi ?? 0;
    const natalMoonRasi = overlayData?.natal_moon_rasi ?? 0;

    return (
        <div className="h-full flex flex-col overflow-hidden">
            <div className="flex-1 overflow-y-auto p-3 space-y-3">

                {/* Date/Time Controls */}
                <Card className="border border-black/20 dark:border-white/20 bg-white dark:bg-black">
                    <CardContent className="p-3">
                        <div className="flex flex-wrap items-center gap-3">
                            {/* Date Input */}
                            <div className="flex items-center gap-2">
                                <label className="text-xs font-medium text-black/70 dark:text-white/70">Date:</label>
                                <input
                                    type="date"
                                    value={transitDate}
                                    onChange={(e) => setTransitDate(e.target.value)}
                                    className="h-7 text-xs border border-black/20 dark:border-white/20 bg-white dark:bg-black text-black dark:text-white rounded px-2"
                                />
                            </div>

                            {/* Time Input */}
                            <div className="flex items-center gap-2">
                                <label className="text-xs font-medium text-black/70 dark:text-white/70">Time:</label>
                                <input
                                    type="time"
                                    value={transitTime}
                                    onChange={(e) => setTransitTime(e.target.value)}
                                    className="h-7 text-xs border border-black/20 dark:border-white/20 bg-white dark:bg-black text-black dark:text-white rounded px-2"
                                />
                            </div>

                            {/* Navigation Buttons */}
                            <div className="flex items-center gap-1">
                                <button
                                    onClick={handlePrevDay}
                                    className="h-7 px-2 text-xs border border-black/20 dark:border-white/20 rounded hover:bg-black/5 dark:hover:bg-white/5 flex items-center"
                                    title="Previous Day"
                                >
                                    <ChevronLeft className="w-3 h-3" />
                                </button>
                                <button
                                    onClick={handleToday}
                                    className="h-7 px-3 text-xs border border-black/20 dark:border-white/20 rounded hover:bg-black/5 dark:hover:bg-white/5 font-medium"
                                >
                                    Today
                                </button>
                                <button
                                    onClick={handleNextDay}
                                    className="h-7 px-2 text-xs border border-black/20 dark:border-white/20 rounded hover:bg-black/5 dark:hover:bg-white/5 flex items-center"
                                    title="Next Day"
                                >
                                    <ChevronRight className="w-3 h-3" />
                                </button>
                            </div>
                        </div>
                    </CardContent>
                </Card>

                {/* Side-by-Side Charts - Enlarged */}
                <Card className="border border-black/20 dark:border-white/20 bg-white dark:bg-black w-full">
                    <CardContent className="p-8">
                        <div className="flex flex-col xl:flex-row justify-center items-center gap-12 xl:gap-20">
                            <div className="origin-center">
                                <MiniChart
                                    planets={natalPlanets}
                                    lagnaRasi={natalLagnaRasi}
                                    title="Natal Chart"
                                />
                            </div>
                            <div className="origin-center">
                                <MiniChart
                                    planets={transitPlanets}
                                    lagnaRasi={natalLagnaRasi}
                                    title={`Transit ${overlayData?.transit_date || ''}`}
                                    isTransit
                                />
                            </div>
                        </div>
                    </CardContent>
                </Card>

                {/* Side-by-Side Tables Grid */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                    {/* Transit Positions Table */}
                    <Card className="border border-black/20 dark:border-white/20 bg-white dark:bg-black h-full flex flex-col">
                        <CardHeader className="py-3 px-4 border-b border-black/10 dark:border-white/10 bg-black/5 dark:bg-white/5">
                            <CardTitle className="text-sm font-bold text-black dark:text-white tracking-wide uppercase flex items-center gap-2">
                                <span className="w-1.5 h-4 bg-primary rounded-sm"></span>
                                Transit Positions
                            </CardTitle>
                        </CardHeader>
                        <CardContent className="p-0 flex-1">
                            <div className="overflow-x-auto">
                                <table className="w-full text-xs">
                                    <thead>
                                        <tr className="border-b border-black/10 dark:border-white/10">
                                            <th className="text-left font-semibold p-3 text-muted-foreground w-1/4">Planet</th>
                                            <th className="text-left font-semibold p-3 text-muted-foreground w-1/4">Sign</th>
                                            <th className="text-right font-semibold p-3 text-muted-foreground">Deg</th>
                                            <th className="text-right font-semibold p-3 text-muted-foreground">Nakshatra</th>
                                        </tr>
                                    </thead>
                                    <tbody className="divide-y divide-border/50">
                                        {PLANET_ORDER.map((planetName) => {
                                            const planet = transitPlanets[planetName];
                                            if (!planet) return null;
                                            return (
                                                <tr key={planetName} className="hover:bg-muted/30 transition-colors">
                                                    <td className="p-3 font-medium flex items-center gap-2">
                                                        {planetName}
                                                        {planet.is_retrograde && <span className="text-[10px] px-1 rounded bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400">R</span>}
                                                    </td>
                                                    <td className="p-3">{planet.rasi_name}</td>
                                                    <td className="p-3 font-mono text-right">{planet.degree_str}</td>
                                                    <td className="p-3 text-right text-muted-foreground">{planet.nakshatra_pada}</td>
                                                </tr>
                                            );
                                        })}
                                    </tbody>
                                </table>
                            </div>
                        </CardContent>
                    </Card>

                    {/* Upcoming Sign Changes */}
                    <Card className="border border-black/20 dark:border-white/20 bg-white dark:bg-black h-full flex flex-col">
                        <CardHeader className="py-3 px-4 border-b border-black/10 dark:border-white/10 bg-black/5 dark:bg-white/5">
                            <CardTitle className="text-sm font-bold text-black dark:text-white tracking-wide uppercase flex items-center gap-2">
                                <span className="w-1.5 h-4 bg-emerald-500 rounded-sm"></span>
                                Upcoming Sign Changes
                            </CardTitle>
                        </CardHeader>
                        <CardContent className="p-0 flex-1">
                            {entriesLoading ? (
                                <div className="flex items-center justify-center p-8 h-full">
                                    <Loader2 className="w-6 h-6 animate-spin text-muted-foreground" />
                                </div>
                            ) : entriesData?.entries && entriesData.entries.length > 0 ? (
                                <div className="divide-y divide-border/50 max-h-[400px] overflow-y-auto">
                                    {entriesData.entries.map((entry, idx) => (
                                        <div key={idx} className="flex items-center justify-between p-3 text-xs hover:bg-muted/30 transition-colors">
                                            <div className="flex items-center gap-3">
                                                <span className="font-semibold w-16 text-primary">{entry.planet}</span>
                                                <div className="flex items-center gap-2 text-muted-foreground">
                                                    <span>➔</span>
                                                    <span className="font-medium text-foreground">{entry.entering_rasi_name}</span>
                                                </div>
                                            </div>
                                            <div className="text-right">
                                                <div className="font-mono font-medium">{entry.entry_datetime.split(' ')[0]}</div>
                                                <div className="text-[10px] text-muted-foreground">{entry.entry_datetime.split(' ')[1]}</div>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            ) : (
                                <div className="p-8 text-center text-sm text-muted-foreground flex flex-col items-center justify-center h-full">
                                    <Calendar className="w-8 h-8 mb-2 opacity-20" />
                                    No upcoming sign changes found
                                </div>
                            )}
                        </CardContent>
                    </Card>
                </div>

            </div>
        </div>
    );
}
