<template>
  <div class="settings-page">
    <n-page-header title="设置" subtitle="系统配置，所有配置实时保存，不填表示跳过对应功能" style="margin-bottom: 24px;">
      <template #extra>
        <n-button type="primary" @click="save" :loading="saving">
          💾 保存设置
        </n-button>
      </template>
    </n-page-header>

    <n-grid :cols="2" :x-gap="16" :y-gap="16" responsive="screen">
      <!-- PT 站点认证 -->
      <n-grid-item span="2">
        <n-card :bordered="false" embedded>
          <template #header>
            <n-space>
              <span style="font-size: 16px;">🔐</span>
              <n-text strong>PT 站点认证</n-text>
            </n-space>
          </template>
          <n-alert type="info" :show-icon="false" style="margin-bottom: 16px;">
            Cookie / Passkey 用于搜索和下载，不填则跳过该站点
          </n-alert>
          <n-grid :cols="2" :x-gap="16" :y-gap="12" responsive="screen">
            <n-grid-item v-for="site in ptSites" :key="site.short">
              <n-card :bordered="false" embedded>
                <n-text strong style="font-size: 13px;">{{ site.name }}</n-text>
                <n-space vertical style="margin-top: 8px;">
                  <n-input :model-value="getPtValue(site.short, 'cookie')" @update:model-value="setPtValue(site.short, 'cookie', $event)" placeholder="Cookie" size="small" />
                  <n-input v-if="site.auth_type.includes('passkey')" :model-value="getPtValue(site.short, 'passkey')" @update:model-value="setPtValue(site.short, 'passkey', $event)" placeholder="Passkey" size="small" />
                </n-space>
              </n-card>
            </n-grid-item>
          </n-grid>
        </n-card>
      </n-grid-item>

      <!-- 下载器 -->
      <n-grid-item>
        <n-card :bordered="false" embedded>
          <template #header>
            <n-space>
              <span>⬇️</span>
              <n-text strong>下载器 (qBittorrent)</n-text>
            </n-space>
          </template>
          <n-alert type="info" :show-icon="false" style="margin-bottom: 16px;">
            Web UI 连接信息
          </n-alert>
          <n-space vertical>
            <n-input v-model:value="forms.qb.host" placeholder="主机地址 (如 192.168.1.100)" size="small" />
            <n-input-number v-model:value="forms.qb.port" placeholder="端口 (如 8080)" size="small" style="width: 100%;" />
            <n-input v-model:value="forms.qb.username" placeholder="用户名" size="small" />
            <n-input v-model:value="forms.qb.password" type="password" placeholder="密码" size="small" />
          </n-space>
        </n-card>
      </n-grid-item>

      <!-- 媒体库 -->
      <n-grid-item>
        <n-card :bordered="false" embedded>
          <template #header>
            <n-space>
              <span>🎬</span>
              <n-text strong>媒体库 (Jellyfin/EMBY)</n-text>
            </n-space>
          </template>
          <n-alert type="info" :show-icon="false" style="margin-bottom: 16px;">
            下载完成后自动入库
          </n-alert>
          <n-space vertical>
            <n-input v-model:value="forms.emby.host" placeholder="http://192.168.1.100:8096" size="small" />
            <n-input v-model:value="forms.emby.api_key" type="password" placeholder="API 密钥" size="small" />
          </n-space>
        </n-card>
      </n-grid-item>

      <!-- Telegram -->
      <n-grid-item>
        <n-card :bordered="false" embedded>
          <template #header>
            <n-space>
              <span>🔔</span>
              <n-text strong>Telegram 通知</n-text>
            </n-space>
          </template>
          <n-alert type="info" :show-icon="false" style="margin-bottom: 16px;">
            任务完成通知推送
          </n-alert>
          <n-space vertical>
            <n-input v-model:value="forms.telegram.bot_token" placeholder="Bot Token" size="small" />
            <n-input v-model:value="forms.telegram.chat_id" placeholder="-100xxxxxxxx" size="small" />
          </n-space>
        </n-card>
      </n-grid-item>

      <!-- Discord -->
      <n-grid-item>
        <n-card :bordered="false" embedded>
          <template #header>
            <n-space>
              <span>💬</span>
              <n-text strong>Discord 通知</n-text>
            </n-space>
          </template>
          <n-alert type="info" :show-icon="false" style="margin-bottom: 16px;">
            Webhook URL
          </n-alert>
          <n-input v-model:value="forms.discord.webhook_url" placeholder="https://discord.com/api/..." size="small" />
        </n-card>
      </n-grid-item>

      <!-- 代理 -->
      <n-grid-item>
        <n-card :bordered="false" embedded>
          <template #header>
            <n-space>
              <span>🌐</span>
              <n-text strong>代理设置</n-text>
            </n-space>
          </template>
          <n-alert type="info" :show-icon="false" style="margin-bottom: 16px;">
            AV 刮削 / PT 搜索使用代理
          </n-alert>
          <n-input v-model:value="forms.proxy.http_proxy" placeholder="http://127.0.0.1:7890" size="small" />
        </n-card>
      </n-grid-item>

      <!-- 安全限制 -->
      <n-grid-item span="2">
        <n-card :bordered="false" embedded>
          <template #header>
            <n-space>
              <span>🛡️</span>
              <n-text strong>安全限制</n-text>
            </n-space>
          </template>
          <n-alert type="info" :show-icon="false" style="margin-bottom: 16px;">
            控制下载频率和资源消耗
          </n-alert>
          <n-grid :cols="3" :x-gap="16" :y-gap="12" responsive="screen">
            <n-grid-item>
              <n-input-number v-model:value="forms.limits.daily_limit" :min="1" :max="999" placeholder="每日上限" size="small" style="width: 100%;" />
            </n-grid-item>
            <n-grid-item>
              <n-input-number v-model:value="forms.limits.concurrent" :min="1" :max="10" placeholder="并发数" size="small" style="width: 100%;" />
            </n-grid-item>
            <n-grid-item>
              <n-input-number v-model:value="forms.limits.disk_threshold" :min="1" :max="100" placeholder="磁盘阈值 %" size="small" style="width: 100%;" />
            </n-grid-item>
            <n-grid-item>
              <n-input-number v-model:value="forms.limits.max_file_size" :min="1" placeholder="最大文件 MB" size="small" style="width: 100%;" />
            </n-grid-item>
            <n-grid-item>
              <n-input-number v-model:value="forms.limits.max_seeds" :min="1" :max="50" placeholder="最大做种数" size="small" style="width: 100%;" />
            </n-grid-item>
          </n-grid>
        </n-card>
      </n-grid-item>
    </n-grid>
  </div>
</template>

<script setup lang="ts">
import { reactive, onMounted, ref } from 'vue'
import { useMessage } from 'naive-ui'
import { getSettings, saveAllSettings } from '../api'

const message = useMessage()
const saving = ref(false)

const ptSites = [
  { short: 'mteam', name: 'MTeam', url: 'https://mt2.cc', auth_type: ['cookie'] },
  { short: 'nicept', name: 'NicePT', url: 'https://nicept.org', auth_type: ['cookie'] },
  { short: 'pttime', name: 'PT时间', url: 'https://pttime.org', auth_type: ['cookie'] },
  { short: 'rousi', name: '肉丝', url: 'https://rousi.in', auth_type: ['cookie', 'passkey'] },
]

const forms = reactive({
  pt: {} as Record<string, { cookie?: string; passkey?: string }>,
  qb: { host: '', port: 8080, username: '', password: '' },
  emby: { host: '', api_key: '' },
  telegram: { bot_token: '', chat_id: '' },
  discord: { webhook_url: '' },
  proxy: { http_proxy: '' },
  limits: {
    daily_limit: 10,
    concurrent: 3,
    disk_threshold: 90,
    max_file_size: 10000,
    max_seeds: 10,
  },
})

function getPtValue(short: string, field: string) {
  return (forms.pt as any)[short]?.[field] ?? ''
}

function setPtValue(short: string, field: string, value: string) {
  if (!(forms.pt as any)[short]) (forms.pt as any)[short] = {}
  ;(forms.pt as any)[short][field] = value
}

async function load() {
  try {
    const settings = await getSettings()
    const s = settings as any
    if (s.pt) Object.assign(forms.pt, s.pt)
    if (s.qb) Object.assign(forms.qb, s.qb)
    if (s.emby) Object.assign(forms.emby, s.emby)
    if (s.telegram) Object.assign(forms.telegram, s.telegram)
    if (s.discord) Object.assign(forms.discord, s.discord)
    if (s.proxy) Object.assign(forms.proxy, s.proxy)
    if (s.limits) Object.assign(forms.limits, s.limits)
  } catch {}
}

async function save() {
  saving.value = true
  try {
    await saveAllSettings({
      pt: JSON.stringify(forms.pt),
      qb_host: forms.qb.host,
      qb_port: String(forms.qb.port),
      qb_username: forms.qb.username,
      qb_password: forms.qb.password,
      emby_host: forms.emby.host,
      emby_api_key: forms.emby.api_key,
      telegram_bot_token: forms.telegram.bot_token,
      telegram_chat_id: forms.telegram.chat_id,
      discord_webhook_url: forms.discord.webhook_url,
      http_proxy: forms.proxy.http_proxy,
      daily_limit: String(forms.limits.daily_limit),
      concurrent: String(forms.limits.concurrent),
      disk_threshold: String(forms.limits.disk_threshold),
      max_file_size: String(forms.limits.max_file_size),
      max_seeds: String(forms.limits.max_seeds),
    })
    message.success('设置已保存')
  } catch {
    message.error('保存失败')
  } finally {
    saving.value = false
  }
}

onMounted(load)
</script>

<style scoped>
.settings-page { max-width: 960px; }
</style>
