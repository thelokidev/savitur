'use client';

import { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import Link from 'next/link';
import { ThemeToggle } from '@/components/ThemeToggle';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { BirthDetailsForm } from '@/components/features/BirthDetailsForm';
import { panchangaApi } from '@/lib/api/panchanga';
import { useBirthDetailsStore } from '@/lib/store/birth-details-store';
import { Menu, X } from 'lucide-react';

export default function PanchangaPage() {
  // Use global store instead of local state
  const { birthData, hasCalculated, setBirthData, setHasCalculated } = useBirthDetailsStore();

  const [shouldFetch, setShouldFetch] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // Auto-calculate on mount if birth data exists (always, not just if calculated before)
  useEffect(() => {
    if (birthData.date && birthData.time && birthData.place.name) {
      setShouldFetch(true);
    }
  }, []); // Only run on mount

  // Fetch all panchanga data
  const basicPanchanga = useQuery({
    queryKey: [
      'panchanga-basic',
      birthData.date,
      birthData.time,
      birthData.place.latitude,
      birthData.place.longitude,
      birthData.place.timezone,
      birthData.ayanamsa
    ],
    queryFn: () => panchangaApi.calculate(birthData),
    enabled: shouldFetch,
    refetchOnWindowFocus: false,
  });

  const planets = useQuery({
    queryKey: [
      'panchanga-planets',
      birthData.date,
      birthData.time,
      birthData.place.latitude,
      birthData.place.longitude,
      birthData.place.timezone,
      birthData.ayanamsa
    ],
    queryFn: () => panchangaApi.getPlanets(birthData),
    enabled: shouldFetch,
    refetchOnWindowFocus: false,
  });

  const muhurtha = useQuery({
    queryKey: [
      'panchanga-muhurtha',
      birthData.date,
      birthData.time,
      birthData.place.latitude,
      birthData.place.longitude,
      birthData.place.timezone,
      birthData.ayanamsa
    ],
    queryFn: () => panchangaApi.getMuhurtha(birthData),
    enabled: shouldFetch,
    refetchOnWindowFocus: false,
  });

  const extended = useQuery({
    queryKey: [
      'panchanga-extended',
      birthData.date,
      birthData.time,
      birthData.place.latitude,
      birthData.place.longitude,
      birthData.place.timezone,
      birthData.ayanamsa
    ],
    queryFn: () => panchangaApi.getExtended(birthData),
    enabled: shouldFetch,
    refetchOnWindowFocus: false,
  });

  const eclipses = useQuery({
    queryKey: [
      'panchanga-eclipses',
      birthData.date,
      birthData.time,
      birthData.place.latitude,
      birthData.place.longitude,
      birthData.place.timezone,
      birthData.ayanamsa
    ],
    queryFn: () => panchangaApi.getEclipses(birthData),
    enabled: shouldFetch,
    refetchOnWindowFocus: false,
  });

  const sankranti = useQuery({
    queryKey: [
      'panchanga-sankranti',
      birthData.date,
      birthData.time,
      birthData.place.latitude,
      birthData.place.longitude,
      birthData.place.timezone,
      birthData.ayanamsa
    ],
    queryFn: () => panchangaApi.getSankranti(birthData),
    enabled: shouldFetch,
    refetchOnWindowFocus: false,
  });

  const retrograde = useQuery({
    queryKey: [
      'panchanga-retrograde',
      birthData.date,
      birthData.time,
      birthData.place.latitude,
      birthData.place.longitude,
      birthData.place.timezone,
      birthData.ayanamsa
    ],
    queryFn: () => panchangaApi.getRetrograde(birthData),
    enabled: shouldFetch,
    refetchOnWindowFocus: false,
  });

  const handleCalculate = () => {
    // Mark that calculation has been done
    setHasCalculated(true);
    
    if (!shouldFetch) {
      setShouldFetch(true);
    } else {
      basicPanchanga.refetch();
      planets.refetch();
      muhurtha.refetch();
      extended.refetch();
      eclipses.refetch();
      sankranti.refetch();
      retrograde.refetch();
    }
  };

  const isLoading = basicPanchanga.isLoading || planets.isLoading || muhurtha.isLoading;
  const error = (basicPanchanga.error as Error)?.message || 
                (planets.error as Error)?.message || 
                (muhurtha.error as Error)?.message;

  return (
    <div className="flex h-screen bg-background overflow-hidden">
      {/* Fixed Left Sidebar - Input Form (desktop) */}
      <aside className="hidden md:block w-80 border-r border-border overflow-y-auto flex-shrink-0">
        <div className="p-4 border-b border-border">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-xl font-bold">PyJHora</h1>
              <p className="text-xs text-muted-foreground">Panchanga Details</p>
            </div>
            <ThemeToggle />
          </div>
          <nav className="flex gap-2 text-xs">
            <Link href="/" className="px-3 py-1.5 hover:bg-accent rounded">Charts</Link>
            <Link href="/panchanga" className="px-3 py-1.5 bg-primary text-primary-foreground rounded">Panchanga</Link>
          </nav>
        </div>

        <div className="m-4">
          <BirthDetailsForm
            birthData={birthData}
            onBirthDataChange={setBirthData}
            onCalculate={handleCalculate}
            isLoading={isLoading}
            error={error}
          />
        </div>
      </aside>

      
      <div className={`fixed inset-0 z-50 md:hidden ${sidebarOpen ? '' : 'pointer-events-none'}`} aria-hidden={!sidebarOpen}>
        <button
          aria-label="Close menu"
          onClick={() => setSidebarOpen(false)}
          className={`absolute inset-0 bg-black/50 transition-opacity ${sidebarOpen ? 'opacity-100' : 'opacity-0'}`}
        />
        <aside className={`absolute left-0 top-0 h-full w-80 border-r border-border bg-background shadow-lg transform transition-transform duration-300 ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}`}>
          <div className="p-4 border-b border-border">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h1 className="text-xl font-bold">PyJHora</h1>
                <p className="text-xs text-muted-foreground">Panchanga Details</p>
              </div>
              <button
                aria-label="Close sidebar"
                onClick={() => setSidebarOpen(false)}
                className="inline-flex items-center justify-center h-9 w-9 rounded-md hover:bg-accent"
              >
                <X className="h-5 w-5" />
              </button>
            </div>
            <nav className="flex gap-2 text-xs">
              <Link href="/" className="px-3 py-1.5 hover:bg-accent rounded">Charts</Link>
              <Link href="/panchanga" className="px-3 py-1.5 bg-primary text-primary-foreground rounded">Panchanga</Link>
            </nav>
          </div>
          <div className="m-4">
            <BirthDetailsForm
              birthData={birthData}
              onBirthDataChange={setBirthData}
              onCalculate={handleCalculate}
              isLoading={isLoading}
              error={error}
            />
          </div>
        </aside>
      </div>

      {/* Main Content Area - Full Panchanga Data */}
      <main className="flex-1 overflow-y-auto">
        
        <div className="sticky top-0 z-40 md:hidden border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 flex items-center justify-between px-3 h-12">
          <button
            aria-label="Toggle menu"
            onClick={() => setSidebarOpen((v) => !v)}
            className="inline-flex items-center justify-center h-9 w-9 rounded-md hover:bg-accent"
          >
            <Menu className={`h-5 w-5 transition-all ${sidebarOpen ? 'scale-0' : 'scale-100'}`} />
            <X className={`absolute h-5 w-5 transition-all ${sidebarOpen ? 'scale-100' : 'scale-0'}`} />
          </button>
          <div className="flex items-center gap-2">
            <span className="text-sm font-semibold">PyJHora</span>
            <ThemeToggle />
          </div>
        </div>
        <div className="p-6 space-y-4">
          <h2 className="text-2xl font-bold">Complete Panchanga Information</h2>

          <Tabs defaultValue="basic" className="w-full">
            <TabsList className="grid w-full grid-cols-7">
              <TabsTrigger value="basic">Basic</TabsTrigger>
              <TabsTrigger value="planets">Planets</TabsTrigger>
              <TabsTrigger value="muhurtha">Muhurtha</TabsTrigger>
              <TabsTrigger value="extended">Extended</TabsTrigger>
              <TabsTrigger value="eclipses">Eclipses</TabsTrigger>
              <TabsTrigger value="sankranti">Sankranti</TabsTrigger>
              <TabsTrigger value="retrograde">Retrograde</TabsTrigger>
            </TabsList>

            {/* Basic Panchanga Tab */}
            <TabsContent value="basic" className="space-y-4">
              {basicPanchanga.data ? (
                <div className="grid grid-cols-2 gap-4">
                  <Card>
                    <CardHeader>
                      <CardTitle className="text-lg">Five Elements (Panchanga)</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-3">
                      <DataRow label="Tithi" value={basicPanchanga.data.tithi?.name} />
                      <DataRow label="Paksha" value={basicPanchanga.data.tithi?.paksha} />
                      <DataRow label="Tithi End" value={basicPanchanga.data.tithi?.end_time} />
                      <Separator />
                      <DataRow label="Nakshatra" value={basicPanchanga.data.nakshatra?.name} />
                      <DataRow label="Pada" value={basicPanchanga.data.nakshatra?.pada} />
                      <DataRow label="Nakshatra Lord" value={basicPanchanga.data.nakshatra?.lord} />
                      <DataRow label="Nakshatra End" value={basicPanchanga.data.nakshatra?.end_time} />
                      <Separator />
                      <DataRow label="Yoga" value={basicPanchanga.data.yoga?.name} />
                      <DataRow label="Yoga End" value={basicPanchanga.data.yoga?.end_time} />
                      <Separator />
                      <DataRow label="Karana" value={basicPanchanga.data.karana?.name} />
                      <DataRow label="Karana End" value={basicPanchanga.data.karana?.end_time} />
                      <Separator />
                      <DataRow label="Vaara (Weekday)" value={basicPanchanga.data.vaara} />
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader>
                      <CardTitle className="text-lg">Astronomical Data</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-3">
                      <DataRow label="Sunrise" value={basicPanchanga.data.sunrise} />
                      <DataRow label="Sunset" value={basicPanchanga.data.sunset} />
                      <DataRow label="Moonrise" value={basicPanchanga.data.moonrise} />
                      <DataRow label="Moonset" value={basicPanchanga.data.moonset} />
                      <Separator />
                      <DataRow label="Ayanamsa Value" value={basicPanchanga.data.ayanamsa_value?.toFixed(6)} />
                      <DataRow label="Julian Day" value={basicPanchanga.data.julian_day?.toFixed(4)} />
                      <Separator className="my-3" />
                      <div className="text-sm font-semibold text-destructive">Inauspicious Times</div>
                      <DataRow 
                        label="Rahu Kala" 
                        value={`${basicPanchanga.data.rahu_kala?.start} - ${basicPanchanga.data.rahu_kala?.end}`} 
                      />
                      <DataRow 
                        label="Yamaganda" 
                        value={`${basicPanchanga.data.yamaganda?.start} - ${basicPanchanga.data.yamaganda?.end}`} 
                      />
                      <DataRow 
                        label="Gulika" 
                        value={`${basicPanchanga.data.gulika?.start} - ${basicPanchanga.data.gulika?.end}`} 
                      />
                      <Separator className="my-3" />
                      <div className="text-sm font-semibold text-green-600">Auspicious Time</div>
                      <DataRow 
                        label="Abhijit Muhurta" 
                        value={`${basicPanchanga.data.abhijit_muhurta?.start} - ${basicPanchanga.data.abhijit_muhurta?.end}`}
                        className="text-green-600"
                      />
                    </CardContent>
                  </Card>

                  <Card className="col-span-2">
                    <CardHeader>
                      <CardTitle className="text-lg">Additional Details</CardTitle>
                    </CardHeader>
                    <CardContent className="grid grid-cols-3 gap-4">
                      <div>
                        <div className="text-sm font-semibold mb-2">Tithi Details</div>
                        <DataRow label="Deity" value={basicPanchanga.data.tithi_details?.deity} />
                        <DataRow label="Lord" value={basicPanchanga.data.tithi_details?.lord} />
                      </div>
                      <div>
                        <div className="text-sm font-semibold mb-2">Nakshatra Details</div>
                        <DataRow label="Deity" value={basicPanchanga.data.nakshatra_details?.deity} />
                      </div>
                      <div>
                        <div className="text-sm font-semibold mb-2">Yoga Details</div>
                        <DataRow label="Quality" value={basicPanchanga.data.yoga_details?.quality} />
                      </div>
                    </CardContent>
                  </Card>
                </div>
              ) : (
                <EmptyState message="Click Calculate to view basic panchanga" />
              )}
            </TabsContent>

            {/* Planets Tab */}
            <TabsContent value="planets" className="space-y-4">
              {planets.data ? (
                <div className="grid grid-cols-2 gap-4">
                  <Card>
                    <CardHeader>
                      <CardTitle className="text-lg">Planet Positions</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-2">
                        {planets.data.ascendant && (
                          <div className="p-3 bg-primary/5 border border-primary/20 rounded-lg">
                            <div className="font-semibold text-primary">Ascendant</div>
                            <div className="grid grid-cols-2 gap-2 text-sm mt-1">
                              <DataRow label="Rasi" value={planets.data.ascendant.rasi_name} />
                              <DataRow label="Longitude" value={`${planets.data.ascendant.longitude.toFixed(2)}°`} />
                              <DataRow label="Degrees" value={`${planets.data.ascendant.degrees_in_rasi.toFixed(2)}°`} />
                              <DataRow label="Nakshatra" value={planets.data.ascendant.nakshatra_name} />
                            </div>
                          </div>
                        )}
                        
                        {planets.data.planets?.map((planet: any, i: number) => (
                          <div key={i} className="p-3 border rounded-lg hover:bg-accent transition-colors">
                            <div className="flex items-center justify-between">
                              <span className="font-semibold">{planet.name}</span>
                              {planet.retrograde && (
                                <span className="text-xs px-2 py-0.5 bg-destructive/20 text-destructive rounded">R</span>
                              )}
                            </div>
                            <div className="grid grid-cols-2 gap-2 text-sm mt-1">
                              <DataRow label="Rasi" value={planet.rasi_name} />
                              <DataRow label="Longitude" value={`${planet.longitude.toFixed(2)}°`} />
                              <DataRow label="Degrees" value={`${planet.degrees_in_rasi.toFixed(2)}°`} />
                              <DataRow label="Nakshatra" value={planet.nakshatra_name} />
                            </div>
                          </div>
                        ))}
                      </div>
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader>
                      <CardTitle className="text-lg">Astronomical Data</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-3">
                      <DataRow label="Julian Day" value={planets.data.julian_day?.toFixed(4)} />
                      <DataRow label="Ayanamsa Value" value={planets.data.ayanamsa_value?.toFixed(6)} />
                    </CardContent>
                  </Card>
                </div>
              ) : (
                <EmptyState message="Click Calculate to view planet positions" />
              )}
            </TabsContent>

            {/* Muhurtha Tab */}
            <TabsContent value="muhurtha" className="space-y-4">
              {muhurtha.data ? (
                <div className="grid grid-cols-2 gap-4">
                  <Card>
                    <CardHeader>
                      <CardTitle className="text-lg">Special Muhurthas</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-3">
                      <DataRow 
                        label="Brahma Muhurta" 
                        value={`${muhurtha.data.brahma_muhurta?.start} - ${muhurtha.data.brahma_muhurta?.end}`}
                      />
                      <DataRow 
                        label="Vijaya Muhurta" 
                        value={`${muhurtha.data.vijaya_muhurta?.start} - ${muhurtha.data.vijaya_muhurta?.end}`}
                      />
                      <DataRow 
                        label="Godhuli Muhurta" 
                        value={`${muhurtha.data.godhuli_muhurta?.start} - ${muhurtha.data.godhuli_muhurta?.end}`}
                      />
                      <DataRow 
                        label="Nishita Kala" 
                        value={`${muhurtha.data.nishita_kala?.start} - ${muhurtha.data.nishita_kala?.end}`}
                      />
                      <DataRow 
                        label="Durmuhurta" 
                        value={`${muhurtha.data.durmuhurta?.start} - ${muhurtha.data.durmuhurta?.end}`}
                      />
                    </CardContent>
                  </Card>

                  <Card className="col-span-1 row-span-2">
                    <CardHeader>
                      <CardTitle className="text-lg">All 30 Muhurthas</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-2 max-h-96 overflow-y-auto">
                        {muhurtha.data.all_muhurthas?.map((m: any, i: number) => (
                          <div key={i} className="p-2 border rounded text-sm">
                            <div className="flex items-center justify-between">
                              <span className="font-semibold">{m.number}. {m.name}</span>
                              <span className="text-xs px-2 py-0.5 bg-primary/10 rounded">{m.period}</span>
                            </div>
                            <div className="text-xs text-muted-foreground mt-1">
                              {m.start} - {m.end}
                            </div>
                            <div className="text-xs text-muted-foreground">
                              Quality: {m.quality}
                            </div>
                          </div>
                        ))}
                      </div>
                    </CardContent>
                  </Card>
                </div>
              ) : (
                <EmptyState message="Click Calculate to view muhurtha timings" />
              )}
            </TabsContent>

            {/* Extended Features Tab */}
            <TabsContent value="extended" className="space-y-4">
              {extended.data?.extended_features ? (
                <div className="grid grid-cols-3 gap-4">
                  <Card>
                    <CardHeader>
                      <CardTitle className="text-lg">Tamil Calendar</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-2">
                      <DataRow label="Month" value={extended.data.extended_features.tamil_calendar?.month} />
                      <DataRow label="Date" value={extended.data.extended_features.tamil_calendar?.date} />
                      <DataRow label="Year" value={extended.data.extended_features.tamil_calendar?.year} />
                      <DataRow label="Tamil Yogam" value={extended.data.extended_features.tamil_yogam?.name || extended.data.extended_features.tamil_yogam} />
                      <DataRow label="Tamil Jaamam" value={extended.data.extended_features.tamil_jaamam} />
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader>
                      <CardTitle className="text-lg">Balas & Thaara</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-2">
                      <DataRow label="Thaarabalam" value={extended.data.extended_features.thaarabalam} />
                      <DataRow label="Chandrabalam" value={extended.data.extended_features.chandrabalam} />
                      <DataRow label="Chandrashtama" value={extended.data.extended_features.chandrashtama} />
                      <DataRow label="Nava Thaara" value={extended.data.extended_features.nava_thaara} />
                      <DataRow label="Special Thaara" value={extended.data.extended_features.special_thaara} />
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader>
                      <CardTitle className="text-lg">Yogas & Times</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-2">
                      <DataRow label="Anandhaadhi Yoga" value={extended.data.extended_features.anandhaadhi_yoga} />
                      <DataRow label="Triguna" value={extended.data.extended_features.triguna} />
                      <DataRow label="Karaka Tithi" value={extended.data.extended_features.karaka_tithi} />
                      <DataRow label="Karaka Yogam" value={extended.data.extended_features.karaka_yogam} />
                      <DataRow label="Panchaka Rahitha" value={extended.data.extended_features.panchaka_rahitha} />
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader>
                      <CardTitle className="text-lg">Calendar Info</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-2">
                      <DataRow label="Lunar Month" value={extended.data.extended_features.lunar_month} />
                      <DataRow label="Ritu (Season)" value={extended.data.extended_features.ritu} />
                      <DataRow label="Samvatsara" value={extended.data.extended_features.samvatsara} />
                      <DataRow label="Day Length" value={extended.data.extended_features.day_length} />
                      <DataRow label="Night Length" value={extended.data.extended_features.night_length} />
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader>
                      <CardTitle className="text-lg">Special Timings</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-2">
                      <DataRow label="Midday" value={extended.data.extended_features.midday} />
                      <DataRow label="Midnight" value={extended.data.extended_features.midnight} />
                      <DataRow 
                        label="Amrita Gadiya" 
                        value={extended.data.extended_features.amrita_gadiya ? 
                          `${extended.data.extended_features.amrita_gadiya.start} - ${extended.data.extended_features.amrita_gadiya.end}` : 
                          'N/A'
                        } 
                      />
                      <DataRow 
                        label="Varjyam" 
                        value={extended.data.extended_features.varjyam ? 
                          `${extended.data.extended_features.varjyam.start} - ${extended.data.extended_features.varjyam.end}` : 
                          'N/A'
                        } 
                      />
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader>
                      <CardTitle className="text-lg">Choghadiya & Hora</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-2">
                      <div className="text-sm">
                        <div className="font-semibold mb-2">Gauri Choghadiya</div>
                        <pre className="text-xs bg-muted p-2 rounded overflow-x-auto">
                          {JSON.stringify(extended.data.extended_features.gauri_choghadiya, null, 2)}
                        </pre>
                      </div>
                      <div className="text-sm">
                        <div className="font-semibold mb-2">Shubha Hora</div>
                        <pre className="text-xs bg-muted p-2 rounded overflow-x-auto">
                          {JSON.stringify(extended.data.extended_features.shubha_hora, null, 2)}
                        </pre>
                      </div>
                    </CardContent>
                  </Card>
                </div>
              ) : (
                <EmptyState message="Click Calculate to view extended panchanga features" />
              )}
            </TabsContent>

            {/* Eclipses Tab */}
            <TabsContent value="eclipses" className="space-y-4">
              {eclipses.data?.eclipse_info ? (
                <div className="grid grid-cols-2 gap-4">
                  <Card>
                    <CardHeader>
                      <CardTitle className="text-lg">Solar Eclipse</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-3">
                      <DataRow 
                        label="Eclipse Today" 
                        value={eclipses.data.eclipse_info.is_solar_eclipse_today ? 'Yes' : 'No'}
                        className={eclipses.data.eclipse_info.is_solar_eclipse_today ? 'text-destructive font-bold' : ''}
                      />
                      <Separator />
                      <div className="text-sm font-semibold">Next Solar Eclipse</div>
                      <DataRow label="Date" value={eclipses.data.eclipse_info.next_solar_eclipse?.date} />
                      <DataRow label="Julian Day" value={eclipses.data.eclipse_info.next_solar_eclipse?.jd?.toFixed(4)} />
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader>
                      <CardTitle className="text-lg">Lunar Eclipse</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-3">
                      <div className="text-sm font-semibold">Next Lunar Eclipse</div>
                      <DataRow label="Date" value={eclipses.data.eclipse_info.next_lunar_eclipse?.date} />
                      <DataRow label="Julian Day" value={eclipses.data.eclipse_info.next_lunar_eclipse?.jd?.toFixed(4)} />
                    </CardContent>
                  </Card>
                </div>
              ) : (
                <EmptyState message="Click Calculate to view eclipse information" />
              )}
            </TabsContent>

            {/* Sankranti Tab */}
            <TabsContent value="sankranti" className="space-y-4">
              {sankranti.data?.sankranti_info ? (
                <div className="grid grid-cols-2 gap-4">
                  <Card>
                    <CardHeader>
                      <CardTitle className="text-lg">Previous Sankranti</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-2">
                      <DataRow label="Date" value={sankranti.data.sankranti_info.previous_sankranti?.date} />
                      <DataRow label="Rasi" value={sankranti.data.sankranti_info.previous_sankranti?.rasi} />
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader>
                      <CardTitle className="text-lg">Next Sankranti</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-2">
                      <DataRow label="Date" value={sankranti.data.sankranti_info.next_sankranti?.date} />
                      <DataRow label="Rasi" value={sankranti.data.sankranti_info.next_sankranti?.rasi} />
                    </CardContent>
                  </Card>
                </div>
              ) : (
                <EmptyState message="Click Calculate to view sankranti dates" />
              )}
            </TabsContent>

            {/* Retrograde Tab */}
            <TabsContent value="retrograde" className="space-y-4">
              {retrograde.data?.retrograde_info ? (
                <div className="grid grid-cols-2 gap-4">
                  <Card>
                    <CardHeader>
                      <CardTitle className="text-lg">Retrograde Planets</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-2">
                        {retrograde.data.retrograde_info.retrograde_planets ? (
                          <pre className="text-xs bg-muted p-3 rounded overflow-x-auto">
                            {JSON.stringify(retrograde.data.retrograde_info.retrograde_planets, null, 2)}
                          </pre>
                        ) : (
                          <div className="text-sm text-muted-foreground">No retrograde planets</div>
                        )}
                      </div>
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader>
                      <CardTitle className="text-lg">Planet Speeds</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-2">
                        {retrograde.data.retrograde_info.planet_speeds ? (
                          <pre className="text-xs bg-muted p-3 rounded overflow-x-auto max-h-64 overflow-y-auto">
                            {JSON.stringify(retrograde.data.retrograde_info.planet_speeds, null, 2)}
                          </pre>
                        ) : (
                          <div className="text-sm text-muted-foreground">No speed data available</div>
                        )}
                      </div>
                    </CardContent>
                  </Card>

                  <Card className="col-span-2">
                    <CardHeader>
                      <CardTitle className="text-lg">Graha Yudh (Planetary War)</CardTitle>
                    </CardHeader>
                    <CardContent>
                      {retrograde.data.retrograde_info.graha_yudh ? (
                        <pre className="text-xs bg-muted p-3 rounded overflow-x-auto">
                          {JSON.stringify(retrograde.data.retrograde_info.graha_yudh, null, 2)}
                        </pre>
                      ) : (
                        <div className="text-sm text-muted-foreground">No planetary war detected</div>
                      )}
                    </CardContent>
                  </Card>
                </div>
              ) : (
                <EmptyState message="Click Calculate to view retrograde information" />
              )}
            </TabsContent>
          </Tabs>
        </div>
      </main>
    </div>
  );
}

// Helper components
const DataRow = ({ label, value, className = '' }: { label: string; value: any; className?: string }) => (
  <div className={`flex justify-between text-sm ${className}`}>
    <span className="text-muted-foreground">{label}:</span>
    <span className="font-medium">{value || 'N/A'}</span>
  </div>
);

const EmptyState = ({ message }: { message: string }) => (
  <Card>
    <CardContent className="py-12">
      <div className="text-center text-muted-foreground">{message}</div>
    </CardContent>
  </Card>
);
