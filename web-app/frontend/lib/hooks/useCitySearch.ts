import { useState, useCallback, useRef, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { citiesApi, type City, type AutocompleteResponse } from '@/lib/api/cities';

export function useCitySearch() {
  const [searchQuery, setSearchQuery] = useState('');
  const [debouncedQuery, setDebouncedQuery] = useState('');
  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const [isOpen, setIsOpen] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(-1);

  // Grouped autocomplete query
  const { data: autocompleteData, isLoading, error } = useQuery({
    queryKey: ['citiesAutocomplete', debouncedQuery],
    queryFn: () => citiesApi.autocomplete(debouncedQuery, 8),
    enabled: debouncedQuery.length >= 2,
    staleTime: 5 * 60 * 1000, // 5 minutes cache
  });

  // Get flat list of all suggestions for keyboard navigation
  const allSuggestions: City[] = autocompleteData
    ? [...autocompleteData.usa, ...autocompleteData.international]
    : [];

  const handleSearch = useCallback((query: string) => {
    setSearchQuery(query);
    setSelectedIndex(-1);

    // Clear previous timer
    if (timerRef.current) {
      clearTimeout(timerRef.current);
    }

    // Reduced debounce for snappier feel (150ms instead of 300ms)
    timerRef.current = setTimeout(() => {
      if (query.length >= 2) {
        setDebouncedQuery(query);
        setIsOpen(true);
      } else {
        setDebouncedQuery('');
        setIsOpen(false);
      }
    }, 150);
  }, []);

  const selectCity = useCallback(async (cityName: string): Promise<City | null> => {
    try {
      const city = await citiesApi.lookup(cityName);
      setIsOpen(false);
      setSearchQuery(cityName);
      return city;
    } catch (error) {
      console.error('Error looking up city:', error);
      return null;
    }
  }, []);

  // Keyboard navigation
  const handleKeyDown = useCallback((e: React.KeyboardEvent) => {
    if (!isOpen || allSuggestions.length === 0) return;

    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setSelectedIndex(prev =>
          prev < allSuggestions.length - 1 ? prev + 1 : 0
        );
        break;
      case 'ArrowUp':
        e.preventDefault();
        setSelectedIndex(prev =>
          prev > 0 ? prev - 1 : allSuggestions.length - 1
        );
        break;
      case 'Enter':
        e.preventDefault();
        if (selectedIndex >= 0 && selectedIndex < allSuggestions.length) {
          selectCity(allSuggestions[selectedIndex].name);
        }
        break;
      case 'Escape':
        setIsOpen(false);
        setSelectedIndex(-1);
        break;
    }
  }, [isOpen, allSuggestions, selectedIndex, selectCity]);

  // Cleanup timer on unmount
  useEffect(() => {
    return () => {
      if (timerRef.current) {
        clearTimeout(timerRef.current);
      }
    };
  }, []);

  return {
    searchQuery,
    autocompleteData,
    usaCities: autocompleteData?.usa || [],
    internationalCities: autocompleteData?.international || [],
    allSuggestions,
    isLoading,
    error,
    isOpen,
    selectedIndex,
    setIsOpen,
    handleSearch,
    selectCity,
    handleKeyDown
  };
}
