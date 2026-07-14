<template>
  <div class="library-page">
    <n-page-header title="媒体库" subtitle="Jellyfin / EMBY 媒体管理" style="margin-bottom: 24px;">
      <template #extra>
        <n-button @click="load" size="small">🔄 刷新</n-button>
      </template>
    </n-page-header>

    <n-card :bordered="false" embedded style="margin-bottom: 16px;">
      <n-alert :type="status.connected ? 'success' : 'error'" :show-icon="false">
        {{ status.connected
          ? `${status.server_name} (v${status.version}) — 已连接 ✅`
          : '未连接 — 请在设置中配置 EMBY/Jellyfin 地址'
        }}
      </n-alert>
    </n-card>

    <n-card title="最近添加" :bordered="false" embedded>
      <n-empty v-if="items.length === 0" description="暂无媒体记录" />
      <n-grid v-else :cols="4" :x-gap="14" :y-gap="14" responsive="screen">
        <n-grid-item v-for="item in items" :key="item.id">
          <n-card :bordered="false" embedded hoverable>
            <n-space vertical>
              <n-image v-if="item.poster" :src="item.poster" object-fit="cover" style="width: 100%; height: 160px; border-radius: 8px;" />
              <n-text strong style="font-size: 13px;">{{ item.title }}</n-text>
              <n-tag size="small" round>{{ item.type }}</n-tag>
            </n-space>
          </n-card>
        </n-grid-item>
      </n-grid>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getLibraryStatus, getRecentMedia } from '../api'

const status = ref({ connected: false, server_name: '', version: '' })
const items = ref<any[]>([])

async function load() {
  try {
    const s = await getLibraryStatus()
    status.value = s as any
  } catch {}
  try {
    items.value = await getRecentMedia()
  } catch {}
}

onMounted(load)
</script>

<style scoped>
.library-page { max-width: 960px; }
</style>
