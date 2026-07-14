<template>
  <n-config-provider :theme="darkTheme" :theme-overrides="themeOverrides">
    <n-message-provider>
      <n-notification-provider>
        <div class="app-root">
          <!-- 侧栏 -->
          <aside class="sidebar" :class="{ collapsed: sidebarCollapsed }">
            <div class="sidebar-header">
              <svg class="logo" viewBox="0 0 32 32" width="24" height="24">
                <circle cx="16" cy="16" r="14" fill="none" stroke="#1d9bf0" stroke-width="1.5" opacity="0.4"/>
                <path d="M10 18 Q16 8 22 18" fill="none" stroke="#1d9bf0" stroke-width="2" stroke-linecap="round"/>
                <circle cx="16" cy="12" r="3" fill="#1d9bf0"/>
              </svg>
              <span class="brand" v-show="!sidebarCollapsed">Muse</span>
            </div>

            <nav class="sidebar-nav">
              <div
                v-for="item in menuItems"
                :key="item.key"
                class="nav-item"
                :class="{ active: currentRoute === item.key }"
                @click="go(item.key)"
              >
                <span class="nav-icon">{{ item.icon }}</span>
                <span class="nav-label" v-show="!sidebarCollapsed">{{ item.label }}</span>
              </div>
            </nav>

            <div class="sidebar-footer">
              <n-tag size="tiny" round :type="online ? 'success' : 'error'" v-show="!sidebarCollapsed">
                {{ online ? '在线' : '离线' }}
              </n-tag>
              <n-button quaternary circle size="tiny" @click="sidebarCollapsed = !sidebarCollapsed" v-show="sidebarCollapsed">
                ▶
              </n-button>
            </div>
          </aside>

          <!-- 主内容区 -->
          <main class="main-area">
            <div class="main-inner">
              <router-view />
            </div>
          </main>
        </div>
      </n-notification-provider>
    </n-message-provider>
  </n-config-provider>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { darkTheme } from 'naive-ui'
import { themeOverrides } from './theme'
import { healthCheck } from './api'

const router = useRouter()
const route = useRoute()
const sidebarCollapsed = ref(false)
const online = ref(false)

const currentRoute = computed(() => route.path)

const menuItems = [
  { label: '总览', key: '/dashboard', icon: '📊' },
  { label: '订阅', key: '/subscribe', icon: '📋' },
  { label: '下载', key: '/downloads', icon: '⬇️' },
  { label: '媒体库', key: '/library', icon: '🎬' },
  { label: '搜索', key: '/search', icon: '🔍' },
  { label: '设置', key: '/settings', icon: '⚙️' },
  { label: '关于', key: '/about', icon: 'ℹ️' },
]

function go(path: string) {
  router.push(path)
}

async function checkOnline() {
  try {
    await healthCheck()
    online.value = true
  } catch {
    online.value = false
  }
}

onMounted(checkOnline)
</script>

<style>
/* ========== 全局 ========== */
* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', Roboto, 'Noto Sans SC', 'PingFang SC', system-ui, sans-serif;
  background: #0b0e14;
  color: #c9d1d9;
  -webkit-font-smoothing: antialiased;
}

#app { min-height: 100vh; }

/* ========== 整体布局 ========== */
.app-root {
  display: flex;
  min-height: 100vh;
}

/* ========== 侧栏 ========== */
.sidebar {
  width: 224px;
  background: #0d1117;
  border-right: 1px solid #161b22;
  display: flex;
  flex-direction: column;
  position: sticky;
  top: 0;
  height: 100vh;
  flex-shrink: 0;
  transition: width 0.2s ease;
  z-index: 100;
}

.sidebar.collapsed { width: 64px; }

.sidebar-header {
  padding: 20px 16px;
  display: flex;
  align-items: center;
  gap: 10px;
  border-bottom: 1px solid #161b22;
  min-height: 64px;
}

.logo { flex-shrink: 0; }

.brand {
  font-size: 17px;
  font-weight: 700;
  letter-spacing: -0.3px;
  color: #e6edf3;
}

.sidebar-nav {
  flex: 1;
  padding: 8px;
  overflow-y: auto;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.15s ease;
  color: #8b949e;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 2px;
}

.nav-item:hover {
  background: #161b22;
  color: #e6edf3;
}

.nav-item.active {
  background: rgba(29, 155, 240, 0.12);
  color: #58a6ff;
}

.nav-item.active .nav-icon {
  filter: none;
}

.nav-icon { font-size: 16px; width: 20px; text-align: center; flex-shrink: 0; }
.nav-label { white-space: nowrap; overflow: hidden; }

.sidebar-footer {
  padding: 12px 8px;
  border-top: 1px solid #161b22;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

/* ========== 主内容 ========== */
.main-area {
  flex: 1;
  min-width: 0;
  background: #0b0e14;
}

.main-inner {
  max-width: 1024px;
  padding: 32px 40px 64px;
}

/* ========== 滚动条 ========== */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #161b22; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #21262d; }

/* ========== 全局表单美化 ========== */
.n-input .n-input-wrapper,
.n-input-number .n-input-number-group,
.n-select .n-base-selection,
.n-switch .n-switch__rail {
  border-radius: 8px !important;
}

/* ========== 页面标题 ========== */
.page-title {
  font-size: 22px;
  font-weight: 700;
  letter-spacing: -0.3px;
  margin-bottom: 24px;
  color: #e6edf3;
}

/* ========== 卡片 ========== */
.n-card {
  border-radius: 12px !important;
}
</style>
