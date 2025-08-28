import { Module } from "vuex";
import { StatesState } from "./types";
import { RootState } from "../../types";
import { state } from "./state";
import { mutations } from "./mutations";
import { actions } from "./actions";
import { getters } from "./getters";

export const states: Module<StatesState, RootState> = {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
};
