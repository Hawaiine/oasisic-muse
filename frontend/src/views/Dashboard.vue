<template>
  <div class="dashboard">
    <h1 class="page-title">总览</h1>
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">📋</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.subscribes }}</div>
          <div class="stat-label">订阅数</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">⬇️</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.downloads }}</div>
          <div class="stat-label">下载总量</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">✅</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.done }}</div>
          <div class="stat-label">已完成</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">⏳</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.pending }}</div>
          <div class="stat-label">等待中</div>
        </div>
      </div>
    </div>
    <div class="status-card">
      <h3>服务状态</h3>
      <div class="status-row">
        <span class="status-dot" :class="backendStatus ? 'green' : 'red'"></span>
        <span>后端服务 {{ backendStatus ? '运行中 ✅' : '离线 ❌' }}</span>
      </div>
      <div class="status-row">
        <span class="status-dot" :class="notifyConfigured ? 'green' : 'yellow'"></span>
        <span>通知配置 {{ notifyConfigured ? '已配置' : '未配置' }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { healthCheck, getDownloadStats, getNotifyStatus } from '../api'

const stats = ref({ subscribes: 0, downloads: 0, done: 0, pending: 0 })
const backendStatus = ref(false)
const notifyConfigured = ref(false)

onMounted(async () => {
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
})
</script>

<style scoped>
.dashboard { max-width: 900px; }
.page-title { font-size: 24px; margin-bottom: 20px; color: #e1e8ed; }
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; margin-bottom: 24px; }
.stat-card { background: #1a1f2e; border-radius: 12px; padding: 20px; display: flex; align-items: center; gap: 16px; }
.stat-icon { font-size: 32px; }
.stat-value { font-size: 28px; font-weight: 700; color: #e1e8ed; }
.stat-label { font-size: 13px; color: #8899a6; }
.status-card { background: #1a1f2e; border-radius: 12px; padding: 20px; }
.status-card h3 { font-size: 16px; margin-bottom: 12px; color: #e1e8ed; }
.status-row { display: flex; align-items: center; gap: 10px; padding: 8px 0; font-size: 14px; color: #8899a6; }
.status-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }
.status-dot.green { background: #00ba7c; }
.status-dot.red { background: #f4212e; }
.status-dot.yellow { background: #ffd400; }
</style>