'use client';

import { useState, useEffect, useRef } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Button } from '@/components/ui/button';
import { useCitySearch } from '@/lib/hooks/useCitySearch';
import type { BirthData } from '@/lib/store/birth-details-store';
import type { City } from '@/lib/api/cities';

// Re-export for backwards compatibility
export type { BirthData };

interface BirthDetailsFormProps {
  birthData: BirthData;
  onBirthDataChange: (data: BirthData) => void;
  onCalculate: () => void;
  isLoading?: boolean;
  error?: string | null;
  chartStyle?: 'south' | 'north';
  onChartStyleChange?: (style: 'south' | 'north') => void;
}

export const BirthDetailsForm = ({
  birthData,
  onBirthDataChange,
  onCalculate,
  isLoading = false,
  error = null,
  chartStyle = 'south',
  onChartStyleChange
}: BirthDetailsFormProps) => {
  const {
    handleSearch,
    usaCities,
    internationalCities,
    selectCity,
    isLoading: searchLoading,
    isOpen,
    setIsOpen,
    selectedIndex,
    handleKeyDown,
    allSuggestions
  } = useCitySearch();

  const [placeInput, setPlaceInput] = useState(birthData.place.name);
  const inputRef = useRef<HTMLInputElement>(null);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setPlaceInput(birthData.place.name);
  }, [birthData.place.name]);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node) &&
        inputRef.current && !inputRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [setIsOpen]);

  const handlePlaceChange = (value: string) => {
    setPlaceInput(value);
    onBirthDataChange({ ...birthData, place: { ...birthData.place, name: value } });
    handleSearch(value);
  };

  const handleCitySelect = async (city: City) => {
    const result = await selectCity(city.name);
    if (result) {
      onBirthDataChange({
        ...birthData,
        place: {
          name: result.name,
          latitude: result.latitude,
          longitude: result.longitude,
          timezone: result.timezone
        }
      });
      setPlaceInput(result.name);
    }
    setIsOpen(false);
  };

  // Highlight matching text in city name
  const highlightMatch = (text: string, query: string) => {
    if (!query) return text;
    const idx = text.toLowerCase().indexOf(query.toLowerCase());
    if (idx === -1) return text;
    return (
      <>
        {text.slice(0, idx)}
        <span className="font-semibold text-primary">{text.slice(idx, idx + query.length)}</span>
        {text.slice(idx + query.length)}
      </>
    );
  };

  const renderCityItem = (city: City, globalIndex: number) => (
    <div
      key={`${city.name}-${globalIndex}`}
      onClick={() => handleCitySelect(city)}
      className={`px-3 py-2 text-xs cursor-pointer border-b border-border/50 last:border-b-0 flex items-center gap-2
        ${selectedIndex === globalIndex ? 'bg-accent' : 'hover:bg-accent/50'}`}
    >
      <span className="flex-1">{highlightMatch(city.name, placeInput)}</span>
      {city.timezone_name && (
        <span className="text-muted-foreground text-[10px]">{city.timezone_name.split('/').pop()}</span>
      )}
    </div>
  );

  const hasResults = usaCities.length > 0 || internationalCities.length > 0;

  return (
    <Card className="border-none shadow-none">
      <CardHeader className="pb-3">
        <CardTitle className="text-sm">Input Details</CardTitle>
        <CardDescription className="text-xs">Enter date, time, and location</CardDescription>
      </CardHeader>
      <CardContent className="space-y-3">
        <div className="space-y-1.5">
          <Label htmlFor="date" className="text-xs">Date</Label>
          <Input
            id="date"
            type="date"
            value={birthData.date}
            onChange={(e) => onBirthDataChange({ ...birthData, date: e.target.value })}
            className="h-8 text-xs"
          />
        </div>

        <div className="space-y-1.5">
          <Label htmlFor="time" className="text-xs">Time (24-hour format)</Label>
          <Input
            id="time"
            type="time"
            step="1"
            value={birthData.time.slice(0, 5)}
            onChange={(e) => {
              const timeValue = e.target.value;
              if (timeValue) {
                const [hours, minutes] = timeValue.split(':');
                const formattedTime = `${hours.padStart(2, '0')}:${minutes.padStart(2, '0')}:00`;
                onBirthDataChange({ ...birthData, time: formattedTime });
              }
            }}
            className="h-8 text-xs"
          />
          <p className="text-xs text-muted-foreground">Current: {birthData.time}</p>
        </div>

        <div className="space-y-1.5 relative">
          <Label htmlFor="place" className="text-xs">
            Place (Search 190k+ cities)
            {searchLoading && <span className="ml-2 text-muted-foreground">⏳</span>}
          </Label>
          <Input
            ref={inputRef}
            id="place"
            value={placeInput}
            onChange={(e) => handlePlaceChange(e.target.value)}
            onKeyDown={handleKeyDown}
            onFocus={() => placeInput.length >= 2 && hasResults && setIsOpen(true)}
            className="h-8 text-xs"
            placeholder="Start typing city name..."
            autoComplete="off"
          />

          {/* Grouped Dropdown */}
          {isOpen && hasResults && (
            <div
              ref={dropdownRef}
              className="absolute z-50 w-full mt-1 bg-background border border-border rounded-md shadow-lg max-h-72 overflow-y-auto"
            >
              {/* USA Section */}
              {usaCities.length > 0 && (
                <>
                  <div className="px-3 py-1.5 bg-blue-500/10 border-b border-border flex items-center gap-2 sticky top-0">
                    <span className="text-sm">🇺🇸</span>
                    <span className="text-xs font-medium text-blue-600 dark:text-blue-400">USA</span>
                    <span className="text-[10px] text-muted-foreground ml-auto">{usaCities.length} results</span>
                  </div>
                  {usaCities.map((city, idx) => renderCityItem(city, idx))}
                </>
              )}

              {/* International Section */}
              {internationalCities.length > 0 && (
                <>
                  <div className="px-3 py-1.5 bg-emerald-500/10 border-b border-border flex items-center gap-2 sticky top-0">
                    <span className="text-sm">🌍</span>
                    <span className="text-xs font-medium text-emerald-600 dark:text-emerald-400">International</span>
                    <span className="text-[10px] text-muted-foreground ml-auto">{internationalCities.length} results</span>
                  </div>
                  {internationalCities.map((city, idx) => renderCityItem(city, usaCities.length + idx))}
                </>
              )}
            </div>
          )}

          {/* No results message */}
          {isOpen && !hasResults && placeInput.length >= 2 && !searchLoading && (
            <div className="absolute z-50 w-full mt-1 bg-background border border-border rounded-md shadow-lg p-3">
              <p className="text-xs text-muted-foreground text-center">No cities found for "{placeInput}"</p>
            </div>
          )}
        </div>

        <div className="grid grid-cols-2 gap-2">
          <div className="space-y-1.5">
            <Label htmlFor="lat" className="text-xs">Latitude</Label>
            <Input
              id="lat"
              type="number"
              step="0.0001"
              value={birthData.place.latitude}
              onChange={(e) => onBirthDataChange({ ...birthData, place: { ...birthData.place, latitude: parseFloat(e.target.value) || 0 } })}
              className="h-8 text-xs"
            />
          </div>
          <div className="space-y-1.5">
            <Label htmlFor="lon" className="text-xs">Longitude</Label>
            <Input
              id="lon"
              type="number"
              step="0.0001"
              value={birthData.place.longitude}
              onChange={(e) => onBirthDataChange({ ...birthData, place: { ...birthData.place, longitude: parseFloat(e.target.value) || 0 } })}
              className="h-8 text-xs"
            />
          </div>
        </div>

        <div className="space-y-1.5">
          <Label htmlFor="timezone" className="text-xs">Timezone (UTC offset)</Label>
          <Input
            id="timezone"
            type="number"
            step="0.5"
            value={birthData.place.timezone}
            onChange={(e) => onBirthDataChange({ ...birthData, place: { ...birthData.place, timezone: parseFloat(e.target.value) || 0 } })}
            className="h-8 text-xs"
            placeholder="e.g., 5.5 for IST"
          />
        </div>

        <div className="space-y-1.5">
          <Label htmlFor="ayanamsa" className="text-xs">Ayanamsa</Label>
          <select
            id="ayanamsa"
            value={birthData.ayanamsa}
            onChange={(e) => onBirthDataChange({ ...birthData, ayanamsa: e.target.value })}
            className="w-full h-8 px-3 text-xs border border-input rounded-md bg-background"
          >
            <option value="LAHIRI">Lahiri</option>
            <option value="RAMAN">Raman</option>
            <option value="KP">KP</option>
            <option value="TRUE_CITRA">True Chitra</option>
            <option value="TRUE_REVATI">True Revati</option>
            <option value="YUKTESHWAR">Yukteshwar</option>
            <option value="SURYASIDDHANTA">Surya Siddhanta</option>
          </select>
        </div>

        {onChartStyleChange && (
          <div className="space-y-1.5">
            <Label htmlFor="chartStyle" className="text-xs">Chart Style</Label>
            <select
              id="chartStyle"
              value={chartStyle}
              onChange={(e) => onChartStyleChange(e.target.value as 'south' | 'north')}
              className="w-full h-8 px-3 text-xs border border-input rounded-md bg-background"
            >
              <option value="south">South Indian</option>
              <option value="north">North Indian</option>
            </select>
          </div>
        )}

        <Button onClick={onCalculate} className="w-full h-8 text-xs" disabled={isLoading}>
          {isLoading ? 'Calculating...' : 'Calculate'}
        </Button>

        {error && (
          <div className="mt-3 p-2 bg-destructive/10 border border-destructive/20 rounded-md">
            <p className="text-xs text-destructive font-medium">Error:</p>
            <p className="text-xs text-destructive/80 mt-1">{error}</p>
          </div>
        )}
      </CardContent>
    </Card>
  );
};
