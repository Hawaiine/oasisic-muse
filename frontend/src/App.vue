<template>
  <n-config-provider :theme="darkTheme" :theme-overrides="themeOverrides">
    <n-message-provider>
      <n-notification-provider>
        <div class="app-layout">
          <n-layout has-sider class="app-container">
            <n-layout-sider
              :collapsed-width="60"
              :width="220"
              :collapsed="sidebarCollapsed"
              show-trigger
              collapse-mode="width"
              bordered
              class="sidebar"
            >
              <div class="logo">
                <svg class="logo-svg" viewBox="0 0 32 32" width="28" height="28">
                  <circle cx="16" cy="16" r="14" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.3"/>
                  <path d="M10 18 Q16 8 22 18" fill="none" stroke="#1d9bf0" stroke-width="2.5" stroke-linecap="round"/>
                  <circle cx="16" cy="12" r="3" fill="#1d9bf0"/>
                </svg>
                <span v-if="!sidebarCollapsed" class="logo-text">Muse</span>
              </div>

              <n-menu
                :options="menuOptions"
                :value="currentRoute"
                @update:value="handleMenuSelect"
              />

              <div class="sidebar-footer">
                <n-tag :bordered="false" size="small" round :type="online ? 'success' : 'error'">
                  {{ online ? '在线' : '离线' }}
                </n-tag>
                <n-button quaternary circle size="tiny" @click="sidebarCollapsed = !sidebarCollapsed">
                  ◀
                </n-button>
              </div>
            </n-layout-sider>

            <n-layout-content class="main-content" content-style="padding: 32px; max-width: 960px;">
              <router-view />
            </n-layout-content>
          </n-layout>
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

const menuOptions = [
  { label: '总览', key: '/dashboard' },
  { label: '订阅', key: '/subscribe' },
  { label: '下载', key: '/downloads' },
  { label: '媒体库', key: '/library' },
  { label: '搜索', key: '/search' },
  { label: '设置', key: '/settings' },
  { label: '关于', key: '/about' },
]

function handleMenuSelect(key: string) {
  router.push(key)
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
/* ========== 全局重置 ========== */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', Roboto, 'Noto Sans SC', 'PingFang SC', system-ui, sans-serif;
  background: #0b0e14;
  color: #e2e8f0;
  -webkit-font-smoothing: antialiased;
}

#app {
  min-height: 100vh;
}

/* ========== 布局 ========== */
.app-layout {
  min-height: 100vh;
}

.app-container {
  min-height: 100vh;
}

/* ========== 侧栏 ========== */
.sidebar {
  background: #0d1117 !important;
  border-right: 1px solid #1e2533 !important;
}

.sidebar .n-layout-scroll-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.sidebar .n-menu {
  flex: 1;
  padding: 12px 8px;
}

.sidebar .n-menu .n-menu-item-content {
  border-radius: 10px;
}

.logo {
  padding: 20px 16px;
  display: flex;
  align-items: center;
  gap: 10px;
  border-bottom: 1px solid #1e2533;
  min-height: 68px;
}

.logo-svg {
  flex-shrink: 0;
  color: #1d9bf0;
}

.logo-text {
  font-size: 18px;
  font-weight: 700;
  letter-spacing: -0.3px;
  background: linear-gradient(135deg, #e2e8f0, #94a3b8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.sidebar-footer {
  padding: 12px 8px;
  border-top: 1px solid #1e2533;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

/* ========== 主内容 ========== */
.main-content {
  background: #0b0e14;
  overflow-y: auto;
}

/* ========== 页面标题 ========== */
.page-title {
  font-size: 26px;
  font-weight: 700;
  letter-spacing: -0.5px;
  margin-bottom: 24px;
  color: #e2e8f0;
}

/* ========== 通用组件 ========== */
.card {
  background: #1a202c;
  border: 1px solid #1e2533;
  border-radius: 14px;
  padding: 20px;
  transition: border-color 0.2s;
}

.card:hover {
  border-color: #2a3344;
}

.section {
  margin-bottom: 24px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 12px;
  color: #e2e8f0;
}

.section-desc {
  font-size: 13px;
  color: #8892a6;
  margin-bottom: 16px;
}

/* ========== 表单控件 ========== */
.n-input .n-input-wrapper,
.n-input-number .n-input-number-group,
.n-select .n-base-selection,
.n-switch .n-switch__rail {
  border-radius: 10px !important;
}

/* ========== 滚动条 ========== */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: #1e2533;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #2a3344;
}

/* ========== 导航高亮 ========== */
.n-menu .n-menu-item-content--selected {
  background: rgba(29, 155, 240, 0.1) !important;
  color: #1d9bf0 !important;
}

.n-menu .n-menu-item-content--selected::before {
  content: '';
  position: absolute;
  left: -8px;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 20px;
  background: #1d9bf0;
  border-radius: 0 3px 3px 0;
}
</style>
