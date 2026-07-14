<template>
  <n-config-provider :theme="darkTheme" :theme-overrides="themeOverrides">
    <n-message-provider>
      <n-notification-provider>
        <div class="app-root">
          <!-- Sidebar -->
          <aside class="sidebar" :class="{ collapsed: isCollapsed }">
            <div class="sidebar-brand">
              <span class="brand-icon">🌊</span>
              <span class="brand-text" v-show="!isCollapsed">Oasisic Muse</span>
            </div>

            <nav class="sidebar-nav">
              <div
                v-for="item in navItems"
                :key="item.path"
                class="nav-item"
                :class="{ active: currentRoute === item.path }"
                @click="navigateTo(item.path)"
              >
                <span class="nav-icon">{{ item.icon }}</span>
                <span class="nav-label" v-show="!isCollapsed">{{ item.label }}</span>
              </div>
            </nav>

            <div class="sidebar-footer">
              <div class="collapse-btn" @click="isCollapsed = !isCollapsed">
                {{ isCollapsed ? '→' : '←' }}
              </div>
            </div>
          </aside>

          <!-- Main content -->
          <div class="main-content">
            <header class="top-bar">
              <div class="top-bar-left">
                <button class="menu-toggle" @click="isCollapsed = !isCollapsed">☰</button>
                <h1 class="page-title">{{ currentPageTitle }}</h1>
              </div>
              <div class="top-bar-right">
                <n-tag type="success" round size="small" v-if="connectionStatus === 'connected'" class="status-badge">
                  ● 已连接
                </n-tag>
                <n-tag type="warning" round size="small" v-else-if="connectionStatus === 'connecting'" class="status-badge">
                  ◌ 连接中
                </n-tag>
                <n-tag type="error" round size="small" v-else class="status-badge">
                  ○ 离线
                </n-tag>
              </div>
            </header>
            <main class="content-area">
              <router-view />
            </main>
          </div>
        </div>
      </n-notification-provider>
    </n-message-provider>
  </n-config-provider>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { darkTheme } from 'naive-ui'
import { useMessage } from 'naive-ui'

const router = useRouter()
const route = useRoute()
const message = useMessage()

const isCollapsed = ref(false)
const currentRoute = computed(() => route.path)

const navItems = [
  { path: '/', icon: '📊', label: '总览' },
  { path: '/subscribe', icon: '🔍', label: '订阅' },
  { path: '/downloads', icon: '📥', label: '下载' },
  { path: '/library', icon: '📚', label: '媒体库' },
  { path: '/search', icon: '🔎', label: '搜索' },
  { path: '/settings', icon: '⚙️', label: '设置' },
  { path: '/about', icon: 'ℹ️', label: '关于' },
]

const currentPageTitle = computed(() => {
  const item = navItems.find(n => n.path === route.path)
  return item?.label || 'Oasisic Muse'
})

const connectionStatus = ref<'connected' | 'connecting' | 'offline'>('offline')

function navigateTo(path: string) {
  router.push(path)
}
</script>

<style>
/* Import design system */
@import './assets/design-system.css';

/* ── Root layout ─────────────────────────── */
.app-root {
  display: flex;
  min-height: 100vh;
}

/* ── Sidebar ─────────────────────────────── */
.sidebar {
  width: 224px;
  min-height: 100vh;
  background: var(--bg-surface);
  border-right: 1px solid var(--border-default);
  display: flex;
  flex-direction: column;
  transition: width 0.2s ease-out;
  flex-shrink: 0;
  position: sticky;
  top: 0;
  height: 100vh;
}
.sidebar.collapsed {
  width: 64px;
}

.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 16px 20px;
  border-bottom: 1px solid var(--border-subtle);
  height: 56px;
}
.brand-icon {
  font-size: 20px;
  flex-shrink: 0;
}
.brand-text {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.3px;
  white-space: nowrap;
  overflow: hidden;
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
  border-radius: var(--radius-sm);
  cursor: pointer;
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 400;
  transition: all 0.15s ease-out;
  white-space: nowrap;
  margin-bottom: 2px;
}
.nav-item:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}
.nav-item.active {
  background: var(--accent-muted);
  color: var(--accent);
  font-weight: 500;
}
.nav-item.active .nav-icon {
  opacity: 1;
}
.nav-icon {
  font-size: 16px;
  flex-shrink: 0;
  width: 20px;
  text-align: center;
}
.nav-label {
  overflow: hidden;
  text-overflow: ellipsis;
}

.sidebar-footer {
  border-top: 1px solid var(--border-subtle);
  padding: 8px;
}
.collapse-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 32px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  color: var(--text-muted);
  font-size: 14px;
  transition: all 0.15s ease-out;
}
.collapse-btn:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

/* ── Main content ────────────────────────── */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  height: 56px;
  border-bottom: 1px solid var(--border-subtle);
  background: var(--bg-page);
  position: sticky;
  top: 0;
  z-index: 10;
}
.top-bar-left {
  display: flex;
  align-items: center;
  gap: 12px;
}
.menu-toggle {
  background: none;
  border: none;
  color: var(--text-muted);
  font-size: 18px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: var(--radius-sm);
  transition: all 0.15s ease-out;
}
.menu-toggle:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}
.page-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.2px;
}
.top-bar-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-badge {
  font-size: 12px;
  font-weight: 500;
}

.content-area {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
}

/* ── Page header ─────────────────────────── */
.page-header {
  margin-bottom: 24px;
}
.page-header h2 {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
}
.page-header p {
  font-size: 14px;
  color: var(--text-muted);
}

/* ── Grid ────────────────────────────────── */
.grid {
  display: grid;
  gap: 16px;
}
.grid-cols-2 { grid-template-columns: repeat(2, 1fr); }
.grid-cols-3 { grid-template-columns: repeat(3, 1fr); }
.grid-cols-4 { grid-template-columns: repeat(4, 1fr); }

/* ── Fade animation ──────────────────────── */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s ease-out;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* ── Responsive ──────────────────────────── */
@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    z-index: 100;
    transform: translateX(-100%);
  }
  .sidebar.mobile-open {
    transform: translateX(0);
  }
  .grid-cols-2,
  .grid-cols-3,
  .grid-cols-4 {
    grid-template-columns: 1fr;
  }
  .content-area {
    padding: 16px;
  }
}
</style>
