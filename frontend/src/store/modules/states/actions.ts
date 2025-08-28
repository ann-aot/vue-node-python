import { ActionTree } from "vuex";
import { StatesState } from "./types";
import { RootState } from "../../types";
import { MutationTypes } from "./mutations";
import axios from "axios";
import { API_BASE } from "../../../constants";

export const ActionTypes = {
  FETCH_STATES: "FETCH_STATES",
} as const;

export const actions: ActionTree<StatesState, RootState> = {
  async [ActionTypes.FETCH_STATES]({ commit }) {
    commit(MutationTypes.SET_LOADING, true);
    commit(MutationTypes.SET_ERROR, null);
    try {
      const res = await axios.get(`${API_BASE}/states`);
      commit(MutationTypes.SET_STATES, res.data);
    } catch (err: any) {
      commit(MutationTypes.SET_ERROR, err.message || "Failed to fetch states");
    } finally {
      commit(MutationTypes.SET_LOADING, false);
    }
  },
};
