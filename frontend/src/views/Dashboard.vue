<template>
  <div class="dashboard">
    <div class="page-header">
      <h1 class="page-title">总览</h1>
      <div class="header-actions">
        <span class="version-badge">v0.3.0</span>
        <button class="btn btn-sm" @click="refresh">🔄 刷新</button>
      </div>
    </div>

    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon-box" style="background:rgba(29,155,240,0.12);color:var(--accent)">📋</div>
        <div class="stat-body">
          <div class="stat-value">{{ stats.subscribes }}</div>
          <div class="stat-label">订阅数</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon-box" style="background:rgba(34,197,94,0.12);color:var(--green)">⬇️</div>
        <div class="stat-body">
          <div class="stat-value">{{ stats.downloads }}</div>
          <div class="stat-label">下载总量</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon-box" style="background:rgba(234,179,8,0.12);color:var(--yellow)">✅</div>
        <div class="stat-body">
          <div class="stat-value">{{ stats.done }}</div>
          <div class="stat-label">已完成</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon-box" style="background:rgba(239,68,68,0.12);color:var(--red)">⏳</div>
        <div class="stat-body">
          <div class="stat-value">{{ stats.pending }}</div>
          <div class="stat-label">等待中</div>
        </div>
      </div>
    </div>

    <div class="content-grid">
      <div class="card">
        <h3 class="card-title">服务状态</h3>
        <div class="service-list">
          <div class="service-item">
            <span class="status-indicator" :class="backendStatus ? 'green' : 'red'"></span>
            <span class="service-name">后端服务</span>
            <span class="service-status">{{ backendStatus ? '运行中' : '离线' }}</span>
          </div>
          <div class="service-item">
            <span class="status-indicator" :class="notifyConfigured ? 'green' : 'yellow'"></span>
            <span class="service-name">通知</span>
            <span class="service-status">{{ notifyConfigured ? '已配置' : '未配置' }}</span>
          </div>
          <div class="service-item">
            <span class="status-indicator" :class="engineRunning ? 'green' : 'yellow'"></span>
            <span class="service-name">订阅引擎</span>
            <span class="service-status">{{ engineRunning ? '运行中' : '已暂停' }}</span>
          </div>
        </div>
      </div>

      <div class="card">
        <h3 class="card-title">快速操作</h3>
        <div class="quick-actions">
          <router-link to="/search" class="action-btn">
            <span class="action-icon">🔍</span>
            <span>搜索资源</span>
          </router-link>
          <router-link to="/subscribe" class="action-btn">
            <span class="action-icon">📋</span>
            <span>管理订阅</span>
          </router-link>
          <router-link to="/settings" class="action-btn">
            <span class="action-icon">⚙️</span>
            <span>系统设置</span>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { healthCheck, getDownloadStats, getNotifyStatus, getLimits } from '../api'

const stats = ref({ subscribes: 0, downloads: 0, done: 0, pending: 0 })
const backendStatus = ref(false)
const notifyConfigured = ref(false)
const engineRunning = ref(false)

async function refresh() {
  await load()
}

async function load() {
  try {
    await healthCheck()
    backendStatus.value = true
  } catch { backendStatus.value = false }

  try {
    const s = await getDownloadStats()
    stats.value = s as any
  } catch {}

  try {
    const n = await getNotifyStatus()
    notifyConfigured.value = (n as any).channels?.some((c: any) => c.configured)
  } catch {}

  try {
    const l = await getLimits()
    engineRunning.value = (l as any).enabled
  } catch {}
}

onMounted(load)
</script>

<style scoped>
.dashboard { max-width: 800px; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.header-actions { display: flex; align-items: center; gap: 10px; }
.version-badge { font-size: 11px; color: var(--text-muted); background: var(--bg-card); padding: 3px 10px; border-radius: 20px; border: 1px solid var(--border); }

.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 14px; margin-bottom: 24px; }
.stat-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 20px; display: flex; align-items: center; gap: 16px; }
.stat-icon-box { width: 44px; height: 44px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 20px; flex-shrink: 0; }
.stat-body { flex: 1; }
.stat-value { font-size: 28px; font-weight: 700; color: var(--text-primary); line-height: 1.2; }
.stat-label { font-size: 12px; color: var(--text-muted); margin-top: 2px; }

.content-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }

.card-title { font-size: 15px; font-weight: 600; margin-bottom: 16px; color: var(--text-primary); }

.service-list { display: flex; flex-direction: column; gap: 12px; }
.service-item { display: flex; align-items: center; gap: 10px; font-size: 14px; }
.status-indicator { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.status-indicator.green { background: var(--green); }
.status-indicator.red { background: var(--red); }
.status-indicator.yellow { background: var(--yellow); }
.service-name { flex: 1; color: var(--text-secondary); }
.service-status { font-size: 12px; color: var(--text-muted); }

.quick-actions { display: flex; flex-direction: column; gap: 8px; }
.action-btn { display: flex; align-items: center; gap: 10px; padding: 11px 14px; border-radius: var(--radius-md); background: var(--bg-secondary); color: var(--text-secondary); text-decoration: none; font-size: 14px; transition: all 0.15s; border: 1px solid transparent; }
.action-btn:hover { background: var(--bg-card-hover); border-color: var(--border); color: var(--text-primary); }
.action-icon { font-size: 16px; width: 20px; text-align: center; }

@media (max-width: 640px) {
  .content-grid { grid-template-columns: 1fr; }
}
</style>