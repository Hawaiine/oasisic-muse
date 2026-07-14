<template>
  <div class="settings-page">
    <h1 class="page-title">设置</h1>

    <!-- PT 站点认证 -->
    <div class="section">
      <h3>🔐 PT 站点认证</h3>
      <p class="section-desc">填写各站点的 Cookie 和 Passkey，订阅引擎才能自动搜索下载</p>
      <div v-for="site in ptSites" :key="site.short" class="pt-site-card">
        <div class="site-header">
          <span class="site-name">{{ site.name }}</span>
          <span class="site-url">{{ site.url }}</span>
          <span class="site-badge" :class="site.cookie_configured ? 'on' : 'off'">
            {{ site.cookie_configured ? '✅ 已配置' : '❌ 未配置' }}
          </span>
        </div>
        <div class="site-fields">
          <div class="field">
            <label>Cookie</label>
            <input
              v-model="siteForms[site.short].cookie"
              type="password"
              placeholder="粘贴 Cookie（可选）"
              class="input"
            />
          </div>
          <div class="field" v-if="site.auth_type.includes('passkey')">
            <label>Passkey</label>
            <input
              v-model="siteForms[site.short].passkey"
              type="password"
              placeholder="粘贴 Passkey（可选）"
              class="input"
            />
          </div>
        </div>
      </div>
      <button class="btn btn-primary" @click="savePTSites">保存 PT 配置</button>
    </div>

    <!-- 下载器 -->
    <div class="section">
      <h3>⬇️ 下载器</h3>
      <div class="field-row">
        <div class="field">
          <label>qBittorrent 地址</label>
          <div class="value">{{ info.qb_host }}</div>
        </div>
        <div class="field">
          <label>端口</label>
          <div class="value">{{ info.qb_port }}</div>
        </div>
      </div>
    </div>

    <!-- 通知 -->
    <div class="section">
      <h3>🔔 通知</h3>
      <div class="field">
        <label>Telegram</label>
        <div class="value">{{ info.tg_bot_token }}</div>
      </div>
      <div class="field">
        <label>Discord</label>
        <div class="value">{{ info.discord_webhook }}</div>
      </div>
      <button class="btn btn-primary btn-sm" @click="testNotify">发送测试通知</button>
    </div>

    <!-- 媒体库 -->
    <div class="section">
      <h3>🎬 媒体库</h3>
      <div class="field">
        <label>EMBY/Jellyfin 地址</label>
        <div class="value">{{ info.emby_host || '未配置' }}</div>
      </div>
    </div>

    <!-- 代理 -->
    <div class="section">
      <h3>🌐 代理</h3>
      <div class="field">
        <label>代理地址</label>
        <div class="value">{{ info.proxy_url || '未配置' }}</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { getSettings, savePTSites as savePTSitesApi, testNotify as testNotifyApi, getPTSitesConfig } from '../api'

const info = ref<any>({})
const ptSites = ref<any[]>([])
const siteForms = reactive<Record<string, { cookie: string; passkey: string }>>({})

async function savePTSites() {
  const sites: Record<string, { cookie?: string; passkey?: string }> = {}
  for (const [short, form] of Object.entries(siteForms)) {
    const data: { cookie?: string; passkey?: string } = {}
    if (form.cookie) data.cookie = form.cookie
    if (form.passkey) data.passkey = form.passkey
    if (Object.keys(data).length > 0) {
      sites[short] = data
    }
  }
  await savePTSitesApi(sites)
  alert('✅ PT 站点配置已保存')
  // 清空表单
  for (const key of Object.keys(siteForms)) {
    siteForms[key] = { cookie: '', passkey: '' }
  }
  await load()
}

async function testNotify() {
  await testNotifyApi()
  alert('测试通知已发送，请检查 Telegram / Discord')
}

async function load() {
  const [s, pt] = await Promise.all([
    getSettings(),
    getPTSitesConfig().catch(() => ({})),
  ])
  info.value = s as any
  ptSites.value = (s as any).pt_sites || []

  for (const site of ptSites.value) {
    if (!siteForms[site.short]) {
      siteForms[site.short] = { cookie: '', passkey: '' }
    }
  }
}

onMounted(load)
</script>

<style scoped>
.settings-page { max-width: 700px; }
.page-title { font-size: 24px; margin-bottom: 20px; color: #e1e8ed; }
.section { background: #1a1f2e; border-radius: 12px; padding: 20px; margin-bottom: 16px; }
.section h3 { font-size: 16px; margin-bottom: 8px; color: #e1e8ed; }
.section-desc { font-size: 12px; color: #8899a6; margin-bottom: 16px; }
.field { margin-bottom: 12px; }
.field label { display: block; font-size: 13px; color: #8899a6; margin-bottom: 4px; }
.field .value { font-size: 14px; color: #e1e8ed; padding: 8px 0; }
.field-row { display: flex; gap: 16px; }
.field-row .field { flex: 1; }

.pt-site-card { background: #0f1419; border-radius: 10px; padding: 16px; margin-bottom: 12px; }
.site-header { display: flex; align-items: center; gap: 10px; margin-bottom: 12px; flex-wrap: wrap; }
.site-name { font-size: 14px; font-weight: 600; color: #e1e8ed; }
.site-url { font-size: 12px; color: #556; }
.site-badge { font-size: 11px; padding: 2px 8px; border-radius: 10px; }
.site-badge.on { background: #00ba7c20; color: #00ba7c; }
.site-badge.off { background: #2a3040; color: #8899a6; }
.site-fields { display: flex; flex-direction: column; gap: 8px; }

.input { width: 100%; padding: 10px 14px; border-radius: 8px; border: 1px solid #2a3040; background: #1a1f2e; color: #e1e8ed; font-size: 14px; }
.input::placeholder { color: #556; }
.btn { padding: 10px 18px; border-radius: 8px; border: none; cursor: pointer; font-size: 14px; }
.btn-primary { background: #1d9bf0; color: #fff; }
.btn-sm { padding: 8px 16px; font-size: 13px; margin-top: 10px; }
</style>