import { createRouter, createWebHistory } from 'vue-router';
import Login from '../components/Login.vue';
import Dashboard from '../components/Dashboard.vue';
import { authService } from '../services/authService';

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  }
];

const router = createRouter({
  // import.meta.env.BASE_URL is set by Vite from the "base" option in vite.config.js.
  // Locally it's "/", on GitLab Pages it becomes "/repo-name/".
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

// Navigation guard to protect routes that require authentication
router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth) {
    if (authService.isAuthenticated()) {
      next();
    } else {
      next('/login');
    }
  } else if (to.path === '/login' && authService.isAuthenticated()) {
    // If already authenticated, redirect to dashboard
    next('/dashboard');
  } else {
    next();
  }
});

export default router;

