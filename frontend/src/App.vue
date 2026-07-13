<template>
  <div class="app-layout">
    <aside class="sidebar" :class="{ collapsed: sidebarCollapsed }">
      <div class="logo">
        <span class="logo-icon">🎵</span>
        <span v-show="!sidebarCollapsed" class="logo-text">Oasisic Muse</span>
      </div>
      <nav class="nav">
        <router-link
          v-for="route in routes"
          :key="route.path"
          :to="route.path"
          class="nav-item"
          :class="{ active: $route.path === route.path }"
        >
          <span class="nav-icon">{{ route.meta.icon }}</span>
          <span v-show="!sidebarCollapsed" class="nav-label">{{ route.meta.title }}</span>
        </router-link>
      </nav>
      <div class="sidebar-footer">
        <button class="collapse-btn" @click="sidebarCollapsed = !sidebarCollapsed">
          {{ sidebarCollapsed ? '☰' : '◀' }}
        </button>
      </div>
    </aside>
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const routes = router.options.routes.filter(r => r.path !== '/')
const sidebarCollapsed = ref(false)
</script>

<style>
.app-layout {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 220px;
  background: #1a1f2e;
  display: flex;
  flex-direction: column;
  transition: width 0.2s ease;
  flex-shrink: 0;
}
.sidebar.collapsed {
  width: 60px;
}

.logo {
  padding: 20px 16px;
  display: flex;
  align-items: center;
  gap: 10px;
  border-bottom: 1px solid #2a3040;
}
.logo-icon { font-size: 24px; }
.logo-text { font-size: 16px; font-weight: 600; color: #e1e8ed; }

.nav {
  flex: 1;
  padding: 12px 8px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 8px;
  color: #8899a6;
  text-decoration: none;
  transition: all 0.15s ease;
  font-size: 14px;
}
.nav-item:hover { background: #2a3040; color: #e1e8ed; }
.nav-item.active { background: #1d9bf0; color: #fff; }
.nav-icon { font-size: 18px; width: 24px; text-align: center; }

.sidebar-footer {
  padding: 12px 8px;
  border-top: 1px solid #2a3040;
}
.collapse-btn {
  width: 100%;
  padding: 8px;
  background: transparent;
  border: 1px solid #2a3040;
  border-radius: 6px;
  color: #8899a6;
  cursor: pointer;
  font-size: 14px;
}
.collapse-btn:hover { background: #2a3040; color: #e1e8ed; }

.main-content {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
  background: #0f1419;
}
</style>