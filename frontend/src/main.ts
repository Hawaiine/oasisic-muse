import { createApp } from 'vue'
import { createRouter, createWebHashHistory } from 'vue-router'
import App from './App.vue'
import Dashboard from './views/Dashboard.vue'
import Subscribe from './views/Subscribe.vue'
import Downloads from './views/Downloads.vue'
import Library from './views/Library.vue'
import Settings from './views/Settings.vue'
import About from './views/About.vue'
import Search from './views/Search.vue'

const routes = [
  { path: '/', redirect: '/dashboard' },
  { path: '/dashboard', component: Dashboard, meta: { title: '总览', icon: '📊' } },
  { path: '/subscribe', component: Subscribe, meta: { title: '订阅', icon: '📋' } },
  { path: '/downloads', component: Downloads, meta: { title: '下载', icon: '⬇️' } },
  { path: '/library', component: Library, meta: { title: '媒体库', icon: '🎬' } },
  { path: '/settings', component: Settings, meta: { title: '设置', icon: '⚙️' } },
  { path: '/about', component: About, meta: { title: '关于', icon: 'ℹ️' } },
  { path: '/search', component: Search, meta: { title: '搜索', icon: '🔍' } },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

const app = createApp(App)
app.use(router)
app.mount('#app')