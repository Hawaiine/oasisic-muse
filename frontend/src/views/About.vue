<template>
  <div class="about-page">
    <div class="page-header">
      <h2>关于</h2>
      <p>Oasisic Muse 系统信息</p>
    </div>

    <div class="card" style="margin-bottom: 16px;">
      <div style="font-size: 15px; font-weight: 600; margin-bottom: 12px;">系统信息</div>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; font-size: 14px;">
        <div><span style="color: var(--text-muted);">版本：</span>{{ info.version || 'v0.1.0' }}</div>
        <div><span style="color: var(--text-muted);">构建时间：</span>{{ info.buildDate || '-' }}</div>
        <div><span style="color: var(--text-muted);">Python：</span>{{ info.python || '-' }}</div>
        <div><span style="color: var(--text-muted);">Node：</span>{{ info.node || '-' }}</div>
      </div>
    </div>

    <div class="card">
      <div style="font-size: 15px; font-weight: 600; margin-bottom: 12px;">免责声明</div>
      <div style="font-size: 13px; color: var(--text-secondary); line-height: 1.6;">
        <p>本项目仅供学习交流使用，不得用于商业用途。</p>
        <p style="margin-top: 8px;">下载和搜索功能仅支持用户自行授权的 PT 站点，请勿用于非法用途。</p>
        <p style="margin-top: 8px;">使用本软件产生的所有法律责任由使用者自行承担。</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { api } from '@/api'

const info = ref<any>({})

onMounted(async () => {
  try {
    const res = await api('/api/about')
    info.value = res || {}
  } catch {
    // ignore
  }
})
</script>
