import { ofetch } from 'ofetch'

const api = ofetch.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
})

export async function getAbout() {
  return api('/about')
}

export async function getSettings() {
  return api('/settings')
}

export async function getSubscribes() {
  return api('/subscribes')
}

export async function createSubscribe(keyword: string, actor?: string) {
  return api('/subscribes', { method: 'POST', body: { keyword, actor } })
}

export async function toggleSubscribe(id: number) {
  return api(`/subscribes/${id}/toggle`, { method: 'PATCH' })
}

export async function deleteSubscribe(id: number) {
  return api(`/subscribes/${id}`, { method: 'DELETE' })
}

export async function getDownloads() {
  return api('/downloads')
}

export async function getDownloadStats() {
  return api('/downloads/stats')
}

export async function testNotify() {
  return api('/notify/test', { method: 'POST' })
}

export async function getNotifyStatus() {
  return api('/notify/status')
}

export async function healthCheck() {
  return api('/health')
}