import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { PanchangaResponse } from '@/lib/api/panchanga';

interface NatalPanchangaProps {
    data: PanchangaResponse | null;
    extendedData?: any;
    isLoading: boolean;
}

export function NatalPanchanga({ data, extendedData, isLoading }: NatalPanchangaProps) {
    if (isLoading) {
        return (
            <div className="h-full flex items-center justify-center text-xs text-muted-foreground">
                Loading...
            </div>
        );
    }

    if (!data) {
        return (
            <div className="h-full flex items-center justify-center text-xs text-muted-foreground">
                No Data
            </div>
        );
    }

    // Helper to calculate Janma Ghatis (approximate)
    const calculateJanmaGhatis = () => {
        if (!data.sunrise || !data.time) return "N/A";
        try {
            const [birthH, birthM, birthS] = data.time.split(':').map(Number);
            const [riseH, riseM, riseS] = data.sunrise.split(':').map(Number);

            let birthMin = birthH * 60 + birthM + birthS / 60;
            let riseMin = riseH * 60 + riseM + riseS / 60;

            if (birthMin < riseMin) birthMin += 24 * 60; // Next day or same day early morning

            const diffMin = birthMin - riseMin;
            const ghatis = diffMin / 24; // 1 Ghati = 24 mins
            return ghatis.toFixed(4);
        } catch (e) {
            return "N/A";
        }
    };

    // Helper to format time
    const formatTime = (timeStr: string) => {
        if (!timeStr) return "";
        const [h, m, s] = timeStr.split(':');
        return `${h}:${m}:${s}`; // Already in HH:MM:SS
    };

    const ext = extendedData?.extended_features || {};

    return (
        <div className="grid grid-cols-2 gap-x-4 gap-y-1 text-xs p-2">
            <div className="font-semibold text-primary">Date:</div>
            <div>{data.date}</div>

            <div className="font-semibold text-primary">Time:</div>
            <div>{data.time}</div>

            <div className="font-semibold text-primary">Time Zone:</div>
            <div>{data.place.timezone} (West of GMT)</div>

            <div className="font-semibold text-primary">Place:</div>
            <div className="truncate" title={`${data.place.name}, ${data.place.latitude}, ${data.place.longitude}`}>
                {data.place.name}
            </div>

            <div className="font-semibold text-primary">Lunar Yr-Mo:</div>
            <div>
                {ext.samvatsara || 'N/A'} - {Array.isArray(ext.lunar_month) ? (ext.lunar_month[1] || ext.lunar_month[0]) : (ext.lunar_month || 'N/A')}
            </div>

            <div className="font-semibold text-primary">Tithi:</div>
            <div>{data.tithi.name} ({data.tithi.paksha})</div>

            <div className="font-semibold text-primary">Vedic Weekday:</div>
            <div>{data.vaara}</div>

            <div className="font-semibold text-primary">Nakshatra:</div>
            <div>{data.nakshatra.name}</div>

            <div className="font-semibold text-primary">Yoga:</div>
            <div>{data.yoga.name}</div>

            <div className="font-semibold text-primary">Karana:</div>
            <div>{data.karana.name}</div>

            <div className="font-semibold text-primary">Hora Lord:</div>
            <div>{data.hora_lord || 'N/A'}</div>

            <div className="font-semibold text-primary">Mahakala Hora:</div>
            <div title={ext.mahakala_hora ? JSON.stringify(ext.mahakala_hora) : ''}>
                {ext.mahakala_hora ? `${ext.mahakala_hora.lord} (${ext.mahakala_hora.start}-${ext.mahakala_hora.end})` : 'N/A'}
            </div>

            <div className="font-semibold text-primary">Kaala Lord:</div>
            <div>{ext.kaala_lord || 'N/A'}</div>

            <div className="font-semibold text-primary">Gouri Panchanga:</div>
            <div>
                {ext.gauri_choghadiya && !Array.isArray(ext.gauri_choghadiya) ?
                    `${ext.gauri_choghadiya.name} (${ext.gauri_choghadiya.start}-${ext.gauri_choghadiya.end})`
                    : (ext.gauri_choghadiya ? 'Available' : 'N/A')}
            </div>

            <div className="font-semibold text-primary">Sunrise:</div>
            <div>{formatTime(data.sunrise)}</div>

            <div className="font-semibold text-primary">Sunset:</div>
            <div>{formatTime(data.sunset)}</div>

            <div className="font-semibold text-primary">Janma Ghatis:</div>
            <div>{calculateJanmaGhatis()}</div>

            <div className="font-semibold text-primary">Ayanamsa:</div>
            <div>{data.ayanamsa_value.toFixed(6)}</div>

            <div className="font-semibold text-primary">Sid Time:</div>
            <div>{data.sidereal_time || 'N/A'}</div>

            <div className="font-semibold text-primary">Karaka Tithi:</div>
            <div>{ext.karaka_tithi?.name || 'N/A'}</div>

            <div className="font-semibold text-primary">Karaka Yoga:</div>
            <div>{ext.karaka_yogam?.name || 'N/A'}</div>
        </div>
    );
}
