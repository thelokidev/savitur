'use client';

import { useState, useEffect, useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import Link from 'next/link';
import { ThemeToggle } from '@/components/ThemeToggle';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { panchangaApi } from '@/lib/api/panchanga';
import { chartsApi } from '@/lib/api/charts';

import { strengthApi } from '@/lib/api/strength';
import ChartRenderer from '@/components/charts/ChartRenderer';
import { BirthDetailsForm } from '@/components/features/BirthDetailsForm';
import { ComprehensivePlanetTable } from '@/components/features/ComprehensivePlanetTable';
import { AshtakavargaTable } from '@/components/features/AshtakavargaTable';
import { NatalPanchanga } from '@/components/features/NatalPanchanga';
import { UnifiedPanchanga } from '@/components/features/UnifiedPanchanga';
import DhasaTab from '@/components/features/DhasaTab';
import { StrengthTab } from '@/components/features/StrengthTab';
import { TransitTab } from '@/components/features/TransitTab';
import { AITab } from '@/components/features/AITab';
import { useBirthDetailsStore } from '@/lib/store/birth-details-store';
import { Menu, X } from 'lucide-react';

export default function Home() {
  // Use global store instead of local state
  const { birthData, chartStyle, hasCalculated, setBirthData, setChartStyle, setHasCalculated } = useBirthDetailsStore();

  const [shouldFetch, setShouldFetch] = useState(false);
  const [panchangaMode, setPanchangaMode] = useState<'natal' | 'daily'>('daily');
  const [selectedCharts, setSelectedCharts] = useState({
    chart1: '1',
    chart2: '9'
  });

  const [sidebarOpen, setSidebarOpen] = useState(!hasCalculated);

  // Debug: Log birthData updates
  useEffect(() => {
    console.log('DEBUG: BirthData updated:', birthData);
    console.log('DEBUG: Current Ayanamsa:', birthData.ayanamsa);
  }, [birthData]);

  // Prefetch: Wake up backend on page load to prevent cold start delays
  useEffect(() => {
    // Ping health endpoint to wake up the Render backend
    const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    fetch(`${API_URL}/health`).catch(() => { });
  }, []);

  // Auto-calculate on mount if birth data exists and has been calculated before
  useEffect(() => {
    if (hasCalculated && birthData.date && birthData.time && birthData.place.name) {
      setShouldFetch(true);
      setSidebarOpen(false); // Ensure it's closed if we have data
    }
  }, []); // Only run on mount

  // Build request data based on mode
  // Use useMemo to ensure pReq changes when mode or birthData changes
  const pReq = useMemo(() => {
    if (panchangaMode === 'natal') {
      return birthData;
    } else {
      // For daily mode, use today's date at sunrise time
      // In Hindu panchanga, the day is from sunrise to sunrise,
      // and daily elements are those in force at sunrise
      const now = new Date();
      const currentDateStr = now.toISOString().split('T')[0];

      // Use sunrise time (approximately 6:00 AM as placeholder)
      // The backend will calculate the exact sunrise and use that
      const sunriseTimeStr = '06:00:00';

      return {
        date: currentDateStr,
        time: sunriseTimeStr,
        place: birthData.place,
        ayanamsa: birthData.ayanamsa,
      };
    }
  }, [panchangaMode, birthData]);

  // Fetch all data (depends on mode)
  const panchanga = useQuery({
    queryKey: ['panchanga', panchangaMode, pReq.date, pReq.time, pReq.place.latitude, pReq.place.longitude, pReq.ayanamsa],
    queryFn: () => panchangaApi.calculate(pReq),
    enabled: shouldFetch,
    refetchOnWindowFocus: false,
  });

  // Panchanga sub-queries (for top-level Panchanga tab)
  const pPlanets = useQuery({
    queryKey: ['panchanga-planets', panchangaMode, pReq.date, pReq.time, pReq.place.latitude, pReq.place.longitude, pReq.ayanamsa],
    queryFn: () => panchangaApi.getPlanets(pReq),
    enabled: shouldFetch,
    refetchOnWindowFocus: false,
  });

  const pMuhurtha = useQuery({
    queryKey: ['panchanga-muhurtha', panchangaMode, pReq.date, pReq.time, pReq.place.latitude, pReq.place.longitude, pReq.ayanamsa],
    queryFn: () => panchangaApi.getMuhurtha(pReq),
    enabled: shouldFetch,
    refetchOnWindowFocus: false,
  });

  const pExtended = useQuery({
    queryKey: ['panchanga-extended', panchangaMode, pReq.date, pReq.time, pReq.place.latitude, pReq.place.longitude, pReq.ayanamsa],
    queryFn: () => panchangaApi.getExtended(pReq),
    enabled: shouldFetch,
    refetchOnWindowFocus: false,
  });

  const pEclipses = useQuery({
    queryKey: ['panchanga-eclipses', panchangaMode, pReq.date, pReq.time, pReq.place.latitude, pReq.place.longitude, pReq.ayanamsa],
    queryFn: () => panchangaApi.getEclipses(pReq),
    enabled: shouldFetch,
    refetchOnWindowFocus: false,
  });

  const pSankranti = useQuery({
    queryKey: ['panchanga-sankranti', panchangaMode, pReq.date, pReq.time, pReq.place.latitude, pReq.place.longitude, pReq.ayanamsa],
    queryFn: () => panchangaApi.getSankranti(pReq),
    enabled: shouldFetch,
    refetchOnWindowFocus: false,
  });

  const pRetrograde = useQuery({
    queryKey: ['panchanga-retrograde', panchangaMode, pReq.date, pReq.time, pReq.place.latitude, pReq.place.longitude, pReq.ayanamsa],
    queryFn: () => panchangaApi.getRetrograde(pReq),
    enabled: shouldFetch,
    refetchOnWindowFocus: false,
  });

  // Dedicated queries for Natal Chart Info (always uses birthData)
  const natalPanchanga = useQuery({
    queryKey: ['natal-panchanga', birthData.date, birthData.time, birthData.place.latitude, birthData.place.longitude, birthData.ayanamsa],
    queryFn: () => panchangaApi.calculate(birthData),
    enabled: shouldFetch,
    refetchOnWindowFocus: false,
  });

  const natalExtended = useQuery({
    queryKey: ['natal-extended', birthData.date, birthData.time, birthData.place.latitude, birthData.place.longitude, birthData.ayanamsa],
    queryFn: () => panchangaApi.getExtended(birthData),
    enabled: shouldFetch,
    refetchOnWindowFocus: false,
  });

  const chart1 = useQuery({
    queryKey: ['chart', selectedCharts.chart1, birthData.date, birthData.time, birthData.place.latitude, birthData.place.longitude, birthData.ayanamsa],
    queryFn: () => {
      console.log('DEBUG: Fetching chart1 with ayanamsa:', birthData.ayanamsa);
      if (selectedCharts.chart1 === '1') {
        return chartsApi.getRasiChart({ birth_details: birthData, ayanamsa: birthData.ayanamsa });
      } else {
        return chartsApi.getDivisionalChart(parseInt(selectedCharts.chart1), { birth_details: birthData, ayanamsa: birthData.ayanamsa });
      }
    },
    enabled: shouldFetch,
    refetchOnWindowFocus: false,
    structuralSharing: false,
  });

  const chart2 = useQuery({
    queryKey: ['chart', selectedCharts.chart2, birthData.date, birthData.time, birthData.place.latitude, birthData.place.longitude, birthData.ayanamsa],
    queryFn: () => {
      if (selectedCharts.chart2 === '1') {
        return chartsApi.getRasiChart({ birth_details: birthData, ayanamsa: birthData.ayanamsa });
      } else {
        return chartsApi.getDivisionalChart(parseInt(selectedCharts.chart2), { birth_details: birthData, ayanamsa: birthData.ayanamsa });
      }
    },
    enabled: shouldFetch,
    refetchOnWindowFocus: false,
    structuralSharing: false,
  });





  const ashtakavarga = useQuery({
    queryKey: ['ashtakavarga', birthData.date, birthData.time, birthData.place.latitude, birthData.place.longitude, birthData.ayanamsa],
    queryFn: () => strengthApi.getAshtakavarga({ birth_details: birthData, ayanamsa: birthData.ayanamsa }),
    enabled: shouldFetch,
    refetchOnWindowFocus: false,
  });

  const handleCalculate = () => {
    // Mark that calculation has been done
    setHasCalculated(true);
    setSidebarOpen(false); // Close sidebar on calculate

    // Enable queries and trigger refetch
    if (!shouldFetch) {
      setShouldFetch(true);
    } else {
      // If already enabled, manually refetch all queries
      panchanga.refetch();
      chart1.refetch();
      chart2.refetch();

      ashtakavarga.refetch();
      // DhasaTab handles its own refetching via its own useQuery dependency on birthData
    }
  };

  const handleChartChange = (chartSlot: 'chart1' | 'chart2', chartType: string) => {
    setSelectedCharts(prev => ({
      ...prev,
      [chartSlot]: chartType
    }));
  };

  return (
    <div className="flex h-screen bg-background overflow-hidden flex-col">

      {/* Mobile/Desktop Sidebar (Drawer) */}
      <div className={`fixed inset-0 z-50 ${sidebarOpen ? '' : 'pointer-events-none'}`} aria-hidden={!sidebarOpen}>
        <button
          aria-label="Close menu"
          onClick={() => setSidebarOpen(false)}
          className={`absolute inset-0 bg-black/50 transition-opacity ${sidebarOpen ? 'opacity-100' : 'opacity-0'}`}
        />
        <aside className={`absolute left-0 top-0 h-full w-80 border-r border-border bg-background shadow-lg transform transition-transform duration-300 ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}`}>
          <div className="p-4 border-b border-border">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h1 className="text-xl font-bold">Maara</h1>
                <p className="text-xs text-muted-foreground">Vedic Astrology</p>
              </div>
              <button
                aria-label="Close sidebar"
                onClick={() => setSidebarOpen(false)}
                className="inline-flex items-center justify-center h-9 w-9 rounded-md hover:bg-accent"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

          </div>
          <div className="m-4">
            <BirthDetailsForm
              birthData={birthData}
              onBirthDataChange={setBirthData}
              onCalculate={handleCalculate}
              isLoading={panchanga.isLoading}
              error={(panchanga.error as Error)?.message || (chart1.error as Error)?.message}
              chartStyle={chartStyle}
              onChartStyleChange={setChartStyle}
            />
          </div>
        </aside>
      </div>

      <main className="flex-1 h-full overflow-hidden flex flex-col">

        {/* Top Header (Always Visible) */}
        <div className="sticky top-0 z-40 border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 flex items-center justify-between px-3 h-12 flex-shrink-0">
          <button
            aria-label="Toggle menu"
            onClick={() => setSidebarOpen((v) => !v)}
            className="inline-flex items-center justify-center h-9 w-9 rounded-md hover:bg-accent"
          >
            <Menu className={`h-5 w-5 transition-all ${sidebarOpen ? 'scale-0' : 'scale-100'}`} />
            <X className={`absolute h-5 w-5 transition-all ${sidebarOpen ? 'scale-100' : 'scale-0'}`} />
          </button>
          <div className="flex items-center gap-2">
            <span className="text-sm font-semibold">Maara</span>
            <ThemeToggle />
          </div>
        </div>

        <div className="flex-1 p-2 overflow-hidden">
          {/* Main Tabs */}
          <div className="h-full flex flex-col border border-border rounded-lg p-2">
            <Tabs defaultValue="charts" className="w-full h-full flex flex-col min-h-0">
              <TabsList className="h-8 flex flex-wrap gap-1 flex-shrink-0">
                <TabsTrigger value="charts" className="text-xs">Charts</TabsTrigger>
                <TabsTrigger value="panchanga" className="text-xs">Panchanga</TabsTrigger>

                <TabsTrigger value="strength" className="text-xs">Strength</TabsTrigger>
                <TabsTrigger value="transits" className="text-xs">Transits</TabsTrigger>
                <TabsTrigger value="ai" className="text-xs">AI</TabsTrigger>
              </TabsList>

              {/* Charts Tab */}
              <TabsContent value="charts" className="flex-1 mt-2 flex flex-col gap-2 overflow-hidden min-h-0">

                {/* New Layout: Nested Grid */}
                <div className="flex-1 min-h-0 grid grid-cols-1 lg:grid-cols-[70%_30%] gap-2">

                  {/* Left Section: Flex Column for Rows */}
                  <div className="flex flex-col gap-2 h-full min-h-0">

                    {/* Top Row: Charts (2 columns) */}
                    <div className="grid grid-cols-2 gap-2 h-1/2 min-h-0">
                      {/* Chart 1 */}
                      <ChartRenderer
                        title="Chart 1"
                        data={chart1.data || null}
                        isLoading={chart1.isLoading}
                        onChartChange={(chartType) => handleChartChange('chart1', chartType)}
                        defaultChart={selectedCharts.chart1}
                        chartStyle={chartStyle}
                        className="w-full h-full min-h-0"
                      />

                      {/* Chart 2 */}
                      <ChartRenderer
                        title="Chart 2"
                        data={chart2.data || null}
                        isLoading={chart2.isLoading}
                        onChartChange={(chartType) => handleChartChange('chart2', chartType)}
                        defaultChart={selectedCharts.chart2}
                        chartStyle={chartStyle}
                        className="w-full h-full min-h-0"
                      />
                    </div>

                    {/* Bottom Row: Info Tables (3 columns) */}
                    <div className="grid grid-cols-[4.4fr_2.6fr_3fr] gap-2 h-1/2 min-h-0">

                      {/* Graha / Planet Info */}
                      <Card className="flex flex-col overflow-hidden w-full h-full min-h-0">
                        <CardHeader className="py-1 px-2 flex-shrink-0 bg-muted/30">
                          <CardTitle className="text-xs font-semibold">Graha / Planet Info</CardTitle>
                        </CardHeader>
                        <CardContent className="flex-1 overflow-auto p-0">
                          <ComprehensivePlanetTable
                            planets={chart1.data?.planets || []}
                            ascendant={chart1.data?.ascendant}
                            specialLagnas={chart1.data?.special_lagnas || []}
                            upagrahas={chart1.data?.upagrahas || []}
                            isLoading={chart1.isLoading}
                          />
                        </CardContent>
                      </Card>

                      {/* Natal Chart Info */}
                      <Card className="flex flex-col overflow-hidden w-full h-full min-h-0">
                        <CardHeader className="py-1 px-2 flex-shrink-0 bg-muted/30">
                          <CardTitle className="text-xs font-semibold">Natal Chart Info</CardTitle>
                        </CardHeader>
                        <CardContent className="flex-1 overflow-auto p-0">
                          <NatalPanchanga
                            data={natalPanchanga.data || null}
                            extendedData={natalExtended.data || null}
                            isLoading={natalPanchanga.isLoading}
                          />
                        </CardContent>
                      </Card>

                      {/* Ashtakavarga */}
                      <Card className="flex flex-col overflow-hidden w-full h-full min-h-0">
                        <CardHeader className="py-1 px-2 flex-shrink-0 bg-muted/30">
                          <CardTitle className="text-xs font-semibold">Ashtakavarga</CardTitle>
                        </CardHeader>
                        <CardContent className="flex-1 overflow-auto p-0">
                          <AshtakavargaTable
                            data={ashtakavarga.data}
                            isLoading={ashtakavarga.isLoading}
                            planetPositions={chart1.data}
                          />
                        </CardContent>
                      </Card>
                    </div>
                  </div>

                  {/* Right Section: Dasha Container (Full Height) */}
                  <div className="h-full min-h-0 overflow-hidden">
                    <DhasaTab birthData={birthData} compact={true} />
                  </div>

                </div>
              </TabsContent>

              <TabsContent value="panchanga" className="flex-1 overflow-y-auto min-h-0">
                <div className="p-2">
                  <UnifiedPanchanga
                    basicData={panchanga.data}
                    planetsData={pPlanets.data}
                    muhurthaData={pMuhurtha.data}
                    extendedData={pExtended.data}
                    eclipsesData={pEclipses.data}
                    sankrantiData={pSankranti.data}
                    retrogradeData={pRetrograde.data}
                    isLoading={panchanga.isLoading || pPlanets.isLoading || pMuhurtha.isLoading}
                    mode={panchangaMode}
                    onModeChange={(m) => {
                      setPanchangaMode(m);
                      if (shouldFetch) {
                        panchanga.refetch();
                        pPlanets.refetch();
                        pMuhurtha.refetch();
                        pExtended.refetch();
                        pEclipses.refetch();
                        pSankranti.refetch();
                        pRetrograde.refetch();
                      }
                    }}
                  />
                </div>
              </TabsContent>

              <TabsContent value="strength" className="flex-1 overflow-hidden min-h-0">
                <StrengthTab birthData={birthData} />
              </TabsContent>

              <TabsContent value="transits" className="flex-1 overflow-hidden min-h-0">
                <TransitTab birthData={birthData} />
              </TabsContent>

              <TabsContent value="ai" className="flex-1 overflow-hidden min-h-0">
                <AITab birthData={birthData} />
              </TabsContent>
            </Tabs>
          </div>
        </div>
      </main>
    </div>
  );
}
