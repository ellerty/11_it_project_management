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
    // @ts-ignore
    component: () => import('../modules/job_recommendation/views/JobListView.vue'),
    meta: { title: '首页 - 智慧零工' }
  },
  {
    path: '/login',
    name: 'Login',
    // @ts-ignore
    component: () => import('../modules/user_management/views/LoginView.vue'),
    meta: { title: '登录 - 智慧零工' }
  },
  {
    path: '/login-register',
    name: 'LoginRegister',
    // @ts-ignore
    component: () => import('../modules/user_management/views/LoginRegisterView.vue'),
    meta: { title: '登录/注册 - 智慧零工' }
  },
  {
    path: '/register',
    name: 'Register',
    // @ts-ignore
    component: () => import('../modules/user_management/views/RegisterView.vue'),
    meta: { title: '注册 - 智慧零工' }
  },
  {
    path: '/profile',
    name: 'Profile',
    // @ts-ignore
    component: () => import('../modules/user_management/views/ProfileView.vue'),
    meta: { title: '个人中心 - 智慧零工', requiresAuth: true }
  },
  {
    path: '/resume',
    name: 'Resume',
    // @ts-ignore
    component: () => import('../modules/user_management/views/ResumeView.vue'),
    meta: { title: '我的简历 - 智慧零工', requiresAuth: true }
  },
  {
    path: '/notifications',
    name: 'Notifications',
    // @ts-ignore
    component: () => import('../modules/user_management/views/NotificationView.vue'),
    meta: { title: '消息通知 - 智慧零工', requiresAuth: true }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    // @ts-ignore
    component: () => import('../components/NotFound.vue'),
    meta: { title: '页面未找到 - 智慧零工' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 修改页面标题和认证检查
router.beforeEach((to, from, next) => {
  // 设置页面标题
  if (to.meta.title) {
    document.title = to.meta.title as string
  }
  
  // 检查是否需要认证
  if (to.meta.requiresAuth && !authStore.isAuthenticated.value) {
    console.log('路由需要认证，重定向到登录页面:', to.path)
    next({ path: '/login', query: { redirect: to.fullPath } })
  } else {
    next()
  }
})

export default router