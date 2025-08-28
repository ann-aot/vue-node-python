import { createStore } from 'vuex';
import type { RootState } from './types';
import { states } from './modules/states';

const store = createStore<RootState>({
  state: {
    version: '1.0.0',
  },
  modules: {
    states,
  },
});

export default store;
