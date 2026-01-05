'use client';

import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { panchangaApi, type PanchangaRequest } from '@/lib/api/panchanga';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Button } from '@/components/ui/button';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Separator } from '@/components/ui/separator';
import { Badge } from '@/components/ui/badge';

export default function PanchangaTab() {
  const [formData, setFormData] = useState<PanchangaRequest>({
    date: new Date().toISOString().split('T')[0],
    time: new Date().toTimeString().split(' ')[0].slice(0, 8),
    place: {
      name: 'Chennai',
      latitude: 13.0827,
      longitude: 80.2707,
      timezone: 5.5,
    },
    ayanamsa: 'LAHIRI',
  });

  const [shouldFetch, setShouldFetch] = useState(false);

  const { data, isLoading, error, refetch } = useQuery({
    queryKey: [
      'panchanga',
      formData.date,
      formData.time,
      formData.place.latitude,
      formData.place.longitude,
      formData.place.timezone,
      formData.ayanamsa
    ],
    queryFn: () => panchangaApi.calculate(formData),
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
          <CardTitle>Input Details</CardTitle>
          <CardDescription>Enter date, time, and location</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="date">Date</Label>
              <Input
                id="date"
                type="date"
                value={formData.date}
                onChange={(e) => setFormData({ ...formData, date: e.target.value })}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="time">Time</Label>
              <Input
                id="time"
                type="time"
                step="1"
                value={formData.time.slice(0, 5)}
                onChange={(e) => setFormData({ ...formData, time: e.target.value + ':00' })}
              />
            </div>

            <Separator />

            <div className="space-y-2">
              <Label htmlFor="place">Place</Label>
              <Input
                id="place"
                value={formData.place.name}
                onChange={(e) => setFormData({ ...formData, place: { ...formData.place, name: e.target.value } })}
                placeholder="City name"
              />
            </div>

            <div className="grid grid-cols-2 gap-2">
              <div className="space-y-2">
                <Label htmlFor="lat">Latitude</Label>
                <Input
                  id="lat"
                  type="number"
                  step="0.0001"
                  value={formData.place.latitude}
                  onChange={(e) => setFormData({ ...formData, place: { ...formData.place, latitude: parseFloat(e.target.value) } })}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="lon">Longitude</Label>
                <Input
                  id="lon"
                  type="number"
                  step="0.0001"
                  value={formData.place.longitude}
                  onChange={(e) => setFormData({ ...formData, place: { ...formData.place, longitude: parseFloat(e.target.value) } })}
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="tz">Timezone</Label>
              <Input
                id="tz"
                type="number"
                step="0.5"
                value={formData.place.timezone}
                onChange={(e) => setFormData({ ...formData, place: { ...formData.place, timezone: parseFloat(e.target.value) } })}
              />
            </div>

            <Button type="submit" className="w-full" disabled={isLoading}>
              {isLoading ? 'Calculating...' : 'Calculate'}
            </Button>
          </form>
        </CardContent>
      </Card>

      {/* Results */}
      <Card className="lg:col-span-2">
        <CardHeader>
          <CardTitle>Panchanga Results</CardTitle>
          <CardDescription>
            {data && `${data.place.name} - ${data.date}`}
          </CardDescription>
        </CardHeader>
        <CardContent>
          {error && (
            <div className="rounded-md bg-destructive/10 p-4 text-sm text-destructive">
              Error: {error instanceof Error ? error.message : 'Failed to calculate'}
            </div>
          )}

          {data && (
            <div className="space-y-6">
              {/* Sun & Moon Times */}
              <div>
                <h3 className="text-sm font-medium mb-3">Sun & Moon</h3>
                <Table>
                  <TableBody>
                    <TableRow>
                      <TableCell className="font-medium">Sunrise</TableCell>
                      <TableCell>{data.sunrise}</TableCell>
                      <TableCell className="font-medium">Sunset</TableCell>
                      <TableCell>{data.sunset}</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell className="font-medium">Moonrise</TableCell>
                      <TableCell>{data.moonrise || 'N/A'}</TableCell>
                      <TableCell className="font-medium">Moonset</TableCell>
                      <TableCell>{data.moonset || 'N/A'}</TableCell>
                    </TableRow>
                  </TableBody>
                </Table>
              </div>

              <Separator />

              {/* Panchanga Elements */}
              <div>
                <h3 className="text-sm font-medium mb-3">Panchanga</h3>
                <Table>
                  <TableBody>
                    <TableRow>
                      <TableCell className="font-medium w-32">Tithi</TableCell>
                      <TableCell>
                        <div className="flex items-center gap-2">
                          {data.tithi.name}
                          <Badge variant="secondary">{data.tithi.paksha}</Badge>
                        </div>
                      </TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell className="font-medium">Nakshatra</TableCell>
                      <TableCell>
                        {data.nakshatra.name} - Pada {data.nakshatra.pada} (Lord: {data.nakshatra.lord})
                      </TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell className="font-medium">Yoga</TableCell>
                      <TableCell>{data.yoga.name}</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell className="font-medium">Karana</TableCell>
                      <TableCell>{data.karana.name}</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell className="font-medium">Vaara</TableCell>
                      <TableCell>{data.vaara}</TableCell>
                    </TableRow>
                  </TableBody>
                </Table>
              </div>

              <Separator />

              {/* Special Timings */}
              <div>
                <h3 className="text-sm font-medium mb-3">Special Timings (Inauspicious)</h3>
                <Table>
                  <TableBody>
                    <TableRow>
                      <TableCell className="font-medium w-32">Rahu Kala</TableCell>
                      <TableCell>{data.rahu_kala.start} - {data.rahu_kala.end}</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell className="font-medium">Yamaganda</TableCell>
                      <TableCell>{data.yamaganda.start} - {data.yamaganda.end}</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell className="font-medium">Gulika</TableCell>
                      <TableCell>{data.gulika.start} - {data.gulika.end}</TableCell>
                    </TableRow>
                  </TableBody>
                </Table>
              </div>

              <Separator />

              {/* Additional Info */}
              <div>
                <h3 className="text-sm font-medium mb-3">Additional Information</h3>
                <Table>
                  <TableBody>
                    <TableRow>
                      <TableCell className="font-medium w-32">Ayanamsa</TableCell>
                      <TableCell>{data.ayanamsa_value.toFixed(6)}° ({formData.ayanamsa})</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell className="font-medium">Julian Day</TableCell>
                      <TableCell>{data.julian_day.toFixed(6)}</TableCell>
                    </TableRow>
                  </TableBody>
                </Table>
              </div>
            </div>
          )}

          {!data && !error && !isLoading && (
            <div className="text-center py-12 text-muted-foreground">
              Enter details and click Calculate to see results
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}


