import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const routes = [
  { path: '/', component: () => import('../views/Dashboard.vue'), meta: { auth: true } },
  { path: '/transactions', component: () => import('../views/Transactions.vue'), meta: { auth: true } },
  { path: '/budgets', component: () => import('../views/Budgets.vue'), meta: { auth: true } },
  { path: '/login', component: () => import('../views/Login.vue') },
  { path: '/register', component: () => import('../views/Register.vue') },
];

const router = createRouter({ history: createWebHistory(), routes });

router.beforeEach((to) => {
  const auth = useAuthStore();
  if (to.meta.auth && !auth.isLoggedIn) return '/login';
});

export default router;
