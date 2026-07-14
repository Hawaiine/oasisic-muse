<template>
  <div class="settings-page">
    <h1 class="page-title">设置</h1>

    <!-- ===== PT 站点认证 ===== -->
    <div class="section">
      <h3>🔐 PT 站点认证</h3>
      <p class="section-desc">Cookie / Passkey 用于搜索和下载，不填则跳过该站点</p>
      <div v-for="site in ptSites" :key="site.short" class="card">
        <div class="card-header">
          <span class="card-name">{{ site.name }}</span>
          <span class="card-url">{{ site.url }}</span>
          <span class="badge" :class="site.cookie_configured ? 'on' : 'off'">
            {{ site.cookie_configured ? '已配置' : '未配置' }}
          </span>
        </div>
        <div class="card-body">
          <label>Cookie</label>
          <input v-model="forms.pt[site.short].cookie" type="password" placeholder="选填" class="input" />
          <label v-if="site.auth_type.includes('passkey')">Passkey</label>
          <input v-if="site.auth_type.includes('passkey')" v-model="forms.pt[site.short].passkey" type="password" placeholder="选填" class="input" />
        </div>
      </div>
      <button class="btn btn-primary" @click="savePT">保存 PT 配置</button>
    </div>

    <!-- ===== 下载器 ===== -->
    <div class="section">
      <h3>⬇️ 下载器</h3>
      <p class="section-desc">qBittorrent Web UI 连接信息，不填则跳过自动下载</p>
      <div class="two-col">
        <div><label>地址</label><input v-model="forms.qb.host" placeholder="192.168.1.100" class="input" /></div>
        <div><label>端口</label><input v-model="forms.qb.port" placeholder="8080" class="input" /></div>
      </div>
      <div class="two-col">
        <div><label>用户名</label><input v-model="forms.qb.username" placeholder="admin" class="input" /></div>
        <div><label>密码</label><input v-model="forms.qb.password" type="password" placeholder="选填" class="input" /></div>
      </div>
    </div>

    <!-- ===== 媒体库 ===== -->
    <div class="section">
      <h3>🎬 媒体库</h3>
      <p class="section-desc">Jellyfin / EMBY 连接信息，不填则跳过入库</p>
      <div class="two-col">
        <div><label>地址</label><input v-model="forms.emby.host" placeholder="http://192.168.1.100:8096" class="input" /></div>
        <div><label>API 密钥</label><input v-model="forms.emby.api_key" type="password" placeholder="选填" class="input" /></div>
      </div>
    </div>

    <!-- ===== 通知 ===== -->
    <div class="section">
      <h3>🔔 通知推送</h3>
      <p class="section-desc">下载完成/失败时推送，不填则不通知</p>
      <div class="card">
        <div class="card-header"><span class="card-name">Telegram</span></div>
        <div class="card-body">
          <div class="two-col">
            <div><label>Bot Token</label><input v-model="forms.tg.token" type="password" placeholder="123456:ABC-DEF" class="input" /></div>
            <div><label>Chat ID</label><input v-model="forms.tg.chat_id" placeholder="-1001234567890" class="input" /></div>
          </div>
        </div>
      </div>
      <div class="card">
        <div class="card-header"><span class="card-name">Discord</span></div>
        <div class="card-body">
          <label>Webhook URL</label>
          <input v-model="forms.discord" type="password" placeholder="https://discord.com/api/webhooks/..." class="input" />
        </div>
      </div>
      <button class="btn btn-sm btn-primary" @click="testNotify">测试通知</button>
    </div>

    <!-- ===== 代理 ===== -->
    <div class="section">
      <h3>🌐 代理</h3>
      <p class="section-desc">用于 PT 站点搜索、封面刮削等外网请求，你的环境不需要的可留空</p>
      <label>代理地址</label>
      <input v-model="forms.proxy" placeholder="socks5://127.0.0.1:1080 或留空" class="input" />
    </div>

    <!-- ===== 全局保存 ===== -->
    <div class="section" style="text-align:center">
      <button class="btn btn-primary btn-large" @click="saveAll">💾 保存全部配置</button>
      <p class="save-hint">所有配置持久化保存，重启容器不丢失</p>
    </div>

    <!-- ===== 安全限制 ===== -->
    <div class="section">
      <h3>🛡️ 安全限制</h3>
      <p class="section-desc">控制订阅引擎下载行为，防止 PT 警告和硬盘爆炸</p>

      <div class="limit-item">
        <div class="limit-h"><label>每日下载上限</label><span class="limit-v">{{ limits.max_daily_downloads }} 个</span></div>
        <input type="range" min="1" max="50" v-model.number="limits.max_daily_downloads" class="slider" />
        <span class="limit-d">到上限自动停，次日重置</span>
      </div>
      <div class="limit-item">
        <div class="limit-h"><label>最大并发下载</label><span class="limit-v">{{ limits.max_concurrent_downloads }} 个</span></div>
        <input type="range" min="1" max="10" v-model.number="limits.max_concurrent_downloads" class="slider" />
      </div>
      <div class="limit-item">
        <div class="limit-h"><label>磁盘剩余阈值</label><span class="limit-v">{{ limits.disk_threshold_gb }} GB</span></div>
        <input type="range" min="5" max="200" step="5" v-model.number="limits.disk_threshold_gb" class="slider" />
        <span class="limit-d">低于此值自动暂停</span>
      </div>
      <div class="limit-item">
        <div class="limit-h"><label>最小文件</label><span class="limit-v">{{ limits.min_size_gb }} GB</span></div>
        <input type="range" min="0.1" max="5" step="0.1" v-model.number="limits.min_size_gb" class="slider" />
      </div>
      <div class="limit-item">
        <div class="limit-h"><label>最大文件</label><span class="limit-v">{{ limits.max_size_gb }} GB</span></div>
        <input type="range" min="5" max="100" step="5" v-model.number="limits.max_size_gb" class="slider" />
      </div>
      <div class="limit-item">
        <div class="limit-h"><label>最少做种数</label><span class="limit-v">{{ limits.min_seeders }} 个</span></div>
        <input type="range" min="0" max="20" v-model.number="limits.min_seeders" class="slider" />
      </div>
      <div class="limit-item">
        <div class="limit-h"><label>订阅引擎</label><span class="limit-v">{{ limits.enabled ? '🟢 运行' : '🔴 暂停' }}</span></div>
        <div class="flex gap-8">
          <button class="btn btn-sm" :class="limits.enabled ? 'btn-gray' : 'btn-green'" @click="toggleEngine">{{ limits.enabled ? '暂停' : '启动' }}</button>
          <button class="btn btn-sm btn-primary" @click="runNow">立即执行</button>
        </div>
      </div>
      <div class="limit-s">
        今日 <strong>{{ limits.today_downloaded }}</strong> / {{ limits.max_daily_downloads }}  ·  活跃 <strong>{{ limits.active_downloads }}</strong> / {{ limits.max_concurrent_downloads }}
      </div>
      <button class="btn btn-primary" @click="saveLimits" style="margin-top:12px">保存安全限制</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import {
  getSettings, getPTSitesConfig, getLimits,
  savePTSites, saveAllSettings, updateLimits,
  testNotify as testNotifyApi, runEngineNow,
} from '../api'

