/// <reference types="vite/client" />
declare module "vuex" {
  export * from "@vue/runtime-core";
  export interface MutationTree<S> {
    [key: string]: (state: S, payload?: any) => void;
  }
}