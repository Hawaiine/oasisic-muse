<template>
  <div class="dashboard">
    <div class="page-header">
      <n-page-header title="总览" subtitle="Oasisic Muse 系统概览" />
      <n-space>
        <n-tag type="info" round>
          v0.3.0
        </n-tag>
        <n-button size="small" @click="refresh">
          刷新
        </n-button>
      </n-space>
    </div>

    <n-grid :cols="4" :x-gap="14" :y-gap="14" responsive="screen">
      <n-grid-item v-for="stat in stats" :key="stat.key">
        <n-card :bordered="false" embedded>
          <n-statistic :label="stat.label" :value="stat.value" :style="{ color: stat.color }">
            <template #prefix>
              <span :style="{ fontSize: '20px' }">{{ stat.icon }}</span>
            </template>
          </n-statistic>
        </n-card>
      </n-grid-item>
    </n-grid>

    <n-grid :cols="2" :x-gap="14" :y-gap="14" responsive="screen" style="margin-top: 14px;">
      <n-grid-item>
        <n-card title="服务状态" :bordered="false" embedded>
          <n-list>
            <n-list-item>
              <n-list-item-meta description="FastAPI 后端服务">
                <template #avatar>
                  <n-tag :bordered="false" :type="backendStatus ? 'success' : 'error'" round size="small">
                    {{ backendStatus ? '运行中' : '离线' }}
                  </n-tag>
                </template>
              </n-list-item-meta>
            </n-list-item>
            <n-list-item>
              <n-list-item-meta description="通知推送通道">
                <template #avatar>
                  <n-tag :bordered="false" :type="notifyConfigured ? 'success' : 'warning'" round size="small">
                    {{ notifyConfigured ? '已配置' : '未配置' }}
                  </n-tag>
                </template>
              </n-list-item-meta>
            </n-list-item>
            <n-list-item>
              <n-list-item-meta description="订阅引擎调度器">
                <template #avatar>
                  <n-tag :bordered="false" :type="engineRunning ? 'success' : 'warning'" round size="small">
                    {{ engineRunning ? '运行中' : '已暂停' }}
                  </n-tag>
                </template>
              </n-list-item-meta>
            </n-list-item>
          </n-list>
        </n-card>
      </n-grid-item>

      <n-grid-item>
        <n-card title="快速操作" :bordered="false" embedded>
          <n-space vertical :size="8">
            <n-button block quaternary @click="$router.push('/search')">
              🔍 搜索资源
            </n-button>
            <n-button block quaternary @click="$router.push('/subscribe')">
              📋 管理订阅
            </n-button>
            <n-button block quaternary @click="$router.push('/settings')">
              ⚙️ 系统设置
            </n-button>
          </n-space>
        </n-card>
      </n-grid-item>
    </n-grid>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { healthCheck, getDownloadStats, getNotifyStatus, getLimits } from '../api'

const stats = ref([
  { key: 'subscribes', label: '订阅数', value: 0, icon: '📋', color: '#1d9bf0' },
  { key: 'downloads', label: '下载总量', value: 0, icon: '⬇️', color: '#22c55e' },
  { key: 'done', label: '已完成', value: 0, icon: '✅', color: '#eab308' },
  { key: 'pending', label: '等待中', value: 0, icon: '⏳', color: '#ef4444' },
])
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
    stats.value[0].value = (s as any).subscribes ?? 0
    stats.value[1].value = (s as any).downloads ?? 0
    stats.value[2].value = (s as any).done ?? 0
    stats.value[3].value = (s as any).pending ?? 0
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
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
}
.page-header .n-page-header { padding: 0; }
</style>
