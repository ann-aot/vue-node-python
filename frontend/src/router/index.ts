import { createRouter, createWebHashHistory } from 'vue-router';
import type { RouteRecordRaw } from 'vue-router';

import HelloWorld from '../components/HelloWorld.vue';
import WorkflowList from '../components/WorkflowList.vue';

const routes: Array<RouteRecordRaw> = [
  { path: '/', name: 'home', component: HelloWorld },
  { path: '/workflows', name: 'workflows', component: WorkflowList },
];

export const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