const ptSites = ref<any[]>([])
const limits = ref<any>({
  max_daily_downloads: 10, max_concurrent_downloads: 3,
  disk_threshold_gb: 50, min_size_gb: 0.5, max_size_gb: 20,
  min_seeders: 1, enabled: true, today_downloaded: 0, active_downloads: 0,
})

const forms = reactive({
  pt: {} as Record<string, { cookie: string; passkey: string }>,
  qb: { host: '', port: '8080', username: '', password: '' },
  emby: { host: '', api_key: '' },
  tg: { token: '', chat_id: '' },
  discord: '',
  proxy: '',
})

async function savePT() {
  const sites: Record<string, { cookie?: string; passkey?: string }> = {}
  for (const [short, f] of Object.entries(forms.pt)) {
    const d: any = {}
    if (f.cookie) d.cookie = f.cookie
    if (f.passkey) d.passkey = f.passkey
    if (Object.keys(d).length) sites[short] = d
  }
  await savePTSites(sites)
  alert('✅ PT 配置已保存')
  load()
}

async function saveAll() {
  await saveAllSettings({
    qb_host: forms.qb.host,
    qb_port: forms.qb.port,
    qb_username: forms.qb.username,
    qb_password: forms.qb.password,
    emby_host: forms.emby.host,
    emby_api_key: forms.emby.api_key,
    tg_bot_token: forms.tg.token,
    tg_chat_id: forms.tg.chat_id,
    discord_webhook: forms.discord,
    proxy_url: forms.proxy,
  })
  alert('✅ 全部配置已保存')
}

async function saveLimits() {
  const l = limits.value
  await updateLimits({
    max_daily_downloads: l.max_daily_downloads,
    max_concurrent_downloads: l.max_concurrent_downloads,
    disk_threshold_gb: l.disk_threshold_gb,
    min_size_gb: l.min_size_gb,
    max_size_gb: l.max_size_gb,
    min_seeders: l.min_seeders,
    enabled: l.enabled,
  })
  alert('✅ 安全限制已保存')
}

async function toggleEngine() {
  limits.value.enabled = !limits.value.enabled
  await saveLimits()
}

async function runNow() {
  await runEngineNow()
  alert('⚡ 已触发订阅引擎')
}

async function testNotify() {
  await testNotifyApi()
  alert('测试通知已发送')
}

async function load() {
  const [s, pt, l] = await Promise.all([
    getSettings(),
    getPTSitesConfig().catch(() => ({})),
    getLimits().catch(() => ({})),
  ])
  const info = s as any
  ptSites.value = info.pt_sites || []

  // PT 表单
  for (const site of ptSites.value) {
    if (!forms.pt[site.short]) forms.pt[site.short] = { cookie: '', passkey: '' }
  }

  // 加载已有配置到表单
  forms.qb.host = info.qb_configured ? info.qb_host : ''
  forms.emby.host = info.emby_configured ? info.emby_host : ''
  forms.proxy = info.proxy_configured ? info.proxy_url : ''

  Object.assign(limits.value, l as any)
}

onMounted(load)
</script>

<style scoped>
.settings-page { max-width: 700px; }
.page-title { font-size: 24px; margin-bottom: 20px; color: #e1e8ed; }
.section { background: #1a1f2e; border-radius: 12px; padding: 20px; margin-bottom: 16px; }
.section h3 { font-size: 16px; margin-bottom: 4px; color: #e1e8ed; }
.section-desc { font-size: 12px; color: #556; margin-bottom: 16px; }

.card { background: #0f1419; border-radius: 10px; padding: 16px; margin-bottom: 12px; }
.card-header { display: flex; align-items: center; gap: 10px; margin-bottom: 12px; flex-wrap: wrap; }
.card-name { font-size: 14px; font-weight: 600; color: #e1e8ed; }
.card-url { font-size: 11px; color: #556; }
.card-body { display: flex; flex-direction: column; gap: 8px; }
.card-body label { font-size: 12px; color: #8899a6; margin-bottom: -4px; }

.two-col { display: flex; gap: 12px; margin-bottom: 8px; }
.two-col > div { flex: 1; }

label { display: block; font-size: 13px; color: #8899a6; margin-bottom: 4px; }
.input { width: 100%; padding: 10px 14px; border-radius: 8px; border: 1px solid #2a3040; background: #1a1f2e; color: #e1e8ed; font-size: 14px; box-sizing: border-box; }
.input::placeholder { color: #445; }

.badge { font-size: 11px; padding: 2px 8px; border-radius: 10px; }
.badge.on { background: #00ba7c20; color: #00ba7c; }
.badge.off { background: #2a3040; color: #556; }

.btn { padding: 10px 18px; border-radius: 8px; border: none; cursor: pointer; font-size: 14px; display: inline-block; }
.btn-primary { background: #1d9bf0; color: #fff; }
.btn-sm { padding: 6px 14px; font-size: 12px; }
.btn-large { padding: 14px 32px; font-size: 16px; }
.btn-green { background: #00ba7c; color: #fff; }
.btn-gray { background: #2a3040; color: #8899a6; }

.limit-item { background: #0f1419; border-radius: 10px; padding: 16px; margin-bottom: 10px; }
.limit-h { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }
.limit-h label { font-size: 14px; color: #e1e8ed; margin: 0; }
.limit-v { font-size: 16px; font-weight: 600; color: #1d9bf0; }
.limit-d { font-size: 11px; color: #556; display: block; margin-top: 4px; }
.limit-s { font-size: 13px; color: #8899a6; margin-top: 12px; }
.limit-s strong { color: #e1e8ed; }

.slider { width: 100%; height: 6px; appearance: none; background: #2a3040; border-radius: 3px; outline: none; }
.slider::-webkit-slider-thumb { appearance: none; width: 18px; height: 18px; border-radius: 50%; background: #1d9bf0; cursor: pointer; }

.flex { display: flex; gap: 8px; }
.save-hint { font-size: 12px; color: #556; margin-top: 8px; }
</style>