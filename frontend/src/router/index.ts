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
    path: '/task-filtering',
    name: 'TaskFiltering',
    // @ts-ignore
    component: () => import('../modules/job_recommendation/views/TaskFilteringView.vue'),
    meta: { title: '我要接单 - 智慧零工' }
  },
  {
    path: '/post-job',
    name: 'PostJob',
    // @ts-ignore
    component: () => import('../modules/job_recommendation/views/PostJobView.vue'),
    meta: { title: '发布任务 - 智慧零工', requiresAuth: true }
  },
  {
    path: '/my-jobs',
    name: 'MyJobs',
    // @ts-ignore
    component: () => import('../modules/job_recommendation/views/MyJobsView.vue'),
    meta: { title: '我的任务 - 智慧零工', requiresAuth: true }
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
    path: '/evaluation',
    name: 'Evaluation',
    // @ts-ignore
    component: () => import('../modules/user_management/views/EvaluationView.vue'),
    meta: { title: '个人评价 - 智慧零工', requiresAuth: true }
  },
  {
    path: '/notifications',
    name: 'Notifications',
    // @ts-ignore
    component: () => import('../modules/user_management/views/NotificationView.vue'),
    meta: { title: '消息通知 - 智慧零工', requiresAuth: true }
  },
  {
    path: '/admin',
    name: 'AdminDashboard',
    // @ts-ignore
    component: () => import('../modules/admin/views/AdminDashboard.vue'),
    meta: { 
      title: '管理员后台 - 智慧零工', 
      requiresAuth: true,
      requiresAdmin: true
    }
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
  } 
  // 检查是否需要管理员权限
  else if (to.meta.requiresAdmin && authStore.state.user?.role !== 'admin') {
    console.log('路由需要管理员权限:', to.path)
    next({ path: '/' })
  }
  else {
    next()
  }
})

export default router