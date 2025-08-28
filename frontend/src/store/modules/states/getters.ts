import type { GetterTree } from 'vuex';
import type { StatesState, StateItem } from './types';
import type { RootState } from '../../types';

export const getters: GetterTree<StatesState, RootState> = {
  allStates: (state): StateItem[] => state.states,
  activeStates: (state): StateItem[] => state.states.filter((s) => s.is_active),
  isLoading: (state): boolean => state.loading,
  errorMessage: (state): string | null => state.error,
};
