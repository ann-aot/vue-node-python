import type { Module } from 'vuex';
import type { StatesState } from './types';
import type { RootState } from '../../types';
import { state } from './state';
import { mutations } from './mutations';
import { actions } from './actions';
import { getters } from './getters';

export const states: Module<StatesState, RootState> = {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
};
