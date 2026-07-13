<template>
  <div class="settings-page">
    <h1 class="page-title">设置</h1>
    <div class="section">
      <h3>下载器</h3>
      <div class="field">
        <label>qBittorrent 地址</label>
        <div class="value">{{ settings.qb_host || '未配置' }}</div>
      </div>
      <div class="field">
        <label>端口</label>
        <div class="value">{{ settings.qb_port }}</div>
      </div>
    </div>
    <div class="section">
      <h3>通知</h3>
      <div class="field">
        <label>Telegram</label>
        <div class="value">{{ settings.tg_bot_token }}</div>
      </div>
      <div class="field">
        <label>Discord</label>
        <div class="value">{{ settings.discord_webhook }}</div>
      </div>
      <button class="btn btn-primary" @click="testNotify">发送测试通知</button>
    </div>
    <div class="section">
      <h3>媒体库</h3>
      <div class="field">
        <label>EMBY 地址</label>
        <div class="value">{{ settings.emby_host || '未配置' }}</div>
      </div>
    </div>
    <div class="section">
      <h3>代理</h3>
      <div class="field">
        <label>代理地址</label>
        <div class="value">{{ settings.proxy_url || '未配置' }}</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getSettings, testNotify as testNotifyApi } from '../api'

const settings = ref<any>({})

async function testNotify() {
  await testNotifyApi()
  alert('测试通知已发送，请检查 Telegram/Discord')
}

onMounted(async () => {
  try {
    settings.value = await getSettings()
  } catch {}
})
</script>

<style scoped>
.settings-page { max-width: 600px; }
.page-title { font-size: 24px; margin-bottom: 20px; color: #e1e8ed; }
.section { background: #1a1f2e; border-radius: 12px; padding: 20px; margin-bottom: 16px; }
.section h3 { font-size: 16px; margin-bottom: 12px; color: #e1e8ed; }
.field { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #2a3040; }
.field label { font-size: 14px; color: #8899a6; }
.field .value { font-size: 14px; color: #e1e8ed; }
.btn { padding: 10px 18px; border-radius: 8px; border: none; cursor: pointer; font-size: 14px; margin-top: 12px; }
.btn-primary { background: #1d9bf0; color: #fff; }
</style>