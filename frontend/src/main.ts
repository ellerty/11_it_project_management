import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// 导入样式
import './style.css'
import './assets/styles/theme.css'

createApp(App)
  .use(router)
  .mount('#app')
