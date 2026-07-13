# 🎵 Oasisic Muse

> AV 自动化刮削下载工具

基于 FastAPI + Vue 3 的轻量化 **AV 自动化管理工具**，对标 `envyafish/byte-muse`，支持订阅搜索、自动下载、元数据刮削、媒体库集成与多渠道通知推送。

---

## ✨ 功能特性

| 模块 | 功能 |
|------|------|
| 📋 **订阅管理** | 按关键词/番号/演员自动搜索订阅 |
| ⬇️ **自动下载** | 对接 qBittorrent 全自动拉取 |
| 🏷️ **元数据刮削** | 自动刮削封面、演员、元数据 |
| 🎬 **媒体库集成** | 对接 EMBY/Jellyfin 自动入库 |
| 🔔 **多渠道通知** | Telegram + Discord 推送 |
| 🌐 **代理支持** | 节点配置，适配你的 homelab 环境 |
| ⚙️ **Web 管理面板** | 完整的浏览器配置界面 |

---

## 🚀 快速开始

### Docker Compose（推荐）

```bash
# 1. 下载配置
mkdir oasisic-muse && cd oasisic-muse
wget https://raw.githubusercontent.com/Hawaiine/oasisic-muse/main/compose.yaml
cp .env.example .env
# 编辑 .env 填写配置

# 2. 启动
docker compose up -d
```

### Docker 单容器

```bash
docker run -d \
  --name oasisic-muse \
  -p 8000:8000 \
  -v ./data:/data \
  -e TZ=Asia/Shanghai \
  barryallen26/oasisic-muse:latest
```

### 访问面板

打开浏览器访问 `http://<你的IP>:8000`

---

## ⚙️ 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `PORT` | Web 端口 | `8000` |
| `QB_HOST` | qBittorrent 地址 | - |
| `QB_PORT` | qBittorrent 端口 | `8080` |
| `QB_USERNAME` | qBittorrent 用户名 | - |
| `QB_PASSWORD` | qBittorrent 密码 | - |
| `TG_BOT_TOKEN` | Telegram Bot Token | - |
| `TG_CHAT_ID` | Telegram 聊天 ID | - |
| `DISCORD_WEBHOOK_URL` | Discord Webhook URL | - |
| `EMBY_HOST` | EMBY 服务器地址 | - |
| `EMBY_API_KEY` | EMBY API 密钥 | - |
| `PROXY_URL` | 代理地址 | - |

---

## ⚠️ 免责声明

**本项目仅供内部交流学习使用，不得对外传播、转载或用于任何商业用途。**
所有资源来自网络，版权归原作者所有。使用者应对自己的行为负责，项目开发者不承担任何法律责任。

---

## 📄 License

MIT