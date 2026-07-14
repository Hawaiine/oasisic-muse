<template>
  <div class="library-page">
    <h1 class="page-title">媒体库</h1>

    <div class="status-card">
      <h3>连接状态</h3>
      <div class="status-row" v-if="status.connected">
        <span class="status-dot green"></span>
        <span>{{ status.server_name }} (v{{ status.version }}) — 已连接 ✅</span>
      </div>
      <div class="status-row" v-else>
        <span class="status-dot red"></span>
        <span>未连接 — 请在设置中配置 EMBY/Jellyfin 地址</span>
      </div>
      <button class="btn btn-sm" @click="refresh">刷新媒体库</button>
    </div>

    <div class="recent-section" v-if="items.length > 0">
      <h3>最近添加</h3>
      <div class="media-grid">
        <div v-for="item in items" :key="item.Id" class="media-card">
          <div class="media-thumb">
            <img v-if="item.ImageTags?.Primary"
              :src="`${apiBase}/Items/${item.Id}/Images/Primary?fillColor=1a1f2e`"
              :alt="item.Name" />
            <div v-else class="media-placeholder">🎬</div>
          </div>
          <div class="media-name">{{ item.Name }}</div>
          <div class="media-year">{{ item.ProductionYear || '' }}</div>
        </div>
      </div>
    </div>
    <div v-else class="placeholder">
      <p v-if="status.connected">媒体库为空，等待下载刮削完成</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getLibraryStatus, getRecentMedia, refreshLibrary as refreshLib } from '../api'

const status = ref<any>({ connected: false })
const items = ref<any[]>([])
const apiBase = ref('')

async function refresh() {
  await refreshLib()
}

onMounted(async () => {
  try {
    const [s, r] = await Promise.all([
      getLibraryStatus(),
      getRecentMedia(12),
    ])
    status.value = s as any
    items.value = (r as any).items || []
    // 从设置中获取 EMBY 地址
    apiBase.value = (s as any).emby_host || ''
  } catch {}
})
</script>

<style scoped>
.library-page { max-width: 800px; }
.page-title { font-size: 24px; margin-bottom: 20px; color: #e1e8ed; }
.status-card { background: #1a1f2e; border-radius: 12px; padding: 20px; margin-bottom: 20px; }
.status-card h3 { font-size: 16px; margin-bottom: 12px; color: #e1e8ed; }
.status-row { display: flex; align-items: center; gap: 10px; padding: 8px 0; font-size: 14px; color: #8899a6; }
.status-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }
.status-dot.green { background: #00ba7c; }
.status-dot.red { background: #f4212e; }
.btn { padding: 8px 16px; border-radius: 8px; border: none; cursor: pointer; font-size: 13px; background: #1d9bf0; color: #fff; margin-top: 10px; }
.btn-sm { padding: 6px 12px; }
.recent-section h3 { font-size: 16px; margin-bottom: 12px; color: #e1e8ed; }
.media-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 12px; }
.media-card { background: #1a1f2e; border-radius: 10px; overflow: hidden; }
.media-thumb { width: 100%; aspect-ratio: 2/3; background: #2a3040; display: flex; align-items: center; justify-content: center; }
.media-thumb img { width: 100%; height: 100%; object-fit: cover; }
.media-placeholder { font-size: 32px; opacity: 0.3; }
.media-name { padding: 8px 10px 2px; font-size: 13px; color: #e1e8ed; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.media-year { padding: 0 10px 10px; font-size: 11px; color: #556; }
.placeholder { text-align: center; padding: 60px 20px; background: #1a1f2e; border-radius: 12px; color: #8899a6; }
</style>