'use client';

import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';

interface PlanetPosition {
  name: string;
  longitude: number;
  rasi: number;
  rasi_name: string;
  degrees_in_rasi: number;
  nakshatra?: number;
  nakshatra_name?: string;
  nakshatra_pada?: number;
  retrograde?: boolean;
}

interface ComprehensivePlanetTableProps {
  planets: PlanetPosition[];
  ascendant?: {
    rasi: number;
    rasi_name: string;
    longitude: number;
    degrees_in_rasi: number;
    nakshatra?: number;
    nakshatra_name?: string;
  };
  specialLagnas?: PlanetPosition[];
  upagrahas?: PlanetPosition[];
  isLoading?: boolean;
}

const RASI_SHORT: { [key: string]: string } = {
  'Aries': 'Ar', 'Taurus': 'Ta', 'Gemini': 'Ge', 'Cancer': 'Cn',
  'Leo': 'Le', 'Virgo': 'Vi', 'Libra': 'Li', 'Scorpio': 'Sc',
  'Sagittarius': 'Sg', 'Capricorn': 'Cp', 'Aquarius': 'Aq', 'Pisces': 'Pi'
};

const NAKSHATRA_SHORT: { [key: string]: string } = {
  'Ashwini': 'Aswi', 'Bharani': 'Bhar', 'Krittika': 'Krit', 'Rohini': 'Rohi',
  'Mrigashira': 'Mrig', 'Ardra': 'Ardr', 'Punarvasu': 'Puna', 'Pushya': 'Push',
  'Ashlesha': 'Asle', 'Magha': 'Magh', 'Purva Phalguni': 'PPha', 'Uttara Phalguni': 'UPha',
  'Hasta': 'Hast', 'Chitra': 'Chit', 'Swati': 'Swat', 'Vishakha': 'Visa',
  'Anuradha': 'Anur', 'Jyeshtha': 'Jyes', 'Mula': 'Mool', 'Purva Ashadha': 'PAs',
  'Uttara Ashadha': 'UAs', 'Shravana': 'Srav', 'Dhanishta': 'Dhan', 'Shatabhisha': 'Shat',
  'Purva Bhadrapada': 'PBha', 'Uttara Bhadrapada': 'UBha', 'Revati': 'Reva'
};

const CHARA_KARAKA_NAMES = ['AK', 'AmK', 'BK', 'MK', 'PK', 'GK', 'DK'];

const formatLongitude = (longitude: number): string => {
  const sign = Math.floor(longitude / 30);
  const signNames = ['Ar', 'Ta', 'Ge', 'Cn', 'Le', 'Vi', 'Li', 'Sc', 'Sg', 'Cp', 'Aq', 'Pi'];
  const deg = Math.floor(longitude % 30);
  const minTotal = ((longitude % 30) - deg) * 60;
  const min = Math.floor(minTotal);
  const sec = ((minTotal - min) * 60);
  
  return `${deg} ${signNames[sign]} ${min}' ${sec.toFixed(2)}"`;
};

const getNavamsa = (longitude: number): string => {
  const navamsaIndex = Math.floor((longitude * 9 / 360) % 12);
  const signNames = ['Ar', 'Ta', 'Ge', 'Cn', 'Le', 'Vi', 'Li', 'Sc', 'Sg', 'Cp', 'Aq', 'Pi'];
  return signNames[navamsaIndex];
};

// Calculate Chara Karakas based on degrees in sign
const calculateCharaKarakas = (planets: PlanetPosition[]) => {
  // Sort planets by degrees in rasi (descending) - excluding Rahu and Ketu
  const sortedPlanets = [...planets]
    .filter(p => p.name !== 'Rahu' && p.name !== 'Ketu')
    .sort((a, b) => b.degrees_in_rasi - a.degrees_in_rasi);
  
  const karakas: { [key: string]: string } = {};
  sortedPlanets.forEach((planet, index) => {
    if (index < CHARA_KARAKA_NAMES.length) {
      karakas[planet.name] = CHARA_KARAKA_NAMES[index];
    }
  });
  
  return karakas;
};

