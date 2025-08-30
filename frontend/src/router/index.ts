import { createRouter, createWebHashHistory } from 'vue-router';
import type { RouteRecordRaw } from 'vue-router';

import HelloWorld from '../components/HelloWorld.vue';
import StateDashboard from '../components/StateDashboard.vue';

const routes: Array<RouteRecordRaw> = [
  { path: '/', name: 'home', component: HelloWorld },
  { path: '/states', name: 'states', component: StateDashboard },
];

export const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
