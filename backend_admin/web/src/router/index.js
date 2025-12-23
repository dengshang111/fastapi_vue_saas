import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = createRouter({
  history: createWebHistory('/admin/'),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
      meta: { requiresGuest: true }
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/DashboardView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/user-manage',
      name: 'user-manage',
      component: () => import('../views/UserManageView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/swiper-manage',
      name: 'swiper-manage',
      component: () => import('../views/SwiperManageView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/phone-manage',
      name: 'phone-manage',
      component: () => import('../views/PhoneManageView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/product-manage',
      name: 'product-manage',
      component: () => import('../views/ProductManageView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/content-manage',
      name: 'content-manage',
      component: () => import('../views/ContentManageView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/about-manage',
      name: 'about-manage',
      component: () => import('../views/AboutManageView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/theme-settings',
      name: 'theme-settings',
      component: () => import('../views/ThemeSettingsView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    }
  ]
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // 需要认证的页面
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
    return
  }
  
  // 已登录用户不能访问登录页
  if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next('/dashboard')
    return
  }
  
  next()
})

export default router
