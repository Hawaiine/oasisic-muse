<template>
  <div class="search-page">
    <h1 class="page-title">PT 搜索</h1>
    <div class="search-bar">
      <input v-model="keyword" placeholder="番号 / 关键词" class="input" @keyup.enter="doSearch" />
      <input v-model="actor" placeholder="演员（可选）" class="input" />
      <button class="btn btn-primary" @click="doSearch" :disabled="loading">
        {{ loading ? '搜索中...' : '搜索' }}
      </button>
    </div>
    <div class="results" v-if="results.length > 0">
      <div v-for="r in results" :key="r.torrent_url" class="result-item">
        <div class="result-info">
          <div class="result-title">{{ r.title }}</div>
          <div class="result-meta">
            <span class="site-badge">{{ r.site }}</span>
            <span v-if="r.size" class="size">{{ r.size }}</span>
            <span class="seeders">🟢 {{ r.seeders }}</span>
          </div>
        </div>
        <div class="result-actions">
          <button class="btn btn-sm btn-primary" @click="download(r)">下载</button>
        </div>
      </div>
    </div>
    <div v-else-if="searched" class="empty">未找到结果</div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { searchPT } from '../api'

const keyword = ref('')
const actor = ref('')
const results = ref<any[]>([])
const loading = ref(false)
const searched = ref(false)

async function doSearch() {
  if (!keyword.value.trim()) return
  loading.value = true
  searched.value = true
  try {
    const res = await searchPT(keyword.value.trim(), actor.value.trim())
    results.value = (res as any).items || []
  } catch {
    results.value = []
  } finally {
    loading.value = false
  }
}

function download(r: any) {
  if (r.torrent_url) {
    window.open(r.torrent_url, '_blank')
  }
}
</script>

<style scoped>
.search-page { max-width: 800px; }
.page-title { font-size: 24px; margin-bottom: 20px; color: #e1e8ed; }
.search-bar { display: flex; gap: 8px; margin-bottom: 20px; flex-wrap: wrap; }
.input { flex: 1; min-width: 150px; padding: 10px 14px; border-radius: 8px; border: 1px solid #2a3040; background: #1a1f2e; color: #e1e8ed; font-size: 14px; }
.btn { padding: 10px 18px; border-radius: 8px; border: none; cursor: pointer; font-size: 14px; }
.btn-primary { background: #1d9bf0; color: #fff; }
.btn-sm { padding: 6px 12px; font-size: 12px; }
.btn:disabled { opacity: 0.5; cursor: not-allowed; }
.results { display: flex; flex-direction: column; gap: 8px; }
.result-item { display: flex; justify-content: space-between; align-items: center; padding: 14px 16px; background: #1a1f2e; border-radius: 10px; }
.result-title { font-size: 14px; color: #e1e8ed; margin-bottom: 6px; }
.result-meta { display: flex; gap: 10px; font-size: 12px; color: #8899a6; align-items: center; }
.site-badge { padding: 2px 6px; border-radius: 4px; background: #2a3040; font-size: 11px; }
.empty { text-align: center; padding: 40px; color: #556; font-size: 14px; }
</style>