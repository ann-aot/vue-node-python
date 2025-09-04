import { createRouter, createWebHashHistory } from 'vue-router';
import type { RouteRecordRaw } from 'vue-router';
import { authState, restoreAuthFromStorage } from '../store/auth';

const Login = () => import('../views/Login.vue');
const Dashboard = () => import('../views/Dashboard.vue');

const routes: Array<RouteRecordRaw> = [
  { path: '/', redirect: { name: 'dashboard' } },
  { path: '/login', name: 'login', component: Login, meta: { public: true } },
  { path: '/dashboard', name: 'dashboard', component: Dashboard, meta: { requiresAuth: true } },
];

export const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

let isRestored = false;
router.beforeEach((to) => {
  if (!isRestored) {
    restoreAuthFromStorage();
    isRestored = true;
  }

  if (to.meta.public) return true;
  if (to.meta.requiresAuth && !authState.isAuthenticated) {
    return { name: 'login', query: { redirect: to.fullPath } };
  }
  if (to.name === 'login' && authState.isAuthenticated) {
    return { name: 'dashboard' };
  }
  return true;
});

export default router;
