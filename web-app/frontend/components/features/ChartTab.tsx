'use client';

import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { chartsApi, type ChartRequest } from '@/lib/api/charts';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Button } from '@/components/ui/button';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Separator } from '@/components/ui/separator';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';

export default function ChartTab() {
  const [formData, setFormData] = useState<ChartRequest>({
    birth_details: {
      date: '1990-01-15',
      time: '10:30:00',
      place: {
        name: 'Chennai',
        latitude: 13.0827,
        longitude: 80.2707,
        timezone: 5.5,
      },
    },
    ayanamsa: 'LAHIRI',
  });

  const [selectedChart, setSelectedChart] = useState<number>(1);
  const [shouldFetch, setShouldFetch] = useState(false);

  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['chart', formData, selectedChart],
    queryFn: () => selectedChart === 1 
      ? chartsApi.getRasiChart(formData)
      : chartsApi.getDivisionalChart(selectedChart, formData),
    enabled: shouldFetch,
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setShouldFetch(true);
    refetch();
  };

  const divisionalCharts = [
    { num: 1, name: 'Rasi (D-1)' },
    { num: 2, name: 'Hora (D-2)' },
    { num: 3, name: 'Drekkana (D-3)' },
    { num: 4, name: 'Chaturthamsa (D-4)' },
    { num: 7, name: 'Saptamsa (D-7)' },
    { num: 9, name: 'Navamsa (D-9)' },
    { num: 10, name: 'Dasamsa (D-10)' },
    { num: 12, name: 'Dwadasamsa (D-12)' },
    { num: 16, name: 'Shodasamsa (D-16)' },
    { num: 20, name: 'Vimsamsa (D-20)' },
    { num: 24, name: 'Chaturvimsamsa (D-24)' },
    { num: 27, name: 'Nakshatramsa (D-27)' },
    { num: 30, name: 'Trimsamsa (D-30)' },
    { num: 40, name: 'Khavedamsa (D-40)' },
    { num: 45, name: 'Akshavedamsa (D-45)' },
    { num: 60, name: 'Shashtyamsa (D-60)' },
  ];

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Input Form */}
      <Card className="lg:col-span-1">
        <CardHeader>
          <CardTitle>Birth Details</CardTitle>
          <CardDescription>Enter birth information</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="bdate">Date of Birth</Label>
              <Input
                id="bdate"
                type="date"
                value={formData.birth_details.date}
                onChange={(e) => setFormData({
                  ...formData,
                  birth_details: { ...formData.birth_details, date: e.target.value }
                })}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="btime">Time of Birth</Label>
              <Input
                id="btime"
                type="time"
                step="1"
                value={formData.birth_details.time.slice(0, 5)}
                onChange={(e) => setFormData({
                  ...formData,
                  birth_details: { ...formData.birth_details, time: e.target.value + ':00' }
                })}
              />
            </div>

            <Separator />

            <div className="space-y-2">
              <Label htmlFor="bplace">Place of Birth</Label>
              <Input
                id="bplace"
                value={formData.birth_details.place.name}
                onChange={(e) => setFormData({
                  ...formData,
                  birth_details: {
                    ...formData.birth_details,
                    place: { ...formData.birth_details.place, name: e.target.value }
                  }
                })}
                placeholder="City name"
              />
            </div>

            <div className="grid grid-cols-2 gap-2">
              <div className="space-y-2">
                <Label htmlFor="blat">Latitude</Label>
                <Input
                  id="blat"
                  type="number"
                  step="0.0001"
                  value={formData.birth_details.place.latitude}
                  onChange={(e) => setFormData({
                    ...formData,
                    birth_details: {
                      ...formData.birth_details,
                      place: { ...formData.birth_details.place, latitude: parseFloat(e.target.value) }
                    }
                  })}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="blon">Longitude</Label>
                <Input
                  id="blon"
                  type="number"
                  step="0.0001"
                  value={formData.birth_details.place.longitude}
                  onChange={(e) => setFormData({
                    ...formData,
                    birth_details: {
                      ...formData.birth_details,
                      place: { ...formData.birth_details.place, longitude: parseFloat(e.target.value) }
                    }
                  })}
                />
              </div>
            </div>

            <Separator />

            <div className="space-y-2">
              <Label>Select Chart</Label>
              <select
                value={selectedChart}
                onChange={(e) => setSelectedChart(parseInt(e.target.value))}
                className="w-full px-3 py-2 border border-input rounded-md bg-background"
              >
                {divisionalCharts.map(chart => (
                  <option key={chart.num} value={chart.num}>{chart.name}</option>
                ))}
              </select>
            </div>

            <Button type="submit" className="w-full" disabled={isLoading}>
              {isLoading ? 'Calculating...' : 'Calculate Chart'}
            </Button>
          </form>
        </CardContent>
      </Card>

      {/* Results */}
      <Card className="lg:col-span-2">
        <CardHeader>
          <CardTitle>Chart Results</CardTitle>
          <CardDescription>
            {data && `${data.chart_type} for ${formData.birth_details.place.name}`}
          </CardDescription>
        </CardHeader>
        <CardContent>
          {error && (
            <div className="rounded-md bg-destructive/10 p-4 text-sm text-destructive">
              Error: {error instanceof Error ? error.message : 'Failed to calculate'}
            </div>
          )}

          {data && (
            <Tabs defaultValue="positions" className="space-y-4">
              <TabsList>
                <TabsTrigger value="positions">Positions</TabsTrigger>
                <TabsTrigger value="houses">Houses</TabsTrigger>
              </TabsList>

              <TabsContent value="positions" className="space-y-4">
                <div>
                  <h3 className="text-sm font-medium mb-3">Ascendant</h3>
                  <Table>
                    <TableBody>
                      <TableRow>
                        <TableCell className="font-medium">Rasi</TableCell>
                        <TableCell>{data.ascendant.rasi_name}</TableCell>
                        <TableCell className="font-medium">Longitude</TableCell>
                        <TableCell>{data.ascendant.longitude.toFixed(4)}°</TableCell>
                      </TableRow>
                    </TableBody>
                  </Table>
                </div>

                <Separator />

                <div>
                  <h3 className="text-sm font-medium mb-3">Planet Positions</h3>
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>Planet</TableHead>
                        <TableHead>Rasi</TableHead>
                        <TableHead>Longitude</TableHead>
                        <TableHead>Degrees</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {data.planets.map((planet) => (
                        <TableRow key={planet.name}>
                          <TableCell className="font-medium">{planet.name}</TableCell>
                          <TableCell>{planet.rasi_name}</TableCell>
                          <TableCell>{planet.longitude.toFixed(4)}°</TableCell>
                          <TableCell>{planet.degrees_in_rasi.toFixed(2)}°</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              </TabsContent>

              <TabsContent value="houses">
                <div>
                  <h3 className="text-sm font-medium mb-3">House Placements</h3>
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>House</TableHead>
                        <TableHead>Planets</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {Object.entries(data.houses).map(([house, planets]) => (
                        <TableRow key={house}>
                          <TableCell className="font-medium">House {house}</TableCell>
                          <TableCell>{(planets as string[]).join(', ') || 'Empty'}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              </TabsContent>
            </Tabs>
          )}

          {!data && !error && !isLoading && (
            <div className="text-center py-12 text-muted-foreground">
              Enter birth details and select a chart to calculate
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}


