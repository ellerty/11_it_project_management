import ResumeView from '../modules/user_management/views/ResumeView.vue';

export default {
  path: '/resume',
  name: 'Resume',
  component: ResumeView,
  meta: {
    requiresAuth: true,
    title: '我的简历'
  }
};