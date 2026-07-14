<template>
  <div class="about-page">
    <n-page-header title="关于" subtitle="Oasisic Muse 系统信息" style="margin-bottom: 24px;" />

    <n-card :bordered="false" embedded style="margin-bottom: 16px;">
      <n-space vertical align="center">
        <span style="font-size: 48px;">🎵</span>
        <n-text depth="1" strong style="font-size: 20px;">{{ about.title }}</n-text>
        <n-text depth="3">{{ about.description }}</n-text>
        <n-tag type="info" round size="large">v{{ about.version }}</n-tag>
      </n-space>
    </n-card>

    <n-card title="⚠️ 免责声明" :bordered="false" embedded>
      <n-text>{{ about.disclaimer }}</n-text>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getAbout } from '../api'

const about = ref({ title: 'Oasisic Muse', description: '', disclaimer: '', version: '0.1.0' })

onMounted(async () => {
  try {
    about.value = await getAbout() as any
  } catch {}
})
</script>

<style scoped>
.about-page { max-width: 640px; }
</style>
