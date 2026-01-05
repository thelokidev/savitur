'use client';

import React, { useState, useMemo, useEffect } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { dhasaApi, type DhasaPeriod, type DhasaResponse } from '@/lib/api/dhasa';
import { Card } from '@/components/ui/card';
import { ChevronRight, Home, Loader2, ArrowRight } from 'lucide-react';
import ProgressBar from '@/components/ui/progress-bar';
import { runProgressTests } from '@/lib/ui/progress';
import { format, isValid, isWithinInterval } from 'date-fns';
import { cn } from '@/lib/utils';
import { BirthDetails } from '@/lib/api/charts';

// Helper to parse backend dates
const parseDate = (dateStr: string): Date | null => {
  if (!dateStr) return null;
  const d = new Date(dateStr);
  return isValid(d) ? d : null;
};

const formatDateTime = (dateStr: string) => {
  const d = parseDate(dateStr);
  return d ? format(d, 'yyyy-MM-dd HH:mm:ss') : dateStr;
};

const formatDateOnly = (dateStr: string) => {
  const d = parseDate(dateStr);
  return d ? format(d, 'yyyy-MM-dd') : '';
};

const formatTimeHHMM = (dateStr: string) => {
  const d = parseDate(dateStr);
  return d ? format(d, 'HH:mm') : '';
};

interface DhasaTabProps {
  birthData: BirthDetails;
  compact?: boolean;
}

