<template>
  <div class="search-page">
    <n-page-header title="搜索" subtitle="PT 站点资源搜索" style="margin-bottom: 24px;">
      <template #extra>
        <n-button @click="loadSites" size="small">🔄 刷新站点</n-button>
      </template>
    </n-page-header>

    <n-card :bordered="false" embedded style="margin-bottom: 16px;">
      <n-form inline :model="searchForm" @submit.prevent="doSearch">
        <n-form-item label="番号">
          <n-input v-model:value="searchForm.keyword" placeholder="番号 / 演员名 / 关键词" @keyup.enter="doSearch" style="width: 240px;" />
        </n-form-item>
        <n-form-item label="演员">
          <n-input v-model:value="searchForm.actor" placeholder="可选过滤" style="width: 160px;" />
        </n-form-item>
        <n-form-item>
          <n-button type="primary" html-type="submit" :loading="loading">
            {{ loading ? '搜索中...' : '🔍 搜索' }}
          </n-button>
        </n-form-item>
      </n-form>
    </n-card>

    <n-alert v-if="errorMsg" type="error" :show-icon="false" style="margin-bottom: 16px;">
      {{ errorMsg }}
    </n-alert>

    <n-grid :cols="3" :x-gap="16" :y-gap="16" responsive="screen">
      <n-grid-item v-for="r in results" :key="r.torrent_url">
        <n-card :bordered="false" embedded hoverable>
          <n-space vertical>
            <n-image v-if="r.cover" :src="r.cover" object-fit="cover" style="width: 100%; height: 180px; border-radius: 8px;" />
            <div v-else style="width: 100%; height: 180px; background: #161b22; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 40px;">🎬</div>
            <n-text strong>{{ r.title_cn || r.title }}</n-text>
            <n-text depth="3" v-if="r.title_cn" style="font-size: 12px;">{{ r.title }}</n-text>
            <n-space>
              <n-tag size="small" round>{{ r.site }}</n-tag>
              <n-tag v-if="r.size" size="small" round>{{ r.size }}</n-tag>
              <n-tag size="small" round type="success">🟢 {{ r.seeders }}</n-tag>
            </n-space>
            <n-text depth="3" v-if="r.actors && r.actors.length" style="font-size: 12px;">
              {{ r.actors.slice(0, 3).join(' / ') }}
            </n-text>
          </n-space>
        </n-card>
      </n-grid-item>
    </n-grid>

    <n-empty v-if="results.length === 0 && !loading && !errorMsg" description="输入番号搜索资源" style="margin-top: 40px;" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { searchPT, getPTSitesConfig } from '../api'

const searchForm = ref({ keyword: '', actor: '' })
const results = ref<any[]>([])
const loading = ref(false)
const errorMsg = ref('')
const sites = ref<any[]>([])

async function loadSites() {
  try {
    sites.value = await getPTSitesConfig()
  } catch {}
}

async function doSearch() {
  if (!searchForm.value.keyword.trim()) return
  loading.value = true
  errorMsg.value = ''
  try {
    results.value = await searchPT(searchForm.value.keyword, searchForm.value.actor)
  } catch (e: any) {
    errorMsg.value = e.message || '搜索失败'
  } finally {
    loading.value = false
  }
}

onMounted(loadSites)
</script>

<style scoped>
.search-page { max-width: 960px; }
</style>
