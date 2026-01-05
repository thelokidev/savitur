'use client';

import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { yogasApi, type YogaRequest } from '@/lib/api/yogas';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Button } from '@/components/ui/button';
import { Separator } from '@/components/ui/separator';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';

export default function YogaTab() {
  const [formData, setFormData] = useState<YogaRequest>({
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

  const [shouldFetch, setShouldFetch] = useState(false);

  const { data, isLoading, error, refetch } = useQuery({
    queryKey: [
      'yogas',
      formData.birth_details.date,
      formData.birth_details.time,
      formData.birth_details.place.latitude,
      formData.birth_details.place.longitude,
      formData.birth_details.place.timezone,
      formData.ayanamsa
    ],
    queryFn: () => yogasApi.getAllYogasAndDoshas(formData),
    enabled: shouldFetch,
    refetchOnWindowFocus: false,
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setShouldFetch(true);
    refetch();
  };

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
              <Label htmlFor="ydate">Date of Birth</Label>
              <Input
                id="ydate"
                type="date"
                value={formData.birth_details.date}
                onChange={(e) => setFormData({
                  ...formData,
                  birth_details: { ...formData.birth_details, date: e.target.value }
                })}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="ytime">Time of Birth</Label>
              <Input
                id="ytime"
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
              <Label htmlFor="yplace">Place of Birth</Label>
              <Input
                id="yplace"
                value={formData.birth_details.place.name}
                onChange={(e) => setFormData({
                  ...formData,
                  birth_details: {
                    ...formData.birth_details,
                    place: { ...formData.birth_details.place, name: e.target.value }
                  }
                })}
              />
            </div>

            <div className="grid grid-cols-2 gap-2">
              <div className="space-y-2">
                <Label htmlFor="ylat">Latitude</Label>
                <Input
                  id="ylat"
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
                <Label htmlFor="ylon">Longitude</Label>
                <Input
                  id="ylon"
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

            <Button type="submit" className="w-full" disabled={isLoading}>
              {isLoading ? 'Analyzing...' : 'Analyze Yogas & Doshas'}
            </Button>
          </form>
        </CardContent>
      </Card>

      {/* Results */}
      <Card className="lg:col-span-2">
        <CardHeader>
          <CardTitle>Yoga & Dosha Analysis</CardTitle>
          <CardDescription>
            {data && `Found ${data.total_yogas || 0} yogas and ${data.doshas?.length || 0} doshas`}
          </CardDescription>
        </CardHeader>
        <CardContent>
          {error && (
            <div className="rounded-md bg-destructive/10 p-4 text-sm text-destructive">
              Error: {error instanceof Error ? error.message : 'Failed to analyze'}
            </div>
          )}

          {data && (
            <Tabs defaultValue="yogas" className="space-y-4">
              <TabsList>
                <TabsTrigger value="yogas">All Yogas ({data.total_yogas || 0})</TabsTrigger>
                <TabsTrigger value="raja">Raja Yogas ({data.raja_yogas?.length || 0})</TabsTrigger>
                <TabsTrigger value="doshas">Doshas ({data.doshas?.length || 0})</TabsTrigger>
              </TabsList>

              <TabsContent value="yogas" className="space-y-4">
                <div className="max-h-[600px] overflow-y-auto">
                  {data.yogas && data.yogas.length > 0 ? (
                    <table className="w-full text-sm">
                      <thead className="sticky top-0 bg-background border-b">
                        <tr className="text-left">
                          <th className="py-2 px-2 font-semibold text-primary">Yoga</th>
                          <th className="py-2 px-2 font-semibold">Varga</th>
                          <th className="py-2 px-2 font-semibold">Yoga Givers</th>
                          <th className="py-2 px-2 font-semibold">Results ascribed to yoga</th>
                          <th className="py-2 px-2 font-semibold">Brief definition of yoga</th>
                        </tr>
                      </thead>
                      <tbody>
                        {data.yogas.map((yoga, idx) => (
                          <tr key={idx} className="border-b border-border/50 hover:bg-muted/30 transition-colors">
                            <td className="py-2 px-2">
                              <span className="text-blue-500 hover:underline cursor-pointer font-medium">
                                {yoga.name}
                              </span>
                            </td>
                            <td className="py-2 px-2 text-muted-foreground">
                              D-1
                            </td>
                            <td className="py-2 px-2 text-muted-foreground">
                              {yoga.planets?.join(', ') || yoga.planet || '-'}
                            </td>
                            <td className="py-2 px-2 text-muted-foreground">
                              {yoga.impact || yoga.quality || yoga.category || '-'}
                            </td>
                            <td className="py-2 px-2 text-muted-foreground">
                              {yoga.description}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  ) : (
                    <p className="text-center py-8 text-muted-foreground">No yogas found</p>
                  )}
                </div>
              </TabsContent>

              <TabsContent value="raja" className="space-y-4">
                <div className="max-h-[600px] overflow-y-auto">
                  {data.raja_yogas && data.raja_yogas.length > 0 ? (
                    <table className="w-full text-sm">
                      <thead className="sticky top-0 bg-background border-b">
                        <tr className="text-left">
                          <th className="py-2 px-2 font-semibold text-yellow-500">Raja Yoga</th>
                          <th className="py-2 px-2 font-semibold">Varga</th>
                          <th className="py-2 px-2 font-semibold">Yoga Givers</th>
                          <th className="py-2 px-2 font-semibold">Results ascribed to yoga</th>
                          <th className="py-2 px-2 font-semibold">Brief definition of yoga</th>
                        </tr>
                      </thead>
                      <tbody>
                        {data.raja_yogas.map((yoga, idx) => (
                          <tr key={idx} className="border-b border-yellow-500/20 hover:bg-yellow-500/5 transition-colors">
                            <td className="py-2 px-2">
                              <span className="text-yellow-500 hover:underline cursor-pointer font-medium">
                                {yoga.name}
                              </span>
                            </td>
                            <td className="py-2 px-2 text-muted-foreground">
                              D-1
                            </td>
                            <td className="py-2 px-2 text-muted-foreground">
                              {yoga.planets?.join(', ') || yoga.planet || '-'}
                            </td>
                            <td className="py-2 px-2 text-muted-foreground">
                              {yoga.impact || yoga.quality || 'Raja Yoga'}
                            </td>
                            <td className="py-2 px-2 text-muted-foreground">
                              {yoga.description}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  ) : (
                    <p className="text-center py-8 text-muted-foreground">No raja yogas found</p>
                  )}
                </div>
              </TabsContent>

              <TabsContent value="doshas" className="space-y-4">
                <div className="max-h-[600px] overflow-y-auto space-y-3">
                  {data.doshas && data.doshas.length > 0 ? (
                    data.doshas.map((dosha, idx) => (
                      <div key={idx} className="border rounded-lg p-4 border-red-500/20 bg-red-500/5">
                        <div className="flex items-start justify-between mb-2">
                          <h4 className="font-medium">{dosha.name}</h4>
                          <Badge variant="destructive">Dosha</Badge>
                        </div>
                        <p className="text-sm text-muted-foreground">{dosha.description}</p>
                      </div>
                    ))
                  ) : (
                    <p className="text-center py-8 text-muted-foreground">No doshas found</p>
                  )}
                </div>
              </TabsContent>
            </Tabs>
          )}

          {!data && !error && !isLoading && (
            <div className="text-center py-12 text-muted-foreground">
              Enter birth details to analyze yogas and doshas
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

