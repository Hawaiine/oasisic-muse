<template>
  <div class="library-page">
    <div class="page-header">
      <h2>媒体库</h2>
      <p>Jellyfin / EMBY 媒体管理</p>
    </div>

    <div class="grid grid-cols-2">
      <div class="card">
        <div style="font-size: 15px; font-weight: 600; margin-bottom: 12px;">Jellyfin</div>
        <div style="font-size: 13px; color: var(--text-muted); margin-bottom: 12px;">
          {{ jellyfinConfig?.url ? '已配置' : '未配置' }}
        </div>
        <button class="btn btn-sm" @click="refreshLibrary('jellyfin')">🔄 刷新</button>
      </div>
      <div class="card">
        <div style="font-size: 15px; font-weight: 600; margin-bottom: 12px;">Emby</div>
        <div style="font-size: 13px; color: var(--text-muted); margin-bottom: 12px;">
          {{ embyConfig?.url ? '已配置' : '未配置' }}
        </div>
        <button class="btn btn-sm" @click="refreshLibrary('emby')">🔄 刷新</button>
      </div>
    </div>

    <div class="card" style="margin-top: 16px;">
      <div style="font-size: 15px; font-weight: 600; margin-bottom: 12px;">媒体列表</div>
      <table v-if="items.length > 0">
        <thead>
          <tr>
            <th>名称</th>
            <th>类型</th>
            <th>年份</th>
            <th>评分</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in items" :key="item.id">
            <td style="color: var(--text-primary);">{{ item.name }}</td>
            <td>{{ item.type }}</td>
            <td>{{ item.year }}</td>
            <td>⭐ {{ item.rating }}</td>
          </tr>
        </tbody>
      </table>
      <div v-else class="empty-state">
        <div class="empty-state-icon">📚</div>
        <div class="empty-state-text">暂无媒体数据</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { api } from '@/api'

const jellyfinConfig = ref<any>(null)
const embyConfig = ref<any>(null)
const items = ref<any[]>([])

async function refreshLibrary(source: string) {
  try {
    await api('/api/library/refresh', { method: 'POST', params: { source } })
  } catch (e) {
    console.error(e)
  }
}

onMounted(async () => {
  try {
    const res = await api('/api/settings')
    jellyfinConfig.value = res.media?.jellyfin
    embyConfig.value = res.media?.emby
  } catch {
    // ignore
  }
})
</script>