export default function DhasaTab({ birthData, compact = false }: DhasaTabProps) {
  const [dhasaType, setDhasaType] = useState<string>('vimsottari');
  const [path, setPath] = useState<DhasaPeriod[]>([]);
  const [loadingSubtree, setLoadingSubtree] = useState(false);

  const queryClient = useQueryClient();

  const birthDetailsReady = Boolean(
    birthData.date && birthData.time && birthData.place?.name && typeof birthData.place.latitude === 'number'
  );

  // Initial fetch: Level 1 only
  const { data, isLoading } = useQuery({
    queryKey: ['dhasa', birthData.date, birthData.time, birthData.place?.latitude, birthData.place?.longitude, birthData.ayanamsa, dhasaType],
    queryFn: async () => {
      const response = await dhasaApi.calculateDhasa({
        birth_details: birthData,
        dhasa_type: dhasaType,
        include_antardhasa: true,
        ayanamsa: birthData.ayanamsa,
        max_sub_level: 1
      });
      if ((response as any)?.error) {
        throw new Error((response as any).error);
      }
      return response;
    },
    enabled: birthDetailsReady,
    staleTime: 5 * 60 * 1000,
  });

  const currentPeriods = useMemo(() => {
    if (!data?.periods) return [];
    if (path.length === 0) return data.periods;

    // Traverse the path to find the current children
    let current = data.periods;
    for (const p of path) {
      const found = current.find(c => {
        const cp = (c as any).planet_index;
        const pp = (p as any).planet_index;
        if (typeof cp === 'number' && typeof pp === 'number') {
          return cp === pp;
        }
        return c.planet === p.planet;
      });
      if (found && found.sub_periods) {
        current = found.sub_periods;
      } else {
        return [];
      }
    }
    return current;
  }, [data, path]);

  const handleDrillDown = async (period: DhasaPeriod) => {
    const needFetch = !period.sub_periods || period.sub_periods.length === 0;
    if (!needFetch) {
      setPath([...path, period]);
      return;
    }
    const rootIdx = path.length > 0 ? (path[0] as any).planet_index : (period as any).planet_index;
    if (typeof rootIdx !== 'number') {
      setPath([...path, period]);
      return;
    }
    setLoadingSubtree(true);
    try {
      const response = await dhasaApi.calculateDhasa({
        birth_details: birthData,
        dhasa_type: dhasaType,
        include_antardhasa: true,
        ayanamsa: birthData.ayanamsa,
        max_sub_level: 6,
        focus_mahadasha_index: rootIdx
      });
      queryClient.setQueryData(['dhasa', birthData.date, birthData.time, birthData.place?.latitude, birthData.place?.longitude, birthData.ayanamsa, dhasaType], (old: DhasaResponse | undefined) => {
        if (!old) return old;
        const newPeriods = old.periods.map(p => {
          if ((p as any).planet_index === rootIdx) {
            const fetchedPeriod = response.periods.find(fp => (fp as any).planet_index === rootIdx);
            return fetchedPeriod || p;
          }
          return p;
        });
        return { ...old, periods: newPeriods };
      });
      setPath([...path, period]);
    } catch (err) {
      console.error("Failed to fetch subtree", err);
    } finally {
      setLoadingSubtree(false);
    }
  };

  const handleNavigateUp = (index: number) => {
    if (index === -1) {
      setPath([]);
    } else {
      setPath(path.slice(0, index + 1));
    }
  };



  if (process.env.NODE_ENV !== 'production') {
    try {
      const results = runProgressTests();
      // eslint-disable-next-line no-console
      console.log('Progress unit tests:', results);
    } catch { }
  }

  const dhasaGroups = [
    {
      label: 'Graha Dhasas',
      options: [
        { value: 'vimsottari', label: 'Vimsottari' },
        { value: 'ashtottari', label: 'Ashtottari' },
        { value: 'yogini', label: 'Yogini' },
        { value: 'shodasottari', label: 'Shodasottari' },
        { value: 'dwadasottari', label: 'Dwadasottari' },
        { value: 'dwisatpathi', label: 'Dwisatpathi' },
        { value: 'panchottari', label: 'Panchottari' },
        { value: 'sataatbika', label: 'Sataatbika' },
        { value: 'chathuraaseethi_sama', label: 'Chathuraaseethi Sama' },
        { value: 'shastihayani', label: 'Shastihayani' },
        { value: 'shattrimsa_sama', label: 'Shattrimsa Sama' },
        { value: 'naisargika', label: 'Naisargika' },
        { value: 'tara', label: 'Tara' },
        { value: 'karaka', label: 'Karaka' },
        { value: 'aayu', label: 'Aayu' },
      ]
    },
    {
      label: 'Rasi Dhasas',
      options: [
        { value: 'narayana', label: 'Narayana' },
        { value: 'chara', label: 'Chara' },
        { value: 'kendradhi_rasi', label: 'Kendradhi Rasi' },
        { value: 'sudasa', label: 'Sudasa' },
        { value: 'drig', label: 'Drig' },
        { value: 'nirayana', label: 'Nirayana' },
        { value: 'shoola', label: 'Shoola' },
        { value: 'lagnamsaka', label: 'Lagnamsaka' },
        { value: 'padhanadhamsa', label: 'Padhanadhamsa' },
        { value: 'mandooka', label: 'Mandooka' },
        { value: 'sthira', label: 'Sthira' },
        { value: 'tara_lagna', label: 'Tara Lagna' },
        { value: 'brahma', label: 'Brahma' },
        { value: 'varnada', label: 'Varnada' },
        { value: 'yogardha', label: 'Yogardha' },
        { value: 'navamsa', label: 'Navamsa' },
        { value: 'paryaaya', label: 'Paryaaya' },
        { value: 'trikona', label: 'Trikona' },
        { value: 'kalachakra', label: 'Kalachakra' },
        { value: 'moola', label: 'Moola' },
        { value: 'chakra', label: 'Chakra' },
      ]
    }
  ];

  const getLevelName = (depth: number) => {
    switch (depth) {
      case 0: return 'Mahadashas';
      case 1: return 'Antardashas';
      case 2: return 'Pratyantardashas';
      case 3: return 'Sookshma Antardashas';
      case 4: return 'Prana Antardashas';
      case 5: return 'Deha Antardashas';
      default: return 'Sub-periods';
    }
  };

  return (
    <Card className="flex flex-col h-full overflow-hidden border-border/60 bg-card/50 backdrop-blur-sm shadow-none">
      {/* Header Section */}
      <div className="flex flex-col gap-2 p-3 border-b bg-muted/20 flex-shrink-0">
        {/* Top Row: Selector */}
        <div className="flex items-center justify-between gap-2">
          <select
            value={dhasaType}
            onChange={(e) => { setDhasaType(e.target.value); setPath([]); }}
            className="h-7 text-xs rounded-md border border-input bg-background px-2 w-full max-w-[180px] focus:ring-1 focus:ring-primary"
          >
            {dhasaGroups.map(group => (
              <optgroup key={group.label} label={group.label}>
                {group.options.map(opt => (
                  <option key={opt.value} value={opt.value}>{opt.label}</option>
                ))}
              </optgroup>
            ))}
          </select>
        </div>

        {/* Breadcrumbs / Current Level Title */}
        <div className="flex items-center gap-1 text-xs overflow-x-auto scrollbar-none pb-1">
          {path.length === 0 ? (
            <span className="font-semibold text-primary">Maha Dasas</span>
          ) : (
            <div className="flex items-center gap-1 whitespace-nowrap">
              <button
                onClick={() => handleNavigateUp(-1)}
                className="p-1 rounded-md hover:bg-accent text-muted-foreground hover:text-foreground transition-colors"
                title="Back to Root"
              >
                <Home className="w-3.5 h-3.5" />
              </button>
              <ChevronRight className="w-3 h-3 text-muted-foreground/40" />
              {path.map((p, idx) => (
                <React.Fragment key={idx}>
                  <button
                    onClick={() => handleNavigateUp(idx)}
                    className="hover:underline font-medium text-muted-foreground hover:text-primary transition-colors"
                  >
                    {p.planet}
                  </button>
                  <ChevronRight className="w-3 h-3 text-muted-foreground/40" />
                </React.Fragment>
              ))}
              <span className="font-semibold text-primary">{getLevelName(path.length)}</span>
            </div>
          )}
        </div>
      </div>

      {/* Table Content */}
      <div className="flex-1 overflow-y-auto relative">
        {loadingSubtree && (
          <div className="absolute inset-0 bg-background/60 backdrop-blur-[1px] z-50 flex items-center justify-center">
            <div className="flex flex-col items-center gap-2">
              <Loader2 className="w-6 h-6 animate-spin text-primary" />
              <span className="text-[10px] font-medium text-muted-foreground">Loading...</span>
            </div>
          </div>
        )}

        {!birthDetailsReady ? (
          <div className="flex items-center justify-center h-full text-xs text-muted-foreground p-4 text-center">
            Enter birth details to view dhasa
          </div>
        ) : isLoading ? (
          <div className="flex items-center justify-center h-full text-xs text-muted-foreground">
            <Loader2 className="w-5 h-5 animate-spin mr-2" />
            Calculating...
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-xs">
              <thead className="sticky top-0 bg-card">
                <tr className="text-muted-foreground">
                  <th className="text-left font-medium p-2">Planet</th>
                  <th className="text-left font-medium p-2">Start</th>
                  <th className="text-left font-medium p-2">End</th>
                  <th className="text-left font-medium p-2">Duration</th>
                  <th className="text-left font-medium p-2">Left</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border/40">
                {currentPeriods.map((period, idx) => {
                  const now = new Date();
                  const start = parseDate(period.start_date);
                  const end = parseDate(period.end_date);
                  const isActive = start && end ? isWithinInterval(now, { start, end }) : false;
                  const isLeaf = path.length >= 5; // Deha level (Level 6, index 5)
                  const msDay = 24 * 60 * 60 * 1000;
                  const durationDays = start && end ? ((end.getTime() - start.getTime()) / msDay) : undefined;
                  const durationText = typeof durationDays === 'number' ? `${durationDays.toFixed(2)} days` : '';
                  const totalMs = start && end ? Math.max(0, end.getTime() - start.getTime()) : 0;
                  const elapsedMs = start ? Math.max(0, now.getTime() - start.getTime()) : 0;
                  const progress = totalMs > 0 ? Math.min(1, Math.max(0, elapsedMs / totalMs)) : 0;
                  const leftPct = Math.round((1 - progress) * 100);
                  return (
                    <tr
                      key={idx}
                      onClick={() => !isLeaf && handleDrillDown(period)}
                      className={cn("hover:bg-accent/40", !isLeaf && "cursor-pointer", isActive && "bg-primary/5")}
                    >
                      <td className="p-2 font-semibold text-foreground">{period.planet}</td>
                      <td className="p-2">
                        <div className="space-y-0.5">
                          <div className="text-[10px] text-muted-foreground font-medium">Start:</div>
                          <div className="font-mono text-foreground text-xs">{formatDateOnly(period.start_date)}</div>
                          <div className="font-mono text-muted-foreground text-[11px]">{formatTimeHHMM(period.start_date)}</div>
                        </div>
                      </td>
                      <td className="p-2">
                        <div className="space-y-0.5">
                          <div className="text-[10px] text-muted-foreground font-medium">End:</div>
                          <div className="font-mono text-foreground text-xs">{formatDateOnly(period.end_date)}</div>
                          <div className="font-mono text-muted-foreground text-[11px]">{formatTimeHHMM(period.end_date)}</div>
                        </div>
                      </td>
                      <td className="p-2 font-mono text-muted-foreground">{durationText}</td>
                      <td className="p-2">
                        <div className="flex items-center gap-2">
                          <ProgressBar start={period.start_date} end={period.end_date} size="sm" />
                        </div>
                      </td>
                    </tr>
                  );
                })}
                {currentPeriods.length === 0 && (
                  <tr>
                    <td colSpan={5} className="p-4 text-center text-xs text-muted-foreground">No periods found.</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </Card>
  );
}
