<template>
  <div class="app-layout">
    <aside class="sidebar" :class="{ collapsed: sidebarCollapsed }">
      <div class="logo">
        <svg class="logo-svg" viewBox="0 0 32 32" width="28" height="28">
          <circle cx="16" cy="16" r="14" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.3"/>
          <path d="M10 18 Q16 8 22 18" fill="none" stroke="#1d9bf0" stroke-width="2.5" stroke-linecap="round"/>
          <circle cx="16" cy="12" r="3" fill="#1d9bf0"/>
        </svg>
        <span v-show="!sidebarCollapsed" class="logo-text">Muse</span>
      </div>

      <nav class="nav">
        <router-link
          v-for="route in routes"
          :key="route.path"
          :to="route.path"
          class="nav-item"
          :class="{ active: $route.path === route.path }"
        >
          <span class="nav-icon">{{ route.meta?.icon }}</span>
          <span v-show="!sidebarCollapsed" class="nav-label">{{ route.meta?.title }}</span>
        </router-link>
      </nav>

      <div class="sidebar-footer">
        <div class="server-status">
          <span class="status-dot" :class="online ? 'green' : 'red'"></span>
        </div>
        <button class="collapse-btn" @click="sidebarCollapsed = !sidebarCollapsed">
          <span>{{ sidebarCollapsed ? '☰' : '◀' }}</span>
        </button>
      </div>
    </aside>

    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { healthCheck } from './api'

const router = useRouter()
const routes = router.options.routes.filter(r => r.path !== '/')
const sidebarCollapsed = ref(false)
const online = ref(false)

onMounted(async () => {
  try {
    await healthCheck()
    online.value = true
  } catch {}
})
</script>

<style>
/* ========== Design Tokens ========== */
:root {
  --bg-primary: #0b0e14;
  --bg-secondary: #121720;
  --bg-card: #1a202c;
  --bg-card-hover: #1f2633;
  --bg-sidebar: #0d1117;
  --border: #1e2533;
  --border-light: #2a3344;
  --text-primary: #e2e8f0;
  --text-secondary: #8892a6;
  --text-muted: #4a5568;
  --accent: #1d9bf0;
  --accent-hover: #3baff5;
  --green: #22c55e;
  --red: #ef4444;
  --yellow: #eab308;
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 14px;
  --shadow: 0 1px 3px rgba(0,0,0,0.3), 0 1px 2px rgba(0,0,0,0.2);
  --shadow-lg: 0 4px 16px rgba(0,0,0,0.3);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', Roboto, 'Noto Sans SC', 'PingFang SC', system-ui, sans-serif;
  background: var(--bg-primary);
  color: var(--text-primary);
  min-height: 100vh;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#app {
  min-height: 100vh;
}

/* ========== Layout ========== */
.app-layout {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 220px;
  background: var(--bg-sidebar);
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  transition: width 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  flex-shrink: 0;
  position: sticky;
  top: 0;
  height: 100vh;
  overflow: hidden;
}

.sidebar.collapsed {
  width: 60px;
}

.logo {
  padding: 20px 16px;
  display: flex;
  align-items: center;
  gap: 10px;
  border-bottom: 1px solid var(--border);
  min-height: 68px;
}

.logo-svg {
  flex-shrink: 0;
  color: var(--accent);
}

.logo-text {
  font-size: 18px;
  font-weight: 700;
  letter-spacing: -0.3px;
  background: linear-gradient(135deg, #e2e8f0, #94a3b8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.nav {
  flex: 1;
  padding: 12px 8px;
  display: flex;
  flex-direction: column;
  gap: 2px;
  overflow-y: auto;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  text-decoration: none;
  transition: all 0.15s ease;
  font-size: 14px;
  position: relative;
}

.nav-item:hover {
  background: var(--bg-card);
  color: var(--text-primary);
}

.nav-item.active {
  background: rgba(29, 155, 240, 0.1);
  color: var(--accent);
}

.nav-item.active::before {
  content: '';
  position: absolute;
  left: -8px;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 20px;
  background: var(--accent);
  border-radius: 0 3px 3px 0;
}

.nav-icon {
  font-size: 16px;
  width: 24px;
  text-align: center;
  flex-shrink: 0;
}

.sidebar-footer {
  padding: 12px 8px;
  border-top: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.server-status { padding-left: 12px; }
.status-dot { width: 8px; height: 8px; border-radius: 50%; display: block; }
.status-dot.green { background: var(--green); box-shadow: 0 0 6px rgba(34,197,94,0.4); }
.status-dot.red { background: var(--red); }

.collapse-btn {
  padding: 6px 10px;
  background: transparent;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  color: var(--text-muted);
  cursor: pointer;
  font-size: 12px;
  transition: all 0.15s;
}

.collapse-btn:hover {
  background: var(--bg-card);
  color: var(--text-primary);
}

.main-content {
  flex: 1;
  padding: 32px;
  overflow-y: auto;
  max-width: 960px;
}

/* ========== Common Components ========== */
.page-title {
  font-size: 26px;
  font-weight: 700;
  letter-spacing: -0.5px;
  margin-bottom: 24px;
  color: var(--text-primary);
}

.card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 20px;
  transition: border-color 0.2s;
}

.card:hover {
  border-color: var(--border-light);
}

.input {
  width: 100%;
  padding: 10px 14px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border);
  background: var(--bg-secondary);
  color: var(--text-primary);
  font-size: 14px;
  transition: border-color 0.2s;
  outline: none;
}

.input:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(29, 155, 240, 0.1);
}

.input::placeholder {
  color: var(--text-muted);
}

.btn {
  padding: 9px 18px;
  border-radius: var(--radius-md);
  border: none;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.15s;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.btn-primary {
  background: var(--accent);
  color: #fff;
}

.btn-primary:hover {
  background: var(--accent-hover);
}

.btn-sm {
  padding: 6px 12px;
  font-size: 12px;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.badge {
  padding: 2px 8px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 500;
}

.badge-green {
  background: rgba(34, 197, 94, 0.12);
  color: var(--green);
  border: 1px solid rgba(34, 197, 94, 0.2);
}

.badge-blue {
  background: rgba(29, 155, 240, 0.12);
  color: var(--accent);
  border: 1px solid rgba(29, 155, 240, 0.2);
}

.badge-gray {
  background: rgba(74, 85, 104, 0.2);
  color: var(--text-muted);
}

/* ========== Scrollbar ========== */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: var(--border);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: var(--border-light);
}
</style>