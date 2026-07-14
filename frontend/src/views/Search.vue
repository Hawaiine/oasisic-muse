<template>
  <div class="search-page">
    <h1 class="page-title">🔍 搜索</h1>
    <div class="search-bar">
      <input v-model="keyword" placeholder="番号 / 演员名 / 关键词" class="input" @keyup.enter="doSearch" />
      <input v-model="actor" placeholder="演员（可选过滤）" class="input" />
      <button class="btn btn-primary" @click="doSearch" :disabled="loading">
        {{ loading ? '搜索中...' : '搜索' }}
      </button>
    </div>

    <div class="results" v-if="results.length > 0">
      <div v-for="r in results" :key="r.torrent_url" class="result-card">
        <div class="card-cover">
          <img v-if="r.cover" :src="r.cover" :alt="r.title" @error="r.cover = ''" />
          <div v-else class="cover-placeholder">🎬</div>
        </div>
        <div class="card-body">
          <div class="card-title">{{ r.title_cn || r.title }}</div>
          <div class="card-original" v-if="r.title_cn">{{ r.title }}</div>
          <div class="card-meta">
            <span class="site-badge">{{ r.site }}</span>
            <span v-if="r.size" class="meta-item">{{ r.size }}</span>
            <span class="meta-item">🟢 {{ r.seeders }}</span>
            <span v-if="r.movie_id" class="meta-item">#{{ r.movie_id }}</span>
          </div>
          <div class="card-actors" v-if="r.actors && r.actors.length">
            {{ r.actors.slice(0, 3).join(' / ') }}
          </div>
          <button class="btn btn-sm btn-primary" @click="download(r)" v-if="r.torrent_url">
            ⬇️ 下载种子
          </button>
        </div>
      </div>
    </div>

    <div v-else-if="searched" class="empty">
      <p>未找到结果</p>
      <p class="hint">试试其他关键词，或者检查 PT 站点 Cookie 是否已配置</p>
    </div>
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
.input::placeholder { color: #556; }
.btn { padding: 10px 18px; border-radius: 8px; border: none; cursor: pointer; font-size: 14px; }
.btn-primary { background: #1d9bf0; color: #fff; }
.btn-sm { padding: 6px 12px; font-size: 12px; }
.btn:disabled { opacity: 0.5; cursor: not-allowed; }

.results { display: grid; grid-template-columns: 1fr; gap: 12px; }
.result-card { display: flex; gap: 16px; padding: 16px; background: #1a1f2e; border-radius: 12px; }
.card-cover { width: 100px; min-height: 140px; flex-shrink: 0; border-radius: 8px; overflow: hidden; background: #0f1419; }
.card-cover img { width: 100%; height: 100%; object-fit: cover; }
.cover-placeholder { width: 100%; height: 140px; display: flex; align-items: center; justify-content: center; font-size: 32px; opacity: 0.3; }
.card-body { flex: 1; display: flex; flex-direction: column; gap: 6px; }
.card-title { font-size: 15px; font-weight: 600; color: #e1e8ed; line-height: 1.4; }
.card-original { font-size: 12px; color: #556; }
.card-meta { display: flex; gap: 10px; font-size: 12px; color: #8899a6; flex-wrap: wrap; }
.site-badge { padding: 2px 6px; border-radius: 4px; background: #2a3040; font-size: 11px; }
.meta-item { display: flex; align-items: center; gap: 2px; }
.card-actors { font-size: 12px; color: #1d9bf0; }
.empty { text-align: center; padding: 60px 20px; }
.empty p { font-size: 16px; color: #8899a6; }
.hint { font-size: 12px; color: #556; margin-top: 8px; }
</style>