<template>
  <div class="settings-page">
    <n-page-header title="设置" subtitle="系统配置，所有配置实时保存，不填表示跳过对应功能">
      <template #extra>
        <n-tag type="success" round>已保存</n-tag>
      </template>
    </n-page-header>

    <n-grid :cols="2" :x-gap="16" :y-gap="16" responsive="screen">
      <!-- PT 站点认证 -->
      <n-grid-item span="2">
        <n-card title="🔐 PT 站点认证" :bordered="false" embedded>
          <n-alert type="info" :show-icon="false" style="margin-bottom: 16px;">
            Cookie / Passkey 用于搜索和下载，不填则跳过该站点
          </n-alert>
          <n-form inline label-placement="left" :model="forms.pt" label-width="80">
            <n-grid :cols="2" :x-gap="16" :y-gap="12" responsive="screen">
              <n-grid-item v-for="site in ptSites" :key="site.short">
                <n-form-item :label="site.name">
                  <n-input v-model:value="(forms.pt as any)[site.short].cookie" placeholder="Cookie (选填)" size="small" />
                  <n-input v-if="site.auth_type.includes('passkey')" v-model:value="(forms.pt as any)[site.short].passkey" placeholder="Passkey (选填)" size="small" style="margin-top: 4px;" />
                </n-form-item>
              </n-grid-item>
            </n-grid>
          </n-form>
        </n-card>
      </n-grid-item>

      <!-- 下载器 -->
      <n-grid-item>
        <n-card title="⬇️ 下载器 (qBittorrent)" :bordered="false" embedded>
          <n-alert type="info" :show-icon="false" style="margin-bottom: 16px;">
            Web UI 连接信息，不填则跳过自动下载
          </n-alert>
          <n-form inline label-placement="left" :model="forms.qb" label-width="60">
            <n-form-item label="地址">
              <n-input v-model:value="forms.qb.host" placeholder="192.168.1.100" size="small" />
            </n-form-item>
            <n-form-item label="端口">
              <n-input-number v-model:value="forms.qb.port" placeholder="8080" size="small" />
            </n-form-item>
            <n-form-item label="用户名">
              <n-input v-model:value="forms.qb.username" placeholder="admin" size="small" />
            </n-form-item>
            <n-form-item label="密码">
              <n-input v-model:value="forms.qb.password" type="password" placeholder="选填" size="small" />
            </n-form-item>
          </n-form>
        </n-card>
      </n-grid-item>

      <!-- 媒体库 -->
      <n-grid-item>
        <n-card title="🎬 媒体库 (Jellyfin/EMBY)" :bordered="false" embedded>
          <n-alert type="info" :show-icon="false" style="margin-bottom: 16px;">
            下载完成后自动入库，不填则跳过
          </n-alert>
          <n-form inline label-placement="left" :model="forms.emby" label-width="60">
            <n-form-item label="地址">
              <n-input v-model:value="forms.emby.host" placeholder="http://192.168.1.100:8096" size="small" />
            </n-form-item>
            <n-form-item label="API密钥">
              <n-input v-model:value="forms.emby.api_key" type="password" placeholder="选填" size="small" />
            </n-form-item>
          </n-form>
        </n-card>
      </n-grid-item>

      <!-- Telegram -->
      <n-grid-item>
        <n-card title="🔔 Telegram 通知" :bordered="false" embedded>
          <n-alert type="info" :show-icon="false" style="margin-bottom: 16px;">
            任务完成通知推送，不填则不推送
          </n-alert>
          <n-form inline label-placement="left" :model="forms.telegram" label-width="60">
            <n-form-item label="Token">
              <n-input v-model:value="forms.telegram.bot_token" placeholder="Bot Token" size="small" />
            </n-form-item>
            <n-form-item label="Chat ID">
              <n-input v-model:value="forms.telegram.chat_id" placeholder="-100xxxxxxxx" size="small" />
            </n-form-item>
          </n-form>
        </n-card>
      </n-grid-item>

      <!-- Discord -->
      <n-grid-item>
        <n-card title="💬 Discord 通知" :bordered="false" embedded>
          <n-alert type="info" :show-icon="false" style="margin-bottom: 16px;">
            Webhook URL，不填则不推送
          </n-alert>
          <n-form inline label-placement="left" :model="forms.discord" label-width="60">
            <n-form-item label="Webhook">
              <n-input v-model:value="forms.discord.webhook_url" placeholder="https://discord.com/api/..." size="small" />
            </n-form-item>
          </n-form>
        </n-card>
      </n-grid-item>

      <!-- 代理 -->
      <n-grid-item>
        <n-card title="🌐 代理设置" :bordered="false" embedded>
          <n-alert type="info" :show-icon="false" style="margin-bottom: 16px;">
            AV 刮削 / PT 搜索使用代理，国内环境可不填
          </n-alert>
          <n-form inline label-placement="left" :model="forms.proxy" label-width="60">
            <n-form-item label="地址">
              <n-input v-model:value="forms.proxy.http_proxy" placeholder="http://127.0.0.1:7890" size="small" />
            </n-form-item>
          </n-form>
        </n-card>
      </n-grid-item>

      <!-- 安全限制 -->
      <n-grid-item span="2">
        <n-card title="🛡️ 安全限制" :bordered="false" embedded>
          <n-alert type="info" :show-icon="false" style="margin-bottom: 16px;">
            控制下载频率和资源消耗
          </n-alert>
          <n-form inline label-placement="horizontal" :model="forms.limits" label-width="100">
            <n-form-item label="每日上限">
              <n-input-number v-model:value="forms.limits.daily_limit" :min="1" :max="999" size="small" />
            </n-form-item>
            <n-form-item label="并发数">
              <n-input-number v-model:value="forms.limits.concurrent" :min="1" :max="10" size="small" />
            </n-form-item>
            <n-form-item label="磁盘阈值">
              <n-input-number v-model:value="forms.limits.disk_threshold" :min="1" :max="100" size="small">%</n-input-number>
            </n-form-item>
            <n-form-item label="文件大小">
              <n-input-number v-model:value="forms.limits.max_file_size" :min="1" size="small">MB</n-input-number>
            </n-form-item>
            <n-form-item label="做种数">
              <n-input-number v-model:value="forms.limits.max_seeds" :min="1" :max="50" size="small" />
            </n-form-item>
          </n-form>
        </n-card>
      </n-grid-item>
    </n-grid>
  </div>
</template>

<script setup lang="ts">
import { reactive, onMounted } from 'vue'
import { getSettings, saveAllSettings, updateLimits } from '../api'

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
  } catch {}
}

onMounted(load)
</script>

<style scoped>
.settings-page { max-width: 960px; }
</style>