export function ComprehensivePlanetTable({ planets, ascendant, specialLagnas, upagrahas, isLoading }: ComprehensivePlanetTableProps) {
  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-full py-8 text-sm text-muted-foreground">
        Loading planet data...
      </div>
    );
  }

  if (!planets || planets.length === 0) {
    return (
      <div className="flex items-center justify-center h-full py-8 text-sm text-muted-foreground">
        Calculate to view planet positions
      </div>
    );
  }

  const charaKarakas = calculateCharaKarakas(planets);

  return (
    <div className="w-full h-full overflow-auto relative bg-background rounded-md">
      <Table className="w-full border-collapse">
        <TableHeader className="sticky top-0 z-10 bg-background shadow-sm">
          <TableRow className="h-9 border-b border-border hover:bg-transparent">
            <TableHead className="h-9 px-3 text-xs font-bold text-foreground whitespace-nowrap bg-muted/50">Body</TableHead>
            <TableHead className="h-9 px-3 text-xs font-bold text-foreground whitespace-nowrap bg-muted/50">Longitude</TableHead>
            <TableHead className="h-9 px-3 text-xs font-bold text-foreground whitespace-nowrap bg-muted/50">Nakshatra</TableHead>
            <TableHead className="h-9 px-3 text-xs font-bold text-foreground whitespace-nowrap bg-muted/50">Pada</TableHead>
            <TableHead className="h-9 px-3 text-xs font-bold text-foreground whitespace-nowrap bg-muted/50">Rasi</TableHead>
            <TableHead className="h-9 px-3 text-xs font-bold text-foreground whitespace-nowrap bg-muted/50">Navamsa</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {/* Lagna Row */}
          {ascendant && (
            <TableRow className="h-8 border-b border-border/50 hover:bg-muted/20">
              <TableCell className="px-3 py-1.5 text-xs font-semibold text-primary whitespace-nowrap">
                Lagna
              </TableCell>
              <TableCell className="px-3 py-1.5 text-xs font-mono whitespace-nowrap">
                {formatLongitude(ascendant.longitude)}
              </TableCell>
              <TableCell className="px-3 py-1.5 text-xs font-medium text-blue-600 whitespace-nowrap">
                {ascendant.nakshatra_name ? NAKSHATRA_SHORT[ascendant.nakshatra_name] || ascendant.nakshatra_name.substring(0, 4) : '-'}
              </TableCell>
              <TableCell className="px-3 py-1.5 text-xs text-center">
                {ascendant.nakshatra ? (Math.floor((ascendant.longitude * 27 / 360 % 1) * 4) + 1) : '-'}
              </TableCell>
              <TableCell className="px-3 py-1.5 text-xs">
                {RASI_SHORT[ascendant.rasi_name] || ascendant.rasi_name.substring(0, 2)}
              </TableCell>
              <TableCell className="px-3 py-1.5 text-xs">
                {getNavamsa(ascendant.longitude)}
              </TableCell>
            </TableRow>
          )}

          {/* Planet Rows */}
          {planets.map((planet, index) => {
            const karaka = charaKarakas[planet.name];
            const displayName = karaka ? `${planet.name} (${karaka})` : planet.name;
            
            return (
              <TableRow key={index} className="h-8 border-b border-border/50 hover:bg-muted/20">
                <TableCell className="px-3 py-1.5 text-xs font-semibold whitespace-nowrap">
                  {displayName}
                  {planet.retrograde && (
                    <span className="ml-1 text-destructive font-bold" title="Retrograde">®</span>
                  )}
                </TableCell>
                <TableCell className="px-3 py-1.5 text-xs font-mono whitespace-nowrap">
                  {formatLongitude(planet.longitude)}
                </TableCell>
                <TableCell className="px-3 py-1.5 text-xs font-medium text-blue-600 whitespace-nowrap">
                  {planet.nakshatra_name ? NAKSHATRA_SHORT[planet.nakshatra_name] || planet.nakshatra_name.substring(0, 4) : '-'}
                </TableCell>
                <TableCell className="px-3 py-1.5 text-xs text-center">
                  {planet.nakshatra_pada || '-'}
                </TableCell>
                <TableCell className="px-3 py-1.5 text-xs">
                  {RASI_SHORT[planet.rasi_name] || planet.rasi_name.substring(0, 2)}
                </TableCell>
                <TableCell className="px-3 py-1.5 text-xs">
                  {getNavamsa(planet.longitude)}
                </TableCell>
              </TableRow>
            );
          })}

          {/* Special Lagnas Rows */}
          {specialLagnas && specialLagnas.length > 0 && (
            <>
              <TableRow className="bg-muted/40 hover:bg-muted/40">
                <TableCell colSpan={6} className="px-3 py-1.5 text-[10px] font-bold text-muted-foreground uppercase tracking-wider">
                  Special Lagnas
                </TableCell>
              </TableRow>
              {specialLagnas.map((lagna, index) => (
                <TableRow key={`sl-${index}`} className="h-8 border-b border-border/50 hover:bg-muted/20">
                  <TableCell className="px-3 py-1.5 text-xs font-medium text-orange-600 whitespace-nowrap">
                    {lagna.name}
                  </TableCell>
                  <TableCell className="px-3 py-1.5 text-xs font-mono whitespace-nowrap">
                    {formatLongitude(lagna.longitude)}
                  </TableCell>
                  <TableCell className="px-3 py-1.5 text-xs font-medium text-blue-600 whitespace-nowrap">
                    {lagna.nakshatra_name ? NAKSHATRA_SHORT[lagna.nakshatra_name] || lagna.nakshatra_name.substring(0, 4) : '-'}
                  </TableCell>
                  <TableCell className="px-3 py-1.5 text-xs text-center">
                    {lagna.nakshatra_pada || '-'}
                  </TableCell>
                  <TableCell className="px-3 py-1.5 text-xs">
                    {RASI_SHORT[lagna.rasi_name] || lagna.rasi_name.substring(0, 2)}
                  </TableCell>
                  <TableCell className="px-3 py-1.5 text-xs">
                    {getNavamsa(lagna.longitude)}
                  </TableCell>
                </TableRow>
              ))}
            </>
          )}

          {/* Upagrahas Rows */}
          {upagrahas && upagrahas.length > 0 && (
            <>
              <TableRow className="bg-muted/40 hover:bg-muted/40">
                <TableCell colSpan={6} className="px-3 py-1.5 text-[10px] font-bold text-muted-foreground uppercase tracking-wider">
                  Upagrahas
                </TableCell>
              </TableRow>
              {upagrahas.map((upagraha, index) => (
                <TableRow key={`up-${index}`} className="h-8 border-b border-border/50 hover:bg-muted/20">
                  <TableCell className="px-3 py-1.5 text-xs font-medium text-purple-600 whitespace-nowrap">
                    {upagraha.name}
                  </TableCell>
                  <TableCell className="px-3 py-1.5 text-xs font-mono whitespace-nowrap">
                    {formatLongitude(upagraha.longitude)}
                  </TableCell>
                  <TableCell className="px-3 py-1.5 text-xs font-medium text-blue-600 whitespace-nowrap">
                    {upagraha.nakshatra_name ? NAKSHATRA_SHORT[upagraha.nakshatra_name] || upagraha.nakshatra_name.substring(0, 4) : '-'}
                  </TableCell>
                  <TableCell className="px-3 py-1.5 text-xs text-center">
                    {upagraha.nakshatra_pada || '-'}
                  </TableCell>
                  <TableCell className="px-3 py-1.5 text-xs">
                    {RASI_SHORT[upagraha.rasi_name] || upagraha.rasi_name.substring(0, 2)}
                  </TableCell>
                  <TableCell className="px-3 py-1.5 text-xs">
                    {getNavamsa(upagraha.longitude)}
                  </TableCell>
                </TableRow>
              ))}
            </>
          )}
        </TableBody>
      </Table>
    </div>
  );
}
