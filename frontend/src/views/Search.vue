<template>
  <div class="search-page">
    <div class="page-header">
      <h2>PT 搜索</h2>
      <p>在 PT 站点搜索资源</p>
    </div>

    <div class="card" style="margin-bottom: 16px;">
      <div style="display: flex; gap: 8px;">
        <n-input
          v-model:value="keyword"
          placeholder="搜索关键词..."
          size="medium"
          @keydown.enter="doSearch"
          style="flex: 1;"
        />
        <n-select
          v-model:value="selectedSite"
          :options="siteOptions"
          placeholder="站点"
          size="medium"
          clearable
          style="width: 200px;"
        />
        <button class="btn btn-primary" @click="doSearch">🔎 搜索</button>
      </div>
    </div>

    <div class="card">
      <table v-if="results.length > 0">
        <thead>
          <tr>
            <th>名称</th>
            <th>站点</th>
            <th>大小</th>
            <th>种子</th>
            <th>做种</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="r in results" :key="r.title">
            <td style="color: var(--text-primary);">{{ r.title }}</td>
            <td><span class="badge badge-muted">{{ r.site }}</span></td>
            <td>{{ r.size }}</td>
            <td>{{ r.seeders }}</td>
            <td>{{ r.leechers }}</td>
            <td>
              <button class="btn btn-sm" @click="downloadTorrent(r)">📥 下载</button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else class="empty-state">
        <div class="empty-state-icon">🔎</div>
        <div class="empty-state-text">输入关键词开始搜索</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { NSelect } from 'naive-ui'
import { api } from '@/api'

const keyword = ref('')
const selectedSite = ref('')
const results = ref<any[]>([])
const siteOptions = ref<any[]>([])

async function loadSites() {
  try {
    const res = await api.get('/api/sites')
    siteOptions.value = (res.data || []).map((s: any) => ({
      label: s.name,
      value: s.short,
    }))
  } catch {
    // ignore
  }
}

async function doSearch() {
  if (!keyword.value) return
  try {
    const params: any = { q: keyword.value }
    if (selectedSite.value) params.site = selectedSite.value
    const res = await api.get('/api/search', { params })
    results.value = res.data || []
  } catch (e) {
    console.error(e)
    results.value = []
  }
}

async function downloadTorrent(item: any) {
  try {
    await api.post('/api/download', { url: item.download_url })
  } catch (e) {
    console.error(e)
  }
}

onMounted(loadSites)
</script>
