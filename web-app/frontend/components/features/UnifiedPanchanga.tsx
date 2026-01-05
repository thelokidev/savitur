'use client';

import { ReactNode } from 'react';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
import { Badge } from '@/components/ui/badge';

type Tone = 'good' | 'bad' | 'neutral';

interface HighlightStat {
  label: string;
  value?: string;
  detail?: string;
  tone?: Tone;
}

const toneClasses: Record<Tone, string> = {
  good: 'border-green-200 bg-green-50 text-green-900 dark:border-green-900/40 dark:bg-green-900/20 dark:text-green-100',
  bad: 'border-red-200 bg-red-50 text-red-900 dark:border-red-900/40 dark:bg-red-900/20 dark:text-red-100',
  neutral: 'border-border bg-card text-foreground'
};

const StatChip = ({
  label,
  value,
  detail,
  tone = 'neutral'
}: {
  label: string;
  value?: string;
  detail?: string;
  tone?: Tone;
}) => (
  <div className={`rounded-xl border px-4 py-3 transition ${toneClasses[tone]}`}>
    <p className="text-xs uppercase tracking-wide text-muted-foreground">{label}</p>
    <p className="text-lg font-semibold">{value || '—'}</p>
    {detail && <p className="text-xs text-muted-foreground">{detail}</p>}
  </div>
);

const DataRow = ({
  label,
  value,
  helper,
  className = ''
}: {
  label: string;
  value?: ReactNode;
  helper?: string;
  className?: string;
}) => (
  <div className={`py-1 text-sm ${className}`}>
    <div className="flex justify-between items-start gap-4">
      <span className="text-muted-foreground">{label}</span>
      <span className="font-medium text-right">{value ?? '—'}</span>
    </div>
    {helper && <p className="text-xs text-muted-foreground mt-0.5">{helper}</p>}
  </div>
);

const SectionCard = ({
  title,
  description,
  rows,
  children
}: {
  title: string;
  description?: string;
  rows?: Array<{ label: string; value?: ReactNode; helper?: string }>;
  children?: ReactNode;
}) => (
  <Card>
    <CardHeader className="pb-2">
      <CardTitle className="text-base">{title}</CardTitle>
      {description && <p className="text-xs text-muted-foreground">{description}</p>}
    </CardHeader>
    <CardContent className="space-y-2 text-sm">
      {rows?.map((row) => (
        <DataRow key={row.label} label={row.label} value={row.value} helper={row.helper} />
      ))}
      {children}
    </CardContent>
  </Card>
);

interface UnifiedPanchangaProps {
  basicData: any;
  planetsData: any;
  muhurthaData: any;
  extendedData: any;
  eclipsesData: any;
  sankrantiData: any;
  retrogradeData: any;
  isLoading: boolean;
  mode?: 'natal' | 'daily';
  onModeChange?: (mode: 'natal' | 'daily') => void;
}

