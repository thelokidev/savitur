import React from 'react';
import { Card } from '@/components/ui/card';

interface AshtakavargaTableProps {
    data: any;
    isLoading: boolean;
    planetPositions?: any; // Optional prop to highlight planet positions
}

const RASI_NAMES = [
    'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
    'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
];

// South Indian Chart Layout Mapping
// Maps 4x4 grid cells to Rasi indices (0=Aries, 11=Pisces)
// -1 indicates center cell
const SOUTH_INDIAN_LAYOUT = [
    [11, 0, 1, 2],    // Pisces, Aries, Taurus, Gemini
    [10, -1, -1, 3],  // Aquarius, Center, Center, Cancer
    [9, -1, -1, 4],   // Capricorn, Center, Center, Leo
    [8, 7, 6, 5]      // Sagittarius, Scorpio, Libra, Virgo
];

interface MiniChartProps {
    title: string;
    points: number[];
    highlightIndex?: number; // Index of rasi to highlight (0-11)
    className?: string;
}

const MiniSouthIndianChart: React.FC<MiniChartProps> = ({ title, points, highlightIndex, className }) => {
    return (
        <div className={`border border-border bg-card text-card-foreground relative flex flex-col overflow-hidden ${className}`}>
            {/* 4x4 Grid */}
            <div className="w-full h-full grid grid-cols-4 grid-rows-4 text-[9px] leading-none">
                {SOUTH_INDIAN_LAYOUT.map((row, rowIndex) => (
                    <React.Fragment key={rowIndex}>
                        {row.map((rasiIndex, colIndex) => {
                            if (rasiIndex === -1) {
                                // Only render the center cell once (at 1,1)
                                if (rowIndex === 1 && colIndex === 1) {
                                    return (
                                        <div
                                            key="center"
                                            className="col-span-2 row-span-2 flex items-center justify-center bg-muted/20"
                                        >
                                            <span className="text-red-600 dark:text-red-400 font-bold text-xs">
                                                {title}
                                            </span>
                                        </div>
                                    );
                                }
                                return null;
                            }

                            const pointValue = points[rasiIndex] ?? 0;
                            const isHighlighted = highlightIndex === rasiIndex;

                            return (
                                <div
                                    key={`${rowIndex}-${colIndex}`}
                                    className={`
                                        border-[0.5px] border-border/50 flex items-center justify-center
                                        ${isHighlighted ? 'bg-muted/50 dark:bg-muted/30 font-semibold' : ''}
                                    `}
                                >
                                    <span className={isHighlighted ? 'text-primary' : 'text-foreground'}>
                                        {pointValue}
                                    </span>
                                </div>
                            );
                        })}
                    </React.Fragment>
                ))}
            </div>
        </div>
    );
};

export function AshtakavargaTable({ data, isLoading, planetPositions }: AshtakavargaTableProps) {
    if (isLoading) {
        return (
            <div className="h-full flex flex-col items-center justify-center text-xs text-muted-foreground">
                <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-primary mb-2"></div>
                <span>Loading Ashtakavarga...</span>
            </div>
        );
    }

    if (!data || !data.sarvashtakavarga) {
        return (
            <div className="h-full flex items-center justify-center text-xs text-muted-foreground">
                No Ashtakavarga data available
            </div>
        );
    }

    // Helper to convert object {rasi_1: val, ...} to array
    const objToArray = (obj: any): number[] => {
        if (!obj) return new Array(12).fill(0);
        const arr = new Array(12).fill(0);
        for (let i = 1; i <= 12; i++) {
            arr[i - 1] = obj[`rasi_${i}`] || 0;
        }
        return arr;
    };

    // Prepare data for 9 charts
    const savPoints = Array.isArray(data.sarvashtakavarga) ? data.sarvashtakavarga : objToArray(data.sarvashtakavarga);
    const bav = data.bhinnashtakavarga || {};

    // Chart Definitions
    // Title, Data Key, Planet Name (for finding position)
    const charts = [
        { title: 'SAV', points: savPoints, planetName: 'Ascendant' }, // SAV usually highlights Ascendant if anything
        { title: 'As', points: objToArray(bav['Lagnam']), planetName: 'Ascendant' },
        { title: 'Su', points: objToArray(bav['Sun']), planetName: 'Sun' },
        { title: 'Mo', points: objToArray(bav['Moon']), planetName: 'Moon' },
        { title: 'Ma', points: objToArray(bav['Mars']), planetName: 'Mars' },
        { title: 'Me', points: objToArray(bav['Mercury']), planetName: 'Mercury' },
        { title: 'Ju', points: objToArray(bav['Jupiter']), planetName: 'Jupiter' },
        { title: 'Ve', points: objToArray(bav['Venus']), planetName: 'Venus' },
        { title: 'Sa', points: objToArray(bav['Saturn']), planetName: 'Saturn' },
    ];

    // Helper to find planet rasi index
    const getPlanetRasiIndex = (pName: string): number | undefined => {
        if (!planetPositions) return undefined;

        if (pName === 'Ascendant') {
            // Check if ascendant is passed directly or inside planets
            if (planetPositions.ascendant) {
                return RASI_NAMES.indexOf(planetPositions.ascendant.rasi_name);
            }
            // If planetPositions IS the chart data object
            if (planetPositions.rasi_name) { // It's the ascendant object itself? No, usually passed as chartData
                return RASI_NAMES.indexOf(planetPositions.rasi_name);
            }
            return undefined;
        }

        // Search in planets array
        const planets = planetPositions.planets || planetPositions; // Handle if passed full chart object or just planets array
        if (Array.isArray(planets)) {
            const p = planets.find((pl: any) => pl.name === pName);
            if (p) return RASI_NAMES.indexOf(p.rasi_name);
        }
        return undefined;
    };

    return (
        <div className="w-full h-full p-1 overflow-hidden">
            <div className="grid grid-cols-3 grid-rows-3 gap-1 h-full w-full">
                {charts.map((chart, index) => {
                    // Determine highlight index
                    let highlightIdx = undefined;
                    if (planetPositions) {
                        if (chart.title === 'SAV') {
                            if (planetPositions.ascendant) {
                                highlightIdx = RASI_NAMES.indexOf(planetPositions.ascendant.rasi_name);
                            }
                        } else {
                            highlightIdx = getPlanetRasiIndex(chart.planetName);
                        }
                    }

                    return (
                        <MiniSouthIndianChart
                            key={chart.title}
                            title={chart.title}
                            points={chart.points}
                            highlightIndex={highlightIdx}
                            className="w-full h-full"
                        />
                    );
                })}
            </div>
        </div>
    );
}
