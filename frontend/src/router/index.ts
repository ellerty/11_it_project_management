import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw, RouteLocationNormalized, NavigationGuardNext } from 'vue-router'
import { authStore } from '../store/authStore'

// 路由守卫 - 检查用户是否已登录
const requireAuth = (
  to: RouteLocationNormalized, 
  from: RouteLocationNormalized, 
  next: NavigationGuardNext
) => {
  if (authStore.isAuthenticated.value) {
    next()
  } else {
    next('/login')
  }
}

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../modules/job_recommendation/views/JobListView.vue'),
    meta: { title: '首页 - 智慧零工' }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../modules/user_management/views/LoginView.vue'),
    meta: { title: '登录 - 智慧零工' }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../modules/user_management/views/RegisterView.vue'),
    meta: { title: '注册 - 智慧零工' }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../modules/user_management/views/ProfileView.vue'),
    beforeEnter: requireAuth,
    meta: { title: '个人中心 - 智慧零工' }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../components/NotFound.vue'),
    meta: { title: '页面未找到 - 智慧零工' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 修改页面标题
router.beforeEach((to, from, next) => {
  if (to.meta.title) {
    document.title = to.meta.title as string
  }
  next()
})

export default router 