<template>
  <div class="about-page">
    <div class="about-card">
      <div class="about-icon">🎵</div>
      <h1 class="about-title">{{ about.title }}</h1>
      <p class="about-desc">{{ about.description }}</p>
      <div class="divider"></div>
      <div class="disclaimer">
        <h3>⚠️ 免责声明</h3>
        <p>{{ about.disclaimer }}</p>
      </div>
      <div class="version">v{{ about.version }}</div>
    </div>
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
.about-page { display: flex; justify-content: center; padding-top: 40px; }
.about-card { max-width: 500px; width: 100%; background: #1a1f2e; border-radius: 16px; padding: 40px; text-align: center; }
.about-icon { font-size: 48px; margin-bottom: 16px; }
.about-title { font-size: 24px; color: #e1e8ed; margin-bottom: 8px; }
.about-desc { font-size: 14px; color: #8899a6; margin-bottom: 24px; }
.divider { height: 1px; background: #2a3040; margin: 20px 0; }
.disclaimer { text-align: left; }
.disclaimer h3 { font-size: 15px; color: #ffd400; margin-bottom: 12px; }
.disclaimer p { font-size: 13px; color: #8899a6; line-height: 1.8; }
.version { margin-top: 24px; font-size: 12px; color: #556; }
</style>