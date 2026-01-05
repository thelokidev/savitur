import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export interface BirthData {
  date: string;
  time: string;
  place: {
    name: string;
    latitude: number;
    longitude: number;
    timezone: number;
  };
  ayanamsa: string;
}

interface BirthDetailsStore {
  birthData: BirthData;
  chartStyle: 'south' | 'north';
  hasCalculated: boolean;
  setBirthData: (data: BirthData) => void;
  setChartStyle: (style: 'south' | 'north') => void;
  updatePlace: (place: BirthData['place']) => void;
  setHasCalculated: (value: boolean) => void;
}

// Default birth data - empty, user must enter their own data
const defaultBirthData: BirthData = {
  date: '',
  time: '',
  place: {
    name: '',
    latitude: 0,
    longitude: 0,
    timezone: 0,
  },
  ayanamsa: 'LAHIRI',
};

export const useBirthDetailsStore = create<BirthDetailsStore>()(
  persist(
    (set) => ({
      birthData: defaultBirthData,
      chartStyle: 'south',
      hasCalculated: false,

      setBirthData: (data) => set({ birthData: data }),

      setChartStyle: (style) => set({ chartStyle: style }),

      updatePlace: (place) => set((state) => ({
        birthData: {
          ...state.birthData,
          place,
        },
      })),

      setHasCalculated: (value) => set({ hasCalculated: value }),
    }),
    {
      name: 'birth-details-storage', // localStorage key
      // Merge function to handle missing ayanamsa in old persisted data
      merge: (persistedState: any, currentState: BirthDetailsStore) => ({
        ...currentState,
        ...persistedState,
        birthData: {
          ...defaultBirthData,
          ...persistedState?.birthData,
          // Ensure ayanamsa is always defined (add if missing from old data)
          ayanamsa: persistedState?.birthData?.ayanamsa || defaultBirthData.ayanamsa,
        },
      }),
    }
  )
);
