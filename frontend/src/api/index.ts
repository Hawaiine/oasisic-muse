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

export async function searchPT(keyword: string, actor?: string) {
  const params: Record<string, string> = { keyword }
  if (actor) params.actor = actor
  return api('/search', { params })
}

export async function getLibraryStatus() {
  return api('/library/status')
}

export async function getRecentMedia(limit = 10) {
  return api('/library/recent', { params: { limit: String(limit) } })
}

export async function refreshLibrary() {
  return api('/library/refresh', { method: 'POST' })
}