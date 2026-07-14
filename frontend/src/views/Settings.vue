<template>
  <div class="settings-page">
    <div class="page-header">
      <h2>设置</h2>
      <p>系统配置，所有配置实时保存，不填表示跳过对应功能</p>
    </div>

    <n-form
      :model="forms"
      label-placement="left"
      label-width="140"
      size="medium"
    >
      <!-- Downloaders -->
      <n-card :bordered="false" embedded style="margin-bottom: 16px;">
        <div style="font-size: 15px; font-weight: 600; margin-bottom: 16px;">📥 下载器</div>
        <n-grid :cols="2" :x-gap="16" :y-gap="12">
          <n-form-item label="qBittorrent URL" path="downloader.qbittorrent.url">
            <n-input v-model:value="forms.downloader.qbittorrent.url" placeholder="http://localhost:8080" />
          </n-form-item>
          <n-form-item label="用户名" path="downloader.qbittorrent.username">
            <n-input v-model:value="forms.downloader.qbittorrent.username" placeholder="admin" />
          </n-form-item>
          <n-form-item label="密码" path="downloader.qbittorrent.password">
            <n-input v-model:value="forms.downloader.qbittorrent.password" type="password" placeholder="••••••••" show-password-on="click" />
          </n-form-item>
          <n-form-item label="Referer" path="downloader.qbittorrent.referer">
            <n-input v-model:value="forms.downloader.qbittorrent.referer" placeholder="可选，部分站点需要" />
          </n-form-item>
        </n-grid>
      </n-card>

      <!-- Media Library -->
      <n-card :bordered="false" embedded style="margin-bottom: 16px;">
        <div style="font-size: 15px; font-weight: 600; margin-bottom: 16px;">📚 媒体库</div>
        <n-grid :cols="2" :x-gap="16" :y-gap="12">
          <n-form-item label="Jellyfin URL" path="media.jellyfin.url">
            <n-input v-model:value="forms.media.jellyfin.url" placeholder="http://localhost:8096" />
          </n-form-item>
          <n-form-item label="API Key" path="media.jellyfin.api_key">
            <n-input v-model:value="forms.media.jellyfin.api_key" placeholder="Jellyfin API Key" />
          </n-form-item>
          <n-form-item label="Emby URL" path="media.emby.url">
            <n-input v-model:value="forms.media.emby.url" placeholder="http://localhost:8096" />
          </n-form-item>
          <n-form-item label="API Key" path="media.emby.api_key">
            <n-input v-model:value="forms.media.emby.api_key" placeholder="Emby API Key" />
          </n-form-item>
        </n-grid>
      </n-card>

      <!-- Notifications -->
      <n-card :bordered="false" embedded style="margin-bottom: 16px;">
        <div style="font-size: 15px; font-weight: 600; margin-bottom: 16px;">🔔 通知</div>
        <n-grid :cols="2" :x-gap="16" :y-gap="12">
          <n-form-item label="Telegram Bot Token" path="notify.telegram.bot_token">
            <n-input v-model:value="forms.notify.telegram.bot_token" placeholder="123456:ABC-DEF" />
          </n-form-item>
          <n-form-item label="Chat ID" path="notify.telegram.chat_id">
            <n-input v-model:value="forms.notify.telegram.chat_id" placeholder="-1001234567890" />
          </n-form-item>
          <n-form-item label="Webhook URL" path="notify.webhook.url">
            <n-input v-model:value="forms.notify.webhook.url" placeholder="https://hooks.example.com/xxx" />
          </n-form-item>
          <n-form-item label="Webhook Secret" path="notify.webhook.secret">
            <n-input v-model:value="forms.notify.webhook.secret" type="password" placeholder="••••••••" />
          </n-form-item>
        </n-grid>
      </n-card>

      <!-- Proxy -->
      <n-card :bordered="false" embedded style="margin-bottom: 16px;">
        <div style="font-size: 15px; font-weight: 600; margin-bottom: 16px;">🌐 代理</div>
        <n-grid :cols="2" :x-gap="16" :y-gap="12">
          <n-form-item label="HTTP Proxy" path="proxy.http">
            <n-input v-model:value="forms.proxy.http" placeholder="http://127.0.0.1:7890" />
          </n-form-item>
          <n-form-item label="HTTPS Proxy" path="proxy.https">
            <n-input v-model:value="forms.proxy.https" placeholder="http://127.0.0.1:7890" />
          </n-form-item>
        </n-grid>
      </n-card>

      <!-- Safety -->
      <n-card :bordered="false" embedded style="margin-bottom: 16px;">
        <div style="font-size: 15px; font-weight: 600; margin-bottom: 16px;">🛡️ 安全限制</div>
        <n-grid :cols="2" :x-gap="16" :y-gap="12">
          <n-form-item label="最大文件大小 (GB)" path="safety.max_file_size">
            <n-input-number v-model:value="forms.safety.max_file_size" :min="1" :max="100" placeholder="10" />
          </n-form-item>
          <n-form-item label="最大线程数" path="safety.max_threads">
            <n-input-number v-model:value="forms.safety.max_threads" :min="1" :max="16" placeholder="4" />
          </n-form-item>
        </n-grid>
      </n-card>

      <!-- PT Sites -->
      <n-card :bordered="false" embedded style="margin-bottom: 16px;">
        <div style="font-size: 15px; font-weight: 600; margin-bottom: 16px;">🏷️ PT 站点认证</div>
        <n-alert type="info" style="margin-bottom: 16px; font-size: 13px;">
          每个站点的 Cookie 和 UA，留空表示跳过该站点
        </n-alert>
        <n-grid :cols="1" :x-gap="16" v-for="site in ptSites" :key="site.short">
          <n-card :bordered="false" embedded>
            <div style="font-size: 14px; font-weight: 600; margin-bottom: 12px; color: var(--text-primary);">
              {{ site.name }}
            </div>
            <n-grid :cols="2" :x-gap="16" :y-gap="12">
              <n-form-item label="Cookie">
                <n-input
                  :model-value="getPtValue(site.short, 'cookie')"
                  @update:model-value="setPtValue(site.short, 'cookie', $event)"
                  placeholder="站点 Cookie"
                  size="small"
                  type="textarea"
                  :autosize="{ minRows: 2, maxRows: 4 }"
                />
              </n-form-item>
              <n-form-item label="User-Agent">
                <n-input
                  :model-value="getPtValue(site.short, 'ua')"
                  @update:model-value="setPtValue(site.short, 'ua', $event)"
                  placeholder="User-Agent"
                  size="small"
                />
              </n-form-item>
            </n-grid>
          </n-card>
        </n-grid>
      </n-card>

      <!-- Save button -->
      <div style="text-align: right;">
        <n-button type="primary" @click="handleSave" :loading="saving">
          💾 保存配置
        </n-button>
      </div>
    </n-form>
  </div>
</template>

<script setup lang="ts">
import { reactive, onMounted, ref } from 'vue'
import { useMessage } from 'naive-ui'
import { api } from '@/api'

const message = useMessage()
const saving = ref(false)

interface PtSite {
  short: string
  name: string
}

const ptSites = ref<PtSite[]>([])

const forms = reactive({
  downloader: { qbittorrent: { url: '', username: '', password: '', referer: '' } },
  media: { jellyfin: { url: '', api_key: '' }, emby: { url: '', api_key: '' } },
  notify: { telegram: { bot_token: '', chat_id: '' }, webhook: { url: '', secret: '' } },
  proxy: { http: '', https: '' },
  safety: { max_file_size: 10, max_threads: 4 },
  pt: {} as Record<string, { cookie: string; ua: string }>,
})

function getPtValue(short: string, field: string) {
  return (forms.pt as any)[short]?.[field] ?? ''
}

function setPtValue(short: string, field: string, value: string) {
  if (!(forms.pt as any)[short]) {
    ;(forms.pt as any)[short] = { cookie: '', ua: '' }
  }
  ;(forms.pt as any)[short][field] = value
}

async function handleSave() {
  saving.value = true
  try {
    await api('/api/settings', { method: 'POST', body: forms })
    message.success('配置已保存')
  } catch (err: any) {
    message.error((err as Error).message || '保存失败')
  } finally {
    saving.value = false
  }
}

async function load() {
  try {
    const res = await api('/api/settings')
    const data = res
    if (data.downloader?.qbittorrent) Object.assign(forms.downloader.qbittorrent, data.downloader.qbittorrent)
    if (data.media) {
      if (data.media.jellyfin) Object.assign(forms.media.jellyfin, data.media.jellyfin)
      if (data.media.emby) Object.assign(forms.media.emby, data.media.emby)
    }
    if (data.notify) {
      if (data.notify.telegram) Object.assign(forms.notify.telegram, data.notify.telegram)
      if (data.notify.webhook) Object.assign(forms.notify.webhook, data.notify.webhook)
    }
    if (data.proxy) Object.assign(forms.proxy, data.proxy)
    if (data.safety) Object.assign(forms.safety, data.safety)
    if (data.pt) forms.pt = data.pt
  } catch (err) {
    console.error('Failed to load settings:', err)
  }
}

onMounted(load)
</script>
