import type { ActionTree, ActionContext } from 'vuex';
import type { StatesState } from './types';
import type { RootState } from '../../types';
import { MutationTypes } from './mutations';
import apiClient from '../../../plugins/axios';
import { API_BASE } from '../../../constants';

export const ActionTypes = {
  FETCH_STATES: 'FETCH_STATES',
} as const;

export const actions: ActionTree<StatesState, RootState> = {
  async [ActionTypes.FETCH_STATES](context: ActionContext<StatesState, RootState>) {
    const { commit } = context;
    commit(MutationTypes.SET_LOADING, true);
    commit(MutationTypes.SET_ERROR, null);
    try {
      console.log('API_BASE:', API_BASE);
      const fullUrl = `${API_BASE}/states`;
      console.log('Full URL being requested:', fullUrl);
      const res = await apiClient.get(fullUrl);
      commit(MutationTypes.SET_STATES, res.data);
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Failed to fetch states';
      commit(MutationTypes.SET_ERROR, message);
    } finally {
      commit(MutationTypes.SET_LOADING, false);
    }
  },
};
