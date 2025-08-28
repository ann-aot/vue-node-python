import type {MutationTree} from "vuex";
import type { StatesState, StateItem } from "./types";

export const MutationTypes = {
  SET_LOADING: "SET_LOADING",
  SET_STATES: "SET_STATES",
  SET_ERROR: "SET_ERROR",
} as const;

export const mutations: MutationTree<StatesState> = {
  [MutationTypes.SET_LOADING](state, payload: boolean) {
    state.loading = payload;
  },
  [MutationTypes.SET_STATES](state, payload: StateItem[]) {
    state.states = payload;
  },
  [MutationTypes.SET_ERROR](state, payload: string | null) {
    state.error = payload;
  },
};
