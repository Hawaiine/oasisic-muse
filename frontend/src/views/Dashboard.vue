<template>
  <div class="dashboard">
    <n-page-header title="总览" subtitle="Oasisic Muse 系统概览" style="margin-bottom: 24px;">
      <template #extra>
        <n-space>
          <n-tag type="info" round>
            v{{ version }}
          </n-tag>
          <n-button @click="load" size="small">
            🔄 刷新
          </n-button>
        </n-space>
      </template>
    </n-page-header>

    <!-- 统计卡片 -->
    <n-grid :cols="4" :x-gap="16" :y-gap="16" responsive="screen">
      <n-grid-item>
        <n-card :bordered="false" embedded>
          <n-statistic label="订阅数" :value="subCount">
            <template #prefix>
              <n-icon :component="BookOutline" size="18" />
            </template>
          </n-statistic>
        </n-card>
      </n-grid-item>
      <n-grid-item>
        <n-card :bordered="false" embedded>
          <n-statistic label="下载中" :value="dlCount">
            <template #prefix>
              <n-icon :component="DownloadOutline" size="18" />
            </template>
          </n-statistic>
        </n-card>
      </n-grid-item>
      <n-grid-item>
        <n-card :bordered="false" embedded>
          <n-statistic label="种子数" :value="seederCount">
            <template #prefix>
              <n-icon :component="TrendingUpOutline" size="18" />
            </template>
          </n-statistic>
        </n-card>
      </n-grid-item>
      <n-grid-item>
        <n-card :bordered="false" embedded>
          <n-statistic label="状态">
            <template #default>
              <n-tag :type="online ? 'success' : 'error'" round size="small">
                {{ online ? '在线' : '离线' }}
              </n-tag>
            </template>
            <template #prefix>
              <n-icon :component="WifiOutline" size="18" />
            </template>
          </n-statistic>
        </n-card>
      </n-grid-item>
    </n-grid>

    <!-- 快捷入口 -->
    <n-grid :cols="3" :x-gap="16" :y-gap="16" responsive="screen" style="margin-top: 16px;">
      <n-grid-item>
        <n-card :bordered="false" embedded hoverable>
          <template #header>
            <n-space>
              <n-icon :component="SearchOutline" size="18" />
              <n-text strong>快速搜索</n-text>
            </n-space>
          </template>
          <n-text depth="3" style="font-size: 13px;">输入番号搜索 PT 资源</n-text>
          <template #footer>
            <n-button text type="primary" size="small" @click="$router.push('/search')">
              去搜索 →
            </n-button>
          </template>
        </n-card>
      </n-grid-item>
      <n-grid-item>
        <n-card :bordered="false" embedded hoverable>
          <template #header>
            <n-space>
              <n-icon :component="AddOutline" size="18" />
              <n-text strong>新建订阅</n-text>
            </n-space>
          </template>
          <n-text depth="3" style="font-size: 13px;">添加关键词自动搜索下载</n-text>
          <template #footer>
            <n-button text type="primary" size="small" @click="$router.push('/subscribe')">
              去订阅 →
            </n-button>
          </template>
        </n-card>
      </n-grid-item>
      <n-grid-item>
        <n-card :bordered="false" embedded hoverable>
          <template #header>
            <n-space>
              <n-icon :component="SettingsOutline" size="18" />
              <n-text strong>系统设置</n-text>
            </n-space>
          </template>
          <n-text depth="3" style="font-size: 13px;">配置 qBittorrent、PT 站点、通知</n-text>
          <template #footer>
            <n-button text type="primary" size="small" @click="$router.push('/settings')">
              去设置 →
            </n-button>
          </template>
        </n-card>
      </n-grid-item>
    </n-grid>

    <!-- 最近下载 -->
    <n-card :bordered="false" embedded style="margin-top: 16px;">
      <template #header>
        <n-space>
          <n-icon :component="ListOutline" size="18" />
          <n-text strong>最近下载</n-text>
        </n-space>
      </template>
      <n-empty v-if="downloads.length === 0" description="暂无下载记录" />
      <n-data-table v-else :columns="dlColumns" :data="downloads" :bordered="false" :striped="true" :pagination="false" size="small" />
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, h } from 'vue'
import type { DataTableColumns } from 'naive-ui'
import { useMessage } from 'naive-ui'
import {
  BookOutline, DownloadOutline, TrendingUpOutline, WifiOutline,
  SearchOutline, AddOutline, SettingsOutline, ListOutline
} from 'vicons/ionicons5'
import { getSubscribes, getDownloads, getDownloadStats, healthCheck } from '../api'

const message = useMessage()
const version = ref('0.3.0')
const online = ref(false)
const subCount = ref(0)
const dlCount = ref(0)
const seederCount = ref(0)
const downloads = ref<any[]>([])

const dlColumns: DataTableColumns<any> = [
  { title: '名称', key: 'name', ellipsis: { tooltip: true } },
  { title: '大小', key: 'size' },
  { title: '进度', key: 'progress', render(row) {
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
    await healthCheck()
    online.value = true
  } catch {
    online.value = false
  }

  try {
    const subs = await getSubscribes()
    subCount.value = (subs as any[]).length
  } catch {}

  try {
    const stats = await getDownloadStats()
    const s = stats as any
    dlCount.value = s.total || 0
    seederCount.value = s.seeders || 0
  } catch {}

  try {
    downloads.value = await getDownloads()
  } catch {}
}

onMounted(load)
</script>

<style scoped>
.dashboard { max-width: 960px; }
.n-card { border-radius: 12px !important; }
</style>
