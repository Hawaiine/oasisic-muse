<template>
  <div class="dashboard">
    <div class="page-header">
      <n-page-header title="总览" subtitle="Oasisic Muse 系统概览" />
      <n-space>
        <n-tag type="info" round>
          v0.3.0
        </n-tag>
        <n-button size="small" @click="refresh">
          <template #icon>
            <n-icon><refresh-outline /></n-icon>
          </template>
          刷新
        </n-button>
      </n-space>
    </div>

    <n-grid :cols="4" :x-gap="14" :y-gap="14" responsive="screen">
      <n-grid-item v-for="stat in stats" :key="stat.key">
        <n-card :bordered="false" embedded>
          <n-statistic :label="stat.label" :value="stat.value">
            <template #prefix>
              <n-icon :component="stat.icon" :size="20" :color="stat.color" />
            </template>
          </n-statistic>
        </n-card>
      </n-grid-item>
    </n-grid>

    <n-grid :cols="2" :x-gap="14" :y-gap="14" responsive="screen" style="margin-top: 14px;">
      <n-grid-item>
        <n-card title="服务状态" :bordered="false" embedded>
          <n-space vertical :size="12">
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
          </n-space>
        </n-card>
      </n-grid-item>

      <n-grid-item>
        <n-card title="快速操作" :bordered="false" embedded>
          <n-space vertical :size="8">
            <n-button block quaternary @click="$router.push('/search')">
              <template #icon>
                <n-icon><search-outline /></n-icon>
              </template>
              搜索资源
            </n-button>
            <n-button block quaternary @click="$router.push('/subscribe')">
              <template #icon>
                <n-icon><list-outline /></n-icon>
              </template>
              管理订阅
            </n-button>
            <n-button block quaternary @click="$router.push('/settings')">
              <template #icon>
                <n-icon><settings-outline /></n-icon>
              </template>
              系统设置
            </n-button>
          </n-space>
        </n-card>
      </n-grid-item>
    </n-grid>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { NIcon } from 'naive-ui'
import {
  RefreshOutline,
  SearchOutline,
  ListOutline,
  SettingsOutline,
} from 'vicons/ionicons5'

const stats = ref([
  { key: 'subscribes', label: '订阅数', value: 0, icon: ListOutline, color: '#1d9bf0' },
  { key: 'downloads', label: '下载总量', value: 0, icon: SearchOutline, color: '#22c55e' },
  { key: 'done', label: '已完成', value: 0, icon: SettingsOutline, color: '#eab308' },
  { key: 'pending', label: '等待中', value: 0, icon: RefreshOutline, color: '#ef4444' },
])
const backendStatus = ref(false)
const notifyConfigured = ref(false)
const engineRunning = ref(false)

function renderIcon(component: any) {
  return () => h(NIcon, null, { default: () => h(component) })
}

async function refresh() {
  await load()
}

async function load() {
  try {
    await import('../api').then(m => m.healthCheck())
    backendStatus.value = true
  } catch { backendStatus.value = false }

  try {
    const s = await import('../api').then(m => m.getDownloadStats())
    Object.assign(stats.value[0], { value: s?.subscribes ?? 0 })
  } catch {}

  try {
    const n = await import('../api').then(m => m.getNotifyStatus())
    notifyConfigured.value = (n as any)?.channels?.some((c: any) => c.configured)
  } catch {}

  try {
    const l = await import('../api').then(m => m.getLimits())
    engineRunning.value = (l as any)?.enabled
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
