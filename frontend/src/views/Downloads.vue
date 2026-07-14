<template>
  <div class="downloads-page">
    <div class="page-header" style="display: flex; justify-content: space-between; align-items: center;">
      <div>
        <h2>下载任务</h2>
        <p>查看和管理 qBittorrent 下载队列</p>
      </div>
      <button class="btn btn-sm" @click="load">🔄 刷新</button>
    </div>

    <div class="card">
      <table v-if="downloads.length > 0">
        <thead>
          <tr>
            <th>名称</th>
            <th>大小</th>
            <th>进度</th>
            <th>速度</th>
            <th>种子</th>
            <th>状态</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="d in downloads" :key="d.hash">
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
            <td>{{ d.seeds }}</td>
            <td><span :class="['badge', d.state === '下载中' ? 'badge-success' : 'badge-muted']">{{ d.state }}</span></td>
          </tr>
        </tbody>
      </table>
      <div v-else class="empty-state">
        <div class="empty-state-icon">📥</div>
        <div class="empty-state-text">暂无下载任务</div>
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
  seeds: string
  state: string
}

const downloads = ref<DownloadItem[]>([])

async function load() {
  try {
    const res = await api.get('/api/downloads')
    downloads.value = (res.data || []).map((d: any) => ({
      hash: d.hash,
      name: d.name || '未知',
      size: d.size || '0 B',
      progress: Math.round(d.progress || 0),
      speed: d.speed || '0 B/s',
      seeds: d.seeds || '-',
      state: d.state || '未知',
    }))
  } catch {
    downloads.value = []
  }
}

onMounted(load)
</script>
