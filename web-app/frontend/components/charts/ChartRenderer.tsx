'use client';

import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { mapPlanetsToNorthHouses, mapPlanetsToSouthHouses, runChartMappingTests } from '@/lib/charts/mapping';

interface Planet {
  name: string;
  rasi_name: string;
  degrees_in_rasi: number;
  longitude: number;
  retrograde?: boolean;
}

interface ChartData {
  ascendant: {
    rasi_name: string;
    longitude: number;
    degrees_in_rasi: number;
  };
  planets: Planet[];
}

type ChartStyle = 'south' | 'north';

interface ChartRendererProps {
  title: string;
  data: ChartData | null;
  isLoading: boolean;
  onChartChange: (chartType: string) => void;
  defaultChart?: string;
  chartStyle: ChartStyle;
  className?: string;
}

const RASI_NAMES = [
  'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
  'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
];

const RASI_SYMBOLS = ['♈', '♉', '♊', '♋', '♌', '♍', '♎', '♏', '♐', '♑', '♒', '♓'];

const RASI_SHORT = ['Ar', 'Ta', 'Ge', 'Cn', 'Le', 'Vi', 'Li', 'Sc', 'Sg', 'Cp', 'Aq', 'Pi'];

const PLANET_COLORS = {
  'Sun': '#FF6B35',
  'Moon': '#A8DADC',
  'Mars': '#E63946',
  'Mercury': '#06FFA5',
  'Jupiter': '#FFD60A',
  'Venus': '#FF69B4',
  'Saturn': '#457B9D',
  'Rahu': '#9D4EDD',
  'Ketu': '#F72585'
};

const PLANET_SYMBOLS: { [key: string]: string } = {
  'Sun': '☉',
  'Moon': '☽',
  'Mars': '♂',
  'Mercury': '☿',
  'Jupiter': '♃',
  'Venus': '♀',
  'Saturn': '♄',
  'Rahu': '☊',
  'Ketu': '☋'
};

const DIVISIONAL_CHARTS = [
  { value: '1', label: 'D1 - Rasi' },
  { value: '2', label: 'D2 - Hora' },
  { value: '3', label: 'D3 - Drekkana' },
  { value: '4', label: 'D4 - Chaturthamsa' },
  { value: '7', label: 'D7 - Saptamsa' },
  { value: '9', label: 'D9 - Navamsa' },
  { value: '10', label: 'D10 - Dasamsa' },
  { value: '12', label: 'D12 - Dwadasamsa' },
  { value: '16', label: 'D16 - Shodasamsa' },
  { value: '20', label: 'D20 - Vimsamsa' },
  { value: '24', label: 'D24 - Chaturvimsamsa' },
  { value: '27', label: 'D27 - Bhamsa' },
  { value: '30', label: 'D30 - Trimsamsa' },
  { value: '40', label: 'D40 - Khavedamsa' },
  { value: '45', label: 'D45 - Akshavedamsa' },
  { value: '60', label: 'D60 - Shashtyamsa' }
];

export default function ChartRenderer({
  title,
  data,
  isLoading,
  onChartChange,
  defaultChart = '1',
  chartStyle,
  className
}: ChartRendererProps) {
  const [selectedChart, setSelectedChart] = useState(defaultChart);

  const handleChartChange = (value: string) => {
    setSelectedChart(value);
    onChartChange(value);
  };

  const renderSouthIndianChart = () => {
    if (!data) return null;

    const ascendantRasi = RASI_NAMES.indexOf(data.ascendant.rasi_name);
    const southHouses = mapPlanetsToSouthHouses(data);

    // South Indian chart layout - Signs are FIXED, houses rotate
    // Layout matches the reference image: 3x3 grid with fixed sign positions
    // Signs start from bottom-left (Aries=0) and go counter-clockwise
    // Rasi positions in the 4x4 grid (fixed positions for signs)
    const rasiLayout = [
      [11, 0, 1, 2],    // Row 0: Pisces, Aries, Taurus, Gemini
      [10, -1, -1, 3],  // Row 1: Aquarius, (center), (center), Cancer
      [9, -1, -1, 4],   // Row 2: Capricorn, (center), (center), Leo
      [8, 7, 6, 5]      // Row 3: Sagittarius, Scorpio, Libra, Virgo
    ];

    return (
      <svg viewBox="0 0 600 600" className="w-full h-full animate-fadeIn">
        <defs>
          <filter id="shadow">
            <feDropShadow dx="0" dy="1" stdDeviation="2" floodOpacity="0.2" />
          </filter>
        </defs>

        {/* Background - clean white/transparent */}
        <rect width="600" height="600" fill="transparent" />

        {/* Render signs (fixed positions) */}
        {rasiLayout.map((row, rowIndex) =>
          row.map((rasiNum, colIndex) => {
            if (rasiNum === -1) return null;

            // In South Indian chart, signs are fixed, houses rotate
            const rasiIndex = rasiNum;
            const rasiName = RASI_NAMES[rasiIndex];
            const rasiSymbol = RASI_SYMBOLS[rasiIndex];

            // Calculate which house this rasi represents
            const houseNumber = ((rasiIndex - ascendantRasi + 12) % 12) + 1;
            const isAscendant = houseNumber === 1;

            const planetsInHouse = southHouses[houseNumber] || [];

            const x = colIndex * 150;
            const y = rowIndex * 150;

            return (
              <g key={`${rowIndex}-${colIndex}`}>
                {/* Define clip region for this cell to keep all content within borders */}
                <clipPath id={`clip-s-${rowIndex}-${colIndex}`}>
                  <rect x={x + 1} y={y + 1} width="148" height="148" />
                </clipPath>

                {/* House border - only draw borders, no background lines */}
                <rect
                  x={x} y={y} width="150" height="150"
                  fill="transparent"
                  stroke="currentColor"
                  strokeWidth="2.5"
                  className="stroke-foreground hover:fill-accent/10 transition-all cursor-pointer"
                />

                {/* Content via HTML/Flexbox */}
                <foreignObject x={x} y={y} width="150" height="150" clipPath={`url(#clip-s-${rowIndex}-${colIndex})`}>
                  <div className="w-full h-full p-2 flex flex-col justify-start items-start relative text-foreground">
                    {/* Rasi Number */}
                    <div className="text-xl font-bold leading-none mb-1 opacity-70">{rasiIndex + 1}</div>

                    {/* Ascendant Label */}
                    {isAscendant && (
                      <div className="absolute top-2 right-2 flex flex-col items-end">
                        <span className="text-yellow-600 font-extrabold text-sm">Asc</span>
                        <span className="text-yellow-600 font-bold text-xs">
                          {Math.floor(data.ascendant.degrees_in_rasi)}°
                          {Math.floor((data.ascendant.degrees_in_rasi - Math.floor(data.ascendant.degrees_in_rasi)) * 60).toString().padStart(2, '0')}'
                        </span>
                      </div>
                    )}

                    {/* Planets List */}
                    <div className="w-full flex flex-col gap-0.5 mt-2">
                      {planetsInHouse.map((planet, pIndex) => {
                        const degrees = Math.floor(planet.degrees_in_rasi);
                        const minutes = Math.floor((planet.degrees_in_rasi - degrees) * 60);
                        const degreeString = `${degrees}°${minutes.toString().padStart(2, '0')}'`;

                        return (
                          <div key={pIndex} className="flex justify-between items-center w-full text-sm hover:bg-accent/20 rounded px-0.5 font-bold">
                            <div className="flex items-center gap-0.5">
                              <span>{planet.name.substring(0, 2)}</span>
                              {planet.retrograde && (
                                <span className="text-destructive font-bold text-[10px] bg-destructive/10 rounded-full w-3 h-3 inline-flex items-center justify-center">R</span>
                              )}
                            </div>
                            <span className="text-muted-foreground text-xs tabular-nums font-medium">{degreeString}</span>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                </foreignObject>
              </g>
            );
          })
        )}
      </svg>
    );
  };

  const renderNorthIndianChart = () => {
    if (!data) return null;

    const ascendantRasi = RASI_NAMES.indexOf(data.ascendant.rasi_name);
    const northHouses = mapPlanetsToNorthHouses(data);

    // North Indian chart - Diamond with 12 houses
    // Houses are FIXED positions, signs ROTATE based on ascendant
    // Houses go COUNTER-CLOCKWISE starting from House 1 at the top center diamond
    // Enlarged for better visibility: 900x900 viewBox (1.5x scale)

    const BASE_X = 60, BASE_Y = 60, W = 780, H = 780;
    const CX = BASE_X + W / 2, CY = BASE_Y + H / 2; // Center = (450, 450)
    type TextAnchor = 'start' | 'middle' | 'end';
    type HousePosition = {
      house: number;
      signX: number;
      signY: number;
      planetX: number;
      planetY: number;
      anchor: TextAnchor;
      planetAnchor: TextAnchor;
    };

    // Precise symmetric coordinates for 12 houses (scaled 1.5x from original 600x600)
    // House 1, 4, 7, 10 are the central diamonds/triangles (Kendras)
    // House 2, 3, 5, 6, 8, 9, 11, 12 are the outer triangles
    const housePositions: HousePosition[] = [
      // House 1: Top Diamond (Lagna)
      { house: 1, signX: 450, signY: 210, planetX: 450, planetY: 248, anchor: 'middle', planetAnchor: 'middle' },

      // House 2: Top-Left Upper Triangle
      { house: 2, signX: 270, signY: 128, planetX: 270, planetY: 158, anchor: 'middle', planetAnchor: 'middle' },

      // House 3: Top-Left Lower Triangle
      { house: 3, signX: 128, signY: 270, planetX: 128, planetY: 300, anchor: 'middle', planetAnchor: 'middle' },

      // House 4: Left Diamond
      { house: 4, signX: 240, signY: 450, planetX: 240, planetY: 488, anchor: 'middle', planetAnchor: 'middle' },

      // House 5: Bottom-Left Upper Triangle
      { house: 5, signX: 128, signY: 630, planetX: 128, planetY: 660, anchor: 'middle', planetAnchor: 'middle' },

      // House 6: Bottom-Left Lower Triangle
      { house: 6, signX: 270, signY: 773, planetX: 270, planetY: 803, anchor: 'middle', planetAnchor: 'middle' },

      // House 7: Bottom Diamond
      { house: 7, signX: 450, signY: 690, planetX: 450, planetY: 728, anchor: 'middle', planetAnchor: 'middle' },

      // House 8: Bottom-Right Lower Triangle
      { house: 8, signX: 630, signY: 773, planetX: 630, planetY: 803, anchor: 'middle', planetAnchor: 'middle' },

      // House 9: Bottom-Right Upper Triangle
      { house: 9, signX: 773, signY: 630, planetX: 773, planetY: 660, anchor: 'middle', planetAnchor: 'middle' },

      // House 10: Right Diamond
      { house: 10, signX: 660, signY: 450, planetX: 660, planetY: 488, anchor: 'middle', planetAnchor: 'middle' },

      // House 11: Top-Right Lower Triangle
      { house: 11, signX: 773, signY: 270, planetX: 773, planetY: 300, anchor: 'middle', planetAnchor: 'middle' },

      // House 12: Top-Right Upper Triangle
      { house: 12, signX: 630, signY: 128, planetX: 630, planetY: 158, anchor: 'middle', planetAnchor: 'middle' },
    ];

    // Enlarge the north chart contents within its container by scaling the drawing group.
    // This keeps the same card size but makes text/lines/planets visibly larger.
    const DRAW_SCALE = 1.15;

    return (
      <svg viewBox="0 0 900 900" preserveAspectRatio="xMidYMid meet" className="w-full h-full animate-fadeIn">
        {/* Clean background */}
        <rect width="900" height="900" fill="transparent" />

        <g transform={`translate(${CX} ${CY}) scale(${DRAW_SCALE}) translate(${-CX} ${-CY})`}>
          {/* Outer square border */}
          <rect x={BASE_X} y={BASE_Y} width={W} height={H}
            fill="transparent"
            stroke="currentColor"
            strokeWidth="3.5"
            className="stroke-foreground" />

          {/* Main diagonals (corner-to-corner) */}
          <line x1={BASE_X} y1={BASE_Y} x2={BASE_X + W} y2={BASE_Y + H}
            stroke="currentColor" strokeWidth="2.5" className="stroke-foreground" />
          <line x1={BASE_X} y1={BASE_Y + H} x2={BASE_X + W} y2={BASE_Y}
            stroke="currentColor" strokeWidth="2.5" className="stroke-foreground" />

          {/* Inner diamond connecting midpoints of edges */}
          <line x1={BASE_X} y1={CY} x2={CX} y2={BASE_Y}
            stroke="currentColor" strokeWidth="2.5" className="stroke-foreground" />
          <line x1={CX} y1={BASE_Y} x2={BASE_X + W} y2={CY}
            stroke="currentColor" strokeWidth="2.5" className="stroke-foreground" />
          <line x1={BASE_X + W} y1={CY} x2={CX} y2={BASE_Y + H}
            stroke="currentColor" strokeWidth="2.5" className="stroke-foreground" />
          <line x1={CX} y1={BASE_Y + H} x2={BASE_X} y2={CY}
            stroke="currentColor" strokeWidth="2.5" className="stroke-foreground" />

          {/* Render houses */}
          {housePositions.map((pos) => {
            // Signs rotate based on ascendant
            const rasiIndex = (ascendantRasi + pos.house - 1) % 12;
            const planetsInHouse = northHouses[pos.house] || [];
            const isAscendant = pos.house === 1;

            return (
              <g key={pos.house}>
                {/* Sign number (1-12 for Aries-Pisces) */}
                <text
                  x={pos.signX}
                  y={pos.signY}
                  className="fill-muted-foreground text-[20px] font-bold opacity-80"
                  textAnchor={pos.anchor}
                >
                  {String(rasiIndex + 1).padStart(2, '0')}
                </text>

                {/* Ascendant indicator for House 1 */}
                {isAscendant && (
                  <text
                    x={CX}
                    y={BASE_Y + 173}
                    className="fill-yellow-600 text-[14px] font-bold"
                    textAnchor="middle"
                  >
                    Asc {Math.floor(data.ascendant.degrees_in_rasi)}°
                    {Math.floor((data.ascendant.degrees_in_rasi - Math.floor(data.ascendant.degrees_in_rasi)) * 60).toString().padStart(2, '0')}'
                  </text>
                )}

                {/* Planets */}
                {planetsInHouse.map((planet, pIndex) => {
                  const py = pos.planetY + pIndex * 26; // Increased spacing
                  const degrees = Math.floor(planet.degrees_in_rasi);
                  const minutes = Math.floor((planet.degrees_in_rasi - degrees) * 60);
                  const degreeString = `${degrees}°${minutes.toString().padStart(2, '0')}'`;
                  const planetAbbr = planet.name.substring(0, 2);
                  const displayText = planet.retrograde
                    ? `${planetAbbr} (R) ${degreeString}` // Using (R) for SVG compatibility or use unicode
                    : `${planetAbbr} ${degreeString}`;

                  return (
                    <text
                      key={pIndex}
                      x={pos.planetX}
                      y={py}
                      className="fill-foreground text-[15px] font-bold"
                      textAnchor={pos.planetAnchor}
                    >
                      {planetAbbr}
                      {planet.retrograde && (
                        <tspan className="fill-destructive font-bold" dx="2" fontSize="12">Ⓡ</tspan>
                      )}
                      <tspan dx="5" fontSize="13" fontWeight="normal" className="fill-muted-foreground/80">{degreeString}</tspan>
                    </text>
                  );
                })}
              </g>
            );
          })}
        </g>
      </svg>
    );
  };



  const renderChart = () => {
    switch (chartStyle) {
      case 'south':
        return renderSouthIndianChart();
      case 'north':
        return renderNorthIndianChart();
      default:
        return renderSouthIndianChart();
    }
  };

  return (
    <Card className={`flex flex-col overflow-hidden shadow-lg hover:shadow-xl transition-shadow duration-300 ${className || 'h-full'}`}>
      <CardHeader className="py-1 px-2 bg-gradient-to-r from-primary/5 to-accent/5">
        <div className="flex items-center justify-between">
          <CardTitle className="text-xs font-semibold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
            {title}
          </CardTitle>
          <div className="flex gap-2">
            <Select value={selectedChart} onValueChange={handleChartChange}>
              <SelectTrigger className="w-28 h-6 text-xs border-primary/20 hover:border-primary/40 transition-colors">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {DIVISIONAL_CHARTS.map((chart) => (
                  <SelectItem key={chart.value} value={chart.value} className="text-xs">
                    {chart.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>
      </CardHeader>
      <CardContent className="flex-1 p-1 min-h-0">
        {isLoading ? (
          <div className="h-full flex flex-col items-center justify-center text-xs text-muted-foreground">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mb-2"></div>
            <span>Loading chart...</span>
          </div>
        ) : data ? (
          <div className="h-full w-full flex items-center justify-center">
            {renderChart()}
          </div>
        ) : (
          <div className="h-full flex items-center justify-center text-xs text-muted-foreground">
            <div className="text-center">
              <div className="text-4xl mb-2 opacity-20">📊</div>
              <div>Calculate to view chart</div>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
