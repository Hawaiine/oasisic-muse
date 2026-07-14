<template>
  <div class="downloads-page">
    <n-page-header title="下载任务" subtitle="查看和管理下载队列">
      <template #extra>
        <n-button @click="load">刷新</n-button>
      </template>
    </n-page-header>

    <n-grid :cols="4" :x-gap="14" :y-gap="14" responsive="screen">
      <n-grid-item>
        <n-card :bordered="false" embedded>
          <n-statistic label="总计" :value="stats.total" />
        </n-card>
      </n-grid-item>
      <n-grid-item>
        <n-card :bordered="false" embedded>
          <n-statistic label="已完成" :value="stats.done" />
        </n-card>
      </n-grid-item>
      <n-grid-item>
        <n-card :bordered="false" embedded>
          <n-statistic label="下载中" :value="stats.downloading" />
        </n-card>
      </n-grid-item>
      <n-grid-item>
        <n-card :bordered="false" embedded>
          <n-statistic label="等待中" :value="stats.pending" />
        </n-card>
      </n-grid-item>
    </n-grid>

    <n-card title="任务列表" :bordered="false" embedded style="margin-top: 16px;">
      <n-empty v-if="tasks.length === 0" description="暂无下载任务" />
      <n-data-table v-else :columns="columns" :data="tasks" :bordered="false" :single-line="false" />
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, h } from 'vue'
import type { DataTableColumns } from 'naive-ui'
import { getDownloads, getDownloadStats } from '../api'

const tasks = ref<any[]>([])
const stats = ref({ total: 0, done: 0, downloading: 0, pending: 0 })

const columns: DataTableColumns<any> = [
  { title: '标题', key: 'title' },
  { title: '站点', key: 'site' },
  {
    title: '状态',
    key: 'status',
    render(row) {
      const type = row.status === 'completed' ? 'success' :
                   row.status === 'downloading' ? 'primary' :
                   row.status === 'pending' ? 'warning' : 'error'
      return h('n-tag', { type, size: 'small', round: true }, () => row.status)
    },
  },
  { title: '进度', key: 'progress', render(row) {
    return h('n-progress', {
      percentage: row.progress ?? 0,
      type: 'success',
      indicator: 'inside',
    })
  }},
]

async function load() {
  try {
    tasks.value = await getDownloads()
    const s = await getDownloadStats()
    Object.assign(stats.value, s as any)
  } catch {}
}

onMounted(load)
</script>

<style scoped>
.downloads-page { max-width: 960px; }
</style>
