<template>
  <div class="downloads-page">
    <n-page-header title="下载任务" subtitle="查看和管理 qBittorrent 下载队列" style="margin-bottom: 24px;">
      <template #extra>
        <n-button @click="load" size="small">🔄 刷新</n-button>
      </template>
    </n-page-header>

    <n-grid :cols="3" :x-gap="16" :y-gap="16" responsive="screen" style="margin-bottom: 16px;">
      <n-grid-item>
        <n-card :bordered="false" embedded>
          <n-statistic label="总下载数">
            <template #prefix><n-icon :component="DownloadOutline" /></template>
            {{ stats.total }}
          </n-statistic>
        </n-card>
      </n-grid-item>
      <n-grid-item>
        <n-card :bordered="false" embedded>
          <n-statistic label="活跃种子">
            <template #prefix><n-icon :component="TrendingUpOutline" /></template>
            {{ stats.seeders }}
          </n-statistic>
        </n-card>
      </n-grid-item>
      <n-grid-item>
        <n-card :bordered="false" embedded>
          <n-statistic label="连接状态">
            <template #prefix><n-icon :component="WifiOutline" /></template>
            <template #default>
              <n-tag :type="stats.connected ? 'success' : 'error'" round size="small">
                {{ stats.connected ? '已连接' : '未连接' }}
              </n-tag>
            </template>
          </n-statistic>
        </n-card>
      </n-grid-item>
    </n-grid>

    <n-card :bordered="false" embedded>
      <n-data-table
        :columns="columns"
        :data="downloads"
        :bordered="false"
        :striped="true"
        :pagination="{ pageSize: 10 }"
        size="small"
      />
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, h } from 'vue'
import type { DataTableColumns } from 'naive-ui'
import { DownloadOutline, TrendingUpOutline, WifiOutline } from '@vicons/ionicons5'
import { getDownloads, getDownloadStats } from '../api'

const stats = ref({ total: 0, seeders: 0, connected: false })
const downloads = ref<any[]>([])

const columns: DataTableColumns<any> = [
  { title: '名称', key: 'name', ellipsis: { tooltip: true } },
  { title: '大小', key: 'size' },
  { title: '进度', key: 'progress', width: 150, render(row) {
    return h('n-progress', {
      percentage: row.progress || 0,
      type: 'line',
      indicator: 'inside',
      strokeWidth: 6,
    })
  }},
  { title: '状态', key: 'state' },
]

async function load() {
  try {
    const s = await getDownloadStats()
    stats.value = s as any
  } catch {}
  try {
    downloads.value = await getDownloads()
  } catch {}
}

onMounted(load)
</script>

<style scoped>
.downloads-page { max-width: 960px; }
</style>
