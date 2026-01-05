export const RASI_NAMES = [
  'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
  'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
];

export const getRasiIndexByName = (name: string): number => RASI_NAMES.indexOf(name);

export interface PlanetLike {
  name: string;
  rasi_name: string;
  degrees_in_rasi: number;
  longitude: number;
  retrograde?: boolean;
}

export interface ChartDataLike {
  ascendant: { rasi_name: string; longitude: number; degrees_in_rasi: number };
  planets: PlanetLike[];
}

export const mapPlanetsByRasi = (data: ChartDataLike) => {
  const buckets: Record<number, PlanetLike[]> = {};
  for (let i = 0; i < 12; i++) buckets[i] = [];
  data.planets.forEach(p => {
    const idx = getRasiIndexByName(p.rasi_name);
    if (idx >= 0) buckets[idx].push(p);
  });
  return buckets;
};

export const mapPlanetsToNorthHouses = (data: ChartDataLike) => {
  const ascIndex = getRasiIndexByName(data.ascendant.rasi_name);
  const byRasi = mapPlanetsByRasi(data);
  const houses: Record<number, PlanetLike[]> = {};
  for (let h = 1; h <= 12; h++) {
    const rasiIndex = (ascIndex + h - 1) % 12;
    houses[h] = byRasi[rasiIndex] || [];
  }
  return houses;
};

export const mapPlanetsToSouthHouses = (data: ChartDataLike) => {
  const ascIndex = getRasiIndexByName(data.ascendant.rasi_name);
  const byRasi = mapPlanetsByRasi(data);
  const houses: Record<number, PlanetLike[]> = {};
  for (let r = 0; r < 12; r++) {
    const houseNumber = ((r - ascIndex + 12) % 12) + 1;
    houses[houseNumber] = byRasi[r] || [];
  }
  return houses;
};

export const runChartMappingTests = (data: ChartDataLike) => {
  const north = mapPlanetsToNorthHouses(data);
  const south = mapPlanetsToSouthHouses(data);
  const results: Array<{ planet: string; northHouse: number; southHouse: number; match: boolean }> = [];
  for (let h = 1; h <= 12; h++) {
    const northPlanets = north[h] || [];
    northPlanets.forEach(p => {
      let southHouse = 0;
      for (let sh = 1; sh <= 12; sh++) {
        if ((south[sh] || []).includes(p)) { southHouse = sh; break; }
      }
      results.push({ planet: p.name, northHouse: h, southHouse, match: h === southHouse });
    });
  }
  return results;
};