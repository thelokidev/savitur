'use client';

import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { compatibilityApi, type CompatibilityRequest } from '@/lib/api/compatibility';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Button } from '@/components/ui/button';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Separator } from '@/components/ui/separator';
import { Badge } from '@/components/ui/badge';

export default function CompatibilityTab() {
  const [formData, setFormData] = useState<Omit<CompatibilityRequest, 'compatibility_type'>>({
    boy: {
      date: '1990-01-15',
      time: '10:30:00',
      place: {
        name: 'Chennai',
        latitude: 13.0827,
        longitude: 80.2707,
        timezone: 5.5,
      },
    },
    girl: {
      date: '1992-03-20',
      time: '14:15:00',
      place: {
        name: 'Mumbai',
        latitude: 19.0760,
        longitude: 72.8777,
        timezone: 5.5,
      },
    },
    ayanamsa: 'LAHIRI',
  });

  const [method, setMethod] = useState<'north' | 'south'>('south');
  const [shouldFetch, setShouldFetch] = useState(false);

  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['compatibility', formData, method],
    queryFn: () => method === 'north' 
      ? compatibilityApi.getNorthIndian(formData)
      : compatibilityApi.getSouthIndian(formData),
    enabled: shouldFetch,
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
          <CardTitle>Partner Details</CardTitle>
          <CardDescription>Enter boy and girl birth details</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-3">
              <h4 className="font-medium">Boy Details</h4>
              <div className="space-y-2">
                <Label htmlFor="boydate">Date of Birth</Label>
                <Input
                  id="boydate"
                  type="date"
                  value={formData.boy.date}
                  onChange={(e) => setFormData({
                    ...formData,
                    boy: { ...formData.boy, date: e.target.value }
                  })}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="boytime">Time</Label>
                <Input
                  id="boytime"
                  type="time"
                  step="1"
                  value={formData.boy.time.slice(0, 5)}
                  onChange={(e) => setFormData({
                    ...formData,
                    boy: { ...formData.boy, time: e.target.value + ':00' }
                  })}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="boyplace">Place</Label>
                <Input
                  id="boyplace"
                  value={formData.boy.place.name}
                  onChange={(e) => setFormData({
                    ...formData,
                    boy: { ...formData.boy, place: { ...formData.boy.place, name: e.target.value } }
                  })}
                />
              </div>
            </div>

            <Separator />

            <div className="space-y-3">
              <h4 className="font-medium">Girl Details</h4>
              <div className="space-y-2">
                <Label htmlFor="girldate">Date of Birth</Label>
                <Input
                  id="girldate"
                  type="date"
                  value={formData.girl.date}
                  onChange={(e) => setFormData({
                    ...formData,
                    girl: { ...formData.girl, date: e.target.value }
                  })}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="girltime">Time</Label>
                <Input
                  id="girltime"
                  type="time"
                  step="1"
                  value={formData.girl.time.slice(0, 5)}
                  onChange={(e) => setFormData({
                    ...formData,
                    girl: { ...formData.girl, time: e.target.value + ':00' }
                  })}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="girlplace">Place</Label>
                <Input
                  id="girlplace"
                  value={formData.girl.place.name}
                  onChange={(e) => setFormData({
                    ...formData,
                    girl: { ...formData.girl, place: { ...formData.girl.place, name: e.target.value } }
                  })}
                />
              </div>
            </div>

            <Separator />

            <div className="space-y-2">
              <Label>Matching Method</Label>
              <select
                value={method}
                onChange={(e) => setMethod(e.target.value as 'north' | 'south')}
                className="w-full px-3 py-2 border border-input rounded-md bg-background"
              >
                <option value="south">South Indian</option>
                <option value="north">North Indian</option>
              </select>
            </div>

            <Button type="submit" className="w-full" disabled={isLoading}>
              {isLoading ? 'Calculating...' : 'Check Compatibility'}
            </Button>
          </form>
        </CardContent>
      </Card>

      {/* Results */}
      <Card className="lg:col-span-2">
        <CardHeader>
          <CardTitle>Compatibility Results</CardTitle>
          <CardDescription>
            {data && `${data.compatibility_type === 'north' ? 'North' : 'South'} Indian Method`}
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
              <div className="border rounded-lg p-6 text-center">
                <div className="text-4xl font-bold mb-2">
                  {data.total_score}/{data.max_score}
                </div>
                <div className="text-2xl font-medium mb-3">
                  {data.percentage?.toFixed(1) || 0}%
                </div>
                <Badge 
                  variant={data.compatible ? "default" : "destructive"}
                  className="text-lg px-4 py-1"
                >
                  {data.compatible ? 'Compatible' : 'Not Compatible'}
                </Badge>
              </div>

              <Separator />

              <div>
                <h3 className="text-sm font-medium mb-3">Compatibility Factors</h3>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Factor</TableHead>
                      <TableHead>Score</TableHead>
                      <TableHead>Max</TableHead>
                      <TableHead>Status</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {data.factors && data.factors.map((factor, idx) => (
                      <TableRow key={idx}>
                        <TableCell className="font-medium">{factor.name}</TableCell>
                        <TableCell>{factor.score}</TableCell>
                        <TableCell>{factor.max_score}</TableCell>
                        <TableCell>
                          <Badge variant={factor.compatible ? "default" : "secondary"}>
                            {factor.compatible ? '✓' : '✗'}
                          </Badge>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>

              <Separator />

              <div>
                <h3 className="text-sm font-medium mb-2">Recommendation</h3>
                <p className="text-sm text-muted-foreground">{data.recommendation}</p>
              </div>
            </div>
          )}

          {!data && !error && !isLoading && (
            <div className="text-center py-12 text-muted-foreground">
              Enter details for both partners to check compatibility
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

