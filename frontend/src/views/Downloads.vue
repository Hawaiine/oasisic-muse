<template>
  <div class="downloads-page">
    <h1 class="page-title">下载任务</h1>
    <div class="stats-row">
      <span>总计: {{ stats.total }}</span>
      <span>完成: {{ stats.done }}</span>
      <span>下载中: {{ stats.downloading }}</span>
      <span>等待: {{ stats.pending }}</span>
    </div>
    <div class="list">
      <div v-for="task in tasks" :key="task.id" class="task-item">
        <div class="task-info">
          <div class="task-title">{{ task.title }}</div>
          <div class="task-meta">{{ task.site }} · {{ task.status }}</div>
        </div>
        <span class="badge" :class="statusClass(task.status)">{{ statusLabel(task.status) }}</span>
      </div>
      <div v-if="tasks.length === 0" class="empty">暂无下载任务</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getDownloads, getDownloadStats } from '../api'

const tasks = ref<any[]>([])
const stats = ref({ total: 0, done: 0, downloading: 0, pending: 0 })

function statusClass(status: string) {
  const map: Record<string, string> = { done: 'badge-green', downloading: 'badge-blue', pending: 'badge-gray', failed: 'badge-red' }
  return map[status] || 'badge-gray'
}
function statusLabel(status: string) {
  const map: Record<string, string> = { done: '已完成', downloading: '下载中', pending: '等待中', failed: '失败' }
  return map[status] || status
}

onMounted(async () => {
  try {
    const [t, s] = await Promise.all([getDownloads(), getDownloadStats()])
    tasks.value = (t as any).items || []
    stats.value = s as any
  } catch {}
})
</script>

<style scoped>
.downloads-page { max-width: 800px; }
.page-title { font-size: 24px; margin-bottom: 16px; color: #e1e8ed; }
.stats-row { display: flex; gap: 20px; margin-bottom: 20px; font-size: 13px; color: #8899a6; }
.list { display: flex; flex-direction: column; gap: 8px; }
.task-item { display: flex; justify-content: space-between; align-items: center; padding: 14px 16px; background: #1a1f2e; border-radius: 10px; }
.task-title { font-size: 14px; color: #e1e8ed; margin-bottom: 4px; }
.task-meta { font-size: 12px; color: #8899a6; }
.badge { padding: 3px 10px; border-radius: 20px; font-size: 12px; }
.badge-green { background: #00ba7c20; color: #00ba7c; border: 1px solid #00ba7c; }
.badge-blue { background: #1d9bf020; color: #1d9bf0; border: 1px solid #1d9bf0; }
.badge-gray { background: #2a3040; color: #8899a6; }
.badge-red { background: #f4212e20; color: #f4212e; border: 1px solid #f4212e; }
.empty { text-align: center; padding: 40px; color: #556; font-size: 14px; }
</style>