<template>
  <div class="dashboard">
    <!-- Stats row -->
    <div class="grid grid-cols-4" style="margin-bottom: 24px;">
      <div class="stat-card">
        <div class="stat-icon" style="background: var(--accent-muted); color: var(--accent);">📡</div>
        <div>
          <div class="stat-value">{{ stats.connected ? '●' : '○' }}</div>
          <div class="stat-label">{{ stats.connected ? '已连接' : '未连接' }}</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background: rgba(59, 130, 246, 0.12); color: #3b82f6;">📥</div>
        <div>
          <div class="stat-value">{{ stats.downloads }}</div>
          <div class="stat-label">下载任务</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background: rgba(168, 85, 247, 0.12); color: #a855f7;">📚</div>
        <div>
          <div class="stat-value">{{ stats.library }}</div>
          <div class="stat-label">媒体总数</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background: rgba(245, 158, 11, 0.12); color: #f59e0b;">🔔</div>
        <div>
          <div class="stat-value">{{ stats.notifications }}</div>
          <div class="stat-label">今日通知</div>
        </div>
      </div>
    </div>

    <!-- Quick actions -->
    <div class="grid grid-cols-3" style="margin-bottom: 24px;">
      <div class="card" style="cursor: pointer;" @click="$router.push('/subscribe')">
        <div style="font-size: 24px; margin-bottom: 8px;">🔍</div>
        <div style="font-size: 14px; font-weight: 500; color: var(--text-primary);">添加订阅</div>
        <div style="font-size: 12px; color: var(--text-muted); margin-top: 4px;">管理自动搜索与下载任务</div>
      </div>
      <div class="card" style="cursor: pointer;" @click="$router.push('/settings')">
        <div style="font-size: 24px; margin-bottom: 8px;">⚙️</div>
        <div style="font-size: 14px; font-weight: 500; color: var(--text-primary);">系统设置</div>
        <div style="font-size: 12px; color: var(--text-muted); margin-top: 4px;">配置下载器、媒体库、通知</div>
      </div>
      <div class="card" style="cursor: pointer;" @click="$router.push('/search')">
        <div style="font-size: 24px; margin-bottom: 8px;">🔎</div>
        <div style="font-size: 14px; font-weight: 500; color: var(--text-primary);">PT 搜索</div>
        <div style="font-size: 12px; color: var(--text-muted); margin-top: 4px;">搜索 PT 站点资源</div>
      </div>
    </div>

    <!-- Recent downloads -->
    <div class="card">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
        <h3 style="font-size: 15px; font-weight: 600; color: var(--text-primary);">最近下载</h3>
        <button class="btn btn-sm" @click="loadDownloads">刷新</button>
      </div>
      <table v-if="downloads.length > 0">
        <thead>
          <tr>
            <th>名称</th>
            <th>大小</th>
            <th>进度</th>
            <th>速度</th>
            <th>状态</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="d in downloads.slice(0, 5)" :key="d.hash">
            <td style="color: var(--text-primary);">{{ d.name }}</td>
            <td>{{ d.size }}</td>
            <td>
              <div style="display: flex; align-items: center; gap: 8px;">
                <div style="flex: 1; height: 4px; background: var(--bg-hover); border-radius: 2px; overflow: hidden;">
                  <div style="height: 100%; width: {{ d.progress }}%; background: var(--accent); border-radius: 2px;"></div>
                </div>
                <span style="font-size: 12px; color: var(--text-muted);">{{ d.progress }}%</span>
              </div>
            </td>
            <td>{{ d.speed }}</td>
            <td><span class="badge badge-success">{{ d.state }}</span></td>
          </tr>
        </tbody>
      </table>
      <div v-else class="empty-state">
        <div class="empty-state-icon">📥</div>
        <div class="empty-state-text">暂无下载任务</div>
        <button class="btn btn-sm" @click="loadDownloads">刷新</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { api } from '@/api'

interface DownloadItem {
  hash: string
  name: string
  size: string
  progress: number
  speed: string
  state: string
}

const stats = ref({
  connected: false,
  downloads: 0,
  library: 0,
  notifications: 0,
})

const downloads = ref<DownloadItem[]>([])

async function load() {
  try {
    const health = await api('/api/health')
    stats.value.connected = health.status === 'ok'
  } catch {
    stats.value.connected = false
  }
  loadDownloads()
}

async function loadDownloads() {
  try {
    const res = await api('/api/downloads')
    downloads.value = (res || []).map((d: any) => ({
      hash: d.hash,
      name: d.name || '未知',
      size: d.size || '0 B',
      progress: Math.round(d.progress || 0),
      speed: d.speed || '0 B/s',
      state: d.state || '未知',
    }))
  } catch {
    downloads.value = []
  }
}

onMounted(load)
</script>