export function UnifiedPanchanga({
  basicData,
  planetsData,
  muhurthaData,
  extendedData,
  eclipsesData,
  sankrantiData,
  retrogradeData,
  isLoading,
  mode = 'daily',
  onModeChange
}: UnifiedPanchangaProps) {

  if (isLoading) {
    return (
      <div className="flex items-center justify-center p-12 text-muted-foreground">
        <div className="flex flex-col items-center gap-2">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
          <p>Calculating Panchanga...</p>
        </div>
      </div>
    );
  }

  if (!basicData) {
    return (
      <div className="flex items-center justify-center p-12 text-muted-foreground border-2 border-dashed rounded-lg">
        <p>Click "Calculate" to view Panchanga details</p>
      </div>
    );
  }

  const extended = extendedData?.extended_features ?? {};

  const formatRange = (start?: string, end?: string) => {
    if (!start || !end) return '—';
    return `${start} – ${end}`;
  };

  const splitList = (value?: string, delimiter = ',') =>
    value ? value.split(delimiter).map((item: string) => item.trim()).filter(Boolean) : [];

  const normalizeKaraka = (item: any) => {
    if (!item) return null;
    if (typeof item === 'string') return { name: item };
    return item;
  };

  const karakaTithi = normalizeKaraka(extended?.karaka_tithi);
  const karakaYogam = normalizeKaraka(extended?.karaka_yogam);
  const panchakaInfo =
    typeof extended?.panchaka_rahitha === 'object'
      ? extended.panchaka_rahitha
      : extended?.panchaka_rahitha
        ? { label: extended.panchaka_rahitha }
        : null;

  // Handle new structure for thaarabalam and chandrabalam
  const thaarabalamData = extended?.thaarabalam;
  const chandrabalamData = extended?.chandrabalam;

  // Fallback for old string format
  const thaarabalamList = thaarabalamData?.favorable_birth_stars ||
    (typeof thaarabalamData === 'string' ? splitList(thaarabalamData) : []);
  const chandrabalamList = chandrabalamData?.favorable_ascendants ||
    (typeof chandrabalamData === 'string' ? splitList(chandrabalamData) : []);
  const navaThaaraLines: string[] = extended?.nava_thaara
    ? extended.nava_thaara.split('|').map((row: string) => row.trim())
    : [];

  const heroHighlights: HighlightStat[] = [
    {
      label: 'Tithi',
      value: basicData.tithi?.name ? `${basicData.tithi.name} (${basicData.tithi.paksha})` : '-',
      detail: basicData.tithi?.end_time ? `ends ${basicData.tithi.end_time}` : undefined
    },
    {
      label: 'Nakshatra',
      value: basicData.nakshatra?.name ? `${basicData.nakshatra.name} (Pada ${basicData.nakshatra.pada})` : '-',
      detail: basicData.nakshatra?.end_time ? `ends ${basicData.nakshatra.end_time}` : undefined
    },
    {
      label: 'Yoga',
      value: basicData.yoga?.name || '-',
      detail: basicData.yoga?.end_time ? `ends ${basicData.yoga.end_time}` : undefined
    },
    {
      label: 'Karana',
      value: basicData.karana?.name || '-'
    },
    {
      label: 'Vaara',
      value: basicData.vaara || '-'
    },
    {
      label: 'Panchaka',
      value: panchakaInfo?.label || '-',
      detail: panchakaInfo?.description ||
        (panchakaInfo?.window ? formatRange(panchakaInfo.window.start, panchakaInfo.window.end) : undefined),
      tone: panchakaInfo?.tone === 'good' ? 'good' : panchakaInfo?.tone === 'bad' ? 'bad' : 'neutral'
    }
  ];

  const astronomyRows = [
    { label: 'Sunrise', value: basicData.sunrise },
    { label: 'Sunset', value: basicData.sunset },
    { label: 'Moonrise', value: basicData.moonrise },
    { label: 'Moonset', value: basicData.moonset },
    { label: 'Ayanamsa', value: basicData.ayanamsa_value ? basicData.ayanamsa_value.toFixed(6) : '-' },
    { label: 'Julian Day', value: basicData.julian_day ? basicData.julian_day.toFixed(4) : '-' },
    { label: 'Rahu Kala', value: formatRange(basicData.rahu_kala?.start, basicData.rahu_kala?.end), helper: 'Daily inauspicious window' },
    { label: 'Yamaganda', value: formatRange(basicData.yamaganda?.start, basicData.yamaganda?.end) },
    { label: 'Gulika', value: formatRange(basicData.gulika?.start, basicData.gulika?.end) },
    { label: 'Abhijit Muhurta', value: formatRange(basicData.abhijit_muhurta?.start, basicData.abhijit_muhurta?.end), helper: 'Midday auspicious slot' },
    { label: 'Amrita Gadiya', value: extended?.amrita_gadiya ? formatRange(extended.amrita_gadiya.start, extended.amrita_gadiya.end) : '-' }
  ];

  const calendarRows = [
    {
      label: 'Tamil Date',
      value: extended?.tamil_calendar
        ? `${extended.tamil_calendar.date} ${extended.tamil_calendar.month}${extended.tamil_calendar.year ? `, ${extended.tamil_calendar.year}` : ''}`
        : '-'
    },
    { label: 'Tamil Yogam', value: extended?.tamil_yogam?.name || '-' },
    { label: 'Samvatsara', value: extended?.samvatsara || '-' },
    { label: 'Ritu', value: extended?.ritu || '-' },
    { label: 'Lunar Month', value: extended?.lunar_month || '-' },
    { label: 'Day / Night', value: extended?.day_length && extended?.night_length ? `${extended.day_length} / ${extended.night_length}` : '-' }
  ];

  const yogaRows = [
    { label: 'Anandhaadhi', value: extended?.anandhaadhi_yoga?.name || '-', helper: 'Overnight star combination for the day' },
    { label: 'Triguna', value: extended?.triguna || '-' },
    {
      label: 'Karaka Tithi',
      value: karakaTithi?.name || karakaTithi?.index || '-',
      helper: karakaTithi?.end_time ? `Influence up to ${karakaTithi.end_time}` : undefined
    },
    {
      label: 'Karaka Yogam',
      value: karakaYogam?.name || karakaYogam?.index || '-'
    },
    {
      label: 'Panchaka',
      value: panchakaInfo?.label || '-',
      helper: panchakaInfo?.window ? formatRange(panchakaInfo.window.start, panchakaInfo.window.end) : panchakaInfo?.description
    }
  ];

  const specialMuhurthas = [
    { label: 'Brahma', value: formatRange(muhurthaData?.brahma_muhurta?.start, muhurthaData?.brahma_muhurta?.end), helper: 'Pre-dawn meditation window' },
    { label: 'Vijaya', value: formatRange(muhurthaData?.vijaya_muhurta?.start, muhurthaData?.vijaya_muhurta?.end), helper: 'Good for decisive actions' },
    { label: 'Godhuli', value: formatRange(muhurthaData?.godhuli_muhurta?.start, muhurthaData?.godhuli_muhurta?.end), helper: 'Twilight worship slot' },
    { label: 'Nishita', value: formatRange(muhurthaData?.nishita_kala?.start, muhurthaData?.nishita_kala?.end), helper: 'Midnight mantra time' },
    { label: 'Durmuhurta', value: formatRange(muhurthaData?.durmuhurta?.start, muhurthaData?.durmuhurta?.end), helper: 'Avoid new beginnings' }
  ];

  const muhurthaTimeline: Array<{ label: string; range: string; tone: Tone }> = muhurthaData?.all_muhurthas?.map((m: any) => ({
    label: m.name,
    range: formatRange(m.start, m.end),
    tone: m.quality === 'Auspicious' ? 'good' : m.quality === 'Inauspicious' ? 'bad' : 'neutral'
  })) ?? [];

  const fiveElementsRows = [
    { label: 'Tithi', value: basicData.tithi?.name ? `${basicData.tithi.name} (${basicData.tithi.paksha})` : '-' },
    { label: 'Tithi Ends', value: basicData.tithi?.end_time },
    { label: 'Nakshatra', value: basicData.nakshatra?.name ? `${basicData.nakshatra.name} (Pada ${basicData.nakshatra.pada})` : '-' },
    { label: 'Nakshatra Lord', value: basicData.nakshatra?.lord },
    { label: 'Nakshatra Ends', value: basicData.nakshatra?.end_time },
    { label: 'Yoga', value: basicData.yoga?.name, helper: basicData.yoga?.end_time ? `Ends ${basicData.yoga.end_time}` : undefined },
    { label: 'Karana', value: basicData.karana?.name },
    { label: 'Vaara (Weekday)', value: basicData.vaara }
  ];

  const ascRows = [
    { label: 'Rasi', value: planetsData?.ascendant?.rasi_name },
    { label: 'Longitude', value: planetsData?.ascendant ? `${planetsData.ascendant.longitude.toFixed(2)}°` : '-' },
    { label: 'Nakshatra', value: planetsData?.ascendant?.nakshatra_name }
  ];

  const retrogradeList = retrogradeData?.retrograde_info?.retrograde_planets ?? [];

  const eclipseInfo = eclipsesData?.eclipse_info;
  const sankrantiInfo = sankrantiData?.sankranti_info?.next_sankranti;

  return (
    <div className="space-y-6 animate-fadeIn">
      <section className="space-y-3">
        <div className="flex flex-col gap-1">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-semibold">{mode === 'natal' ? 'Natal Panchanga Overview' : 'Daily Panchanga Overview'}</h2>
              <p className="text-sm text-muted-foreground">
                {mode === 'natal'
                  ? 'Snapshot of birth-time five limbs and critical windows.'
                  : 'Panchanga elements in force at today\'s sunrise (traditional Hindu day definition).'}
              </p>
              {/* Show the calculation date/time */}
              <div className="mt-1 flex items-center gap-2 text-xs text-muted-foreground">
                <span className="font-medium">
                  {mode === 'natal' ? '📅 Birth:' : '🌅 Sunrise:'}
                </span>
                <span className="font-mono bg-muted px-2 py-0.5 rounded">
                  {mode === 'natal'
                    ? `${basicData?.date} ${basicData?.time}`
                    : `${basicData?.date} ${basicData?.sunrise || basicData?.time}`
                  }
                </span>
                {basicData?.place && (
                  <>
                    <span>•</span>
                    <span>📍 {basicData.place.name}</span>
                  </>
                )}
              </div>
            </div>
            <div className="flex items-center gap-2">
              <div className="flex items-center rounded-md border border-border overflow-hidden">
                <button
                  type="button"
                  className={`px-3 py-1.5 text-xs ${mode === 'natal' ? 'bg-primary text-primary-foreground' : 'bg-background text-foreground'}`}
                  onClick={() => onModeChange && onModeChange('natal')}
                >
                  Natal
                </button>
                <button
                  type="button"
                  className={`px-3 py-1.5 text-xs border-l border-border ${mode === 'daily' ? 'bg-primary text-primary-foreground' : 'bg-background text-foreground'}`}
                  onClick={() => onModeChange && onModeChange('daily')}
                >
                  Daily
                </button>
              </div>
            </div>
          </div>
        </div>
        <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-3">
          {heroHighlights.map((stat) => (
            <StatChip
              key={stat.label}
              label={stat.label}
              value={stat.value}
              detail={stat.detail}
              tone={(stat as any).tone || 'neutral'}
            />
          ))}
        </div>
      </section>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <SectionCard title="Five Elements (Panchanga)" rows={fiveElementsRows} />
        <SectionCard title="Daily Sky & Timings" description="Astronomical markers and sensitive slots." rows={astronomyRows} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <SectionCard title="Yogas & Properties" rows={yogaRows} />

        <SectionCard title="Strength & Bala">
          <div className="space-y-3">
            <div>
              <div className="flex items-start justify-between mb-1">
                <p className="text-xs uppercase text-muted-foreground">Thaarabalam</p>
                {thaarabalamData?.description && (
                  <span className="text-[10px] text-muted-foreground italic">{thaarabalamData.count} favorable</span>
                )}
              </div>
              {thaarabalamList.length ? (
                <>
                  <div className="flex flex-wrap gap-1 mb-1">
                    {thaarabalamList.map((star: string, idx: number) => (
                      <Badge key={`thaara-${idx}-${star}`} variant="outline" className="text-xs">
                        {star}
                      </Badge>
                    ))}
                  </div>
                  {thaarabalamData?.description && (
                    <p className="text-[10px] text-muted-foreground">{thaarabalamData.description}</p>
                  )}
                </>
              ) : (
                <p className="text-sm font-medium">—</p>
              )}
            </div>
            <div>
              <div className="flex items-start justify-between mb-1">
                <p className="text-xs uppercase text-muted-foreground">Chandrabalam</p>
                {chandrabalamData?.description && (
                  <span className="text-[10px] text-muted-foreground italic">{chandrabalamData.count} favorable</span>
                )}
              </div>
              {chandrabalamList.length ? (
                <>
                  <div className="flex flex-wrap gap-1 mb-1">
                    {chandrabalamList.map((rasi: string, idx: number) => (
                      <Badge key={`chandra-${idx}-${rasi}`} variant="secondary" className="text-xs">
                        {rasi}
                      </Badge>
                    ))}
                  </div>
                  {chandrabalamData?.description && (
                    <p className="text-[10px] text-muted-foreground">{chandrabalamData.description}</p>
                  )}
                </>
              ) : (
                <p className="text-sm font-medium">—</p>
              )}
            </div>
            <DataRow label="Chandrashtama" value={extended?.chandrashtama || '-'} />
            <div className="space-y-1">
              <p className="text-xs uppercase text-muted-foreground">Nava Thaara</p>
              {navaThaaraLines.length ? (
                <ul className="text-xs text-muted-foreground list-disc list-inside space-y-0.5">
                  {navaThaaraLines.map((line) => (
                    <li key={line}>{line}</li>
                  ))}
                </ul>
              ) : (
                <p className="text-sm font-medium">—</p>
              )}
            </div>
          </div>
        </SectionCard>

        <SectionCard title="Ascendant & Retrograde">
          {planetsData?.ascendant && (
            <div className="space-y-1">
              {ascRows.map((row) => (
                <DataRow key={row.label} label={row.label} value={row.value} />
              ))}
            </div>
          )}
          <Separator className="my-2" />
          <div>
            <p className="text-xs uppercase text-muted-foreground mb-1">Retrograde Planets</p>
            <div className="flex flex-wrap gap-1">
              {retrogradeList.length ? (
                retrogradeList.map((planet: string) => (
                  <Badge key={planet} variant="outline" className="text-xs">
                    {planet}
                  </Badge>
                ))
              ) : (
                <span className="text-sm font-medium">None</span>
              )}
            </div>
          </div>
        </SectionCard>
      </div>
    </div>
  );
}

