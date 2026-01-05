'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';

interface PanchangaData {
  tithi?: {
    number: number;
    name: string;
    paksha: string;
    end_time: string;
  };
  nakshatra?: {
    number: number;
    name: string;
    pada: number;
    lord: string;
    end_time: string;
  };
  yoga?: {
    number: number;
    name: string;
    end_time: string;
  };
  karana?: {
    number: number;
    name: string;
    start_time: string;
    end_time: string;
  };
  vaara?: string;
  sunrise?: string;
  sunset?: string;
  moonrise?: string;
  moonset?: string;
  rahu_kala?: {
    start: string;
    end: string;
  };
  yamaganda?: {
    start: string;
    end: string;
  };
  gulika?: {
    start: string;
    end: string;
  };
  abhijit_muhurta?: {
    start: string;
    end: string;
  };
  tithi_details?: {
    deity: string;
    lord: string;
  };
  nakshatra_details?: {
    deity: string;
  };
  yoga_details?: {
    quality: string;
  };
  karana_details?: {
    lord: string;
  };
  ayanamsa_value?: number;
  julian_day?: number;
}

interface PanchangaDisplayProps {
  data: PanchangaData | null;
  isLoading?: boolean;
}

export const PanchangaDisplay = ({ data, isLoading = false }: PanchangaDisplayProps) => {
  if (isLoading) {
    return (
      <Card className="m-4 border-none shadow-none">
        <CardHeader className="pb-3">
          <CardTitle className="text-sm">Panchanga</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-xs text-muted-foreground">Calculating panchanga...</div>
        </CardContent>
      </Card>
    );
  }

  if (!data) {
    return (
      <Card className="m-4 border-none shadow-none">
        <CardHeader className="pb-3">
          <CardTitle className="text-sm">Panchanga</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-xs text-muted-foreground">Click Calculate to view panchanga</div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="m-4 border-none shadow-none">
      <CardHeader className="pb-3">
        <CardTitle className="text-sm">Panchanga</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-2 text-xs">
          {/* Basic Panchanga */}
          {data.tithi && (
            <div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Tithi:</span>
                <span className="font-medium">{data.tithi.name}</span>
              </div>
              <div className="flex justify-between text-[10px] text-muted-foreground">
                <span>Paksha: {data.tithi.paksha}</span>
                {data.tithi_details && <span>Lord: {data.tithi_details.lord}</span>}
              </div>
            </div>
          )}
          
          {data.nakshatra && (
            <div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Nakshatra:</span>
                <span className="font-medium">{data.nakshatra.name}</span>
              </div>
              <div className="flex justify-between text-[10px] text-muted-foreground">
                <span>Pada: {data.nakshatra.pada}</span>
                <span>Lord: {data.nakshatra.lord}</span>
              </div>
            </div>
          )}
          
          {data.yoga && (
            <div className="flex justify-between">
              <span className="text-muted-foreground">Yoga:</span>
              <span className="font-medium">{data.yoga.name}</span>
            </div>
          )}
          
          {data.karana && (
            <div className="flex justify-between">
              <span className="text-muted-foreground">Karana:</span>
              <span className="font-medium">{data.karana.name}</span>
            </div>
          )}
          
          {data.vaara && (
            <div className="flex justify-between">
              <span className="text-muted-foreground">Vaara:</span>
              <span className="font-medium">{data.vaara}</span>
            </div>
          )}

          <Separator className="my-2" />

          {/* Sunrise/Sunset */}
          {data.sunrise && (
            <div className="flex justify-between">
              <span className="text-muted-foreground">Sunrise:</span>
              <span>{data.sunrise}</span>
            </div>
          )}
          {data.sunset && (
            <div className="flex justify-between">
              <span className="text-muted-foreground">Sunset:</span>
              <span>{data.sunset}</span>
            </div>
          )}
          {data.moonrise && (
            <div className="flex justify-between">
              <span className="text-muted-foreground">Moonrise:</span>
              <span>{data.moonrise}</span>
            </div>
          )}
          {data.moonset && (
            <div className="flex justify-between">
              <span className="text-muted-foreground">Moonset:</span>
              <span>{data.moonset}</span>
            </div>
          )}

          <Separator className="my-2" />

          {/* Inauspicious Times */}
          {data.rahu_kala && (
            <div className="flex justify-between">
              <span className="text-muted-foreground">Rahu Kala:</span>
              <span className="text-[10px]">{data.rahu_kala.start} - {data.rahu_kala.end}</span>
            </div>
          )}
          {data.yamaganda && (
            <div className="flex justify-between">
              <span className="text-muted-foreground">Yamaganda:</span>
              <span className="text-[10px]">{data.yamaganda.start} - {data.yamaganda.end}</span>
            </div>
          )}
          {data.gulika && (
            <div className="flex justify-between">
              <span className="text-muted-foreground">Gulika:</span>
              <span className="text-[10px]">{data.gulika.start} - {data.gulika.end}</span>
            </div>
          )}

          {data.abhijit_muhurta && (
            <>
              <Separator className="my-2" />
              <div className="flex justify-between text-green-600 dark:text-green-400">
                <span className="font-medium">Abhijit Muhurta:</span>
                <span className="text-[10px]">{data.abhijit_muhurta.start} - {data.abhijit_muhurta.end}</span>
              </div>
            </>
          )}
        </div>
      </CardContent>
    </Card>
  );
};
