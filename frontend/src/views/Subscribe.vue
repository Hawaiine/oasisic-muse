<template>
  <div class="subscribe-page">
    <div class="page-header" style="display: flex; justify-content: space-between; align-items: flex-start;">
      <div>
        <h2>订阅管理</h2>
        <p>管理自动搜索与下载任务</p>
      </div>
      <div style="display: flex; gap: 8px;">
        <button class="btn btn-primary btn-sm" @click="addTask">➕ 新建任务</button>
        <button class="btn btn-sm" @click="load">🔄 刷新</button>
      </div>
    </div>

    <div class="card">
      <table v-if="tasks.length > 0">
        <thead>
          <tr>
            <th>名称</th>
            <th>关键词</th>
            <th>规则</th>
            <th>频率</th>
            <th>状态</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="t in tasks" :key="t.id">
            <td style="color: var(--text-primary);">{{ t.name }}</td>
            <td>{{ t.keywords }}</td>
            <td>{{ t.rules || '-' }}</td>
            <td>{{ t.interval }}</td>
            <td><span :class="['badge', t.enabled ? 'badge-success' : 'badge-muted']">{{ t.enabled ? '启用' : '停用' }}</span></td>
            <td>
              <div style="display: flex; gap: 4px;">
                <button class="btn btn-sm btn-icon" @click="toggleTask(t)">
                  {{ t.enabled ? '⏸' : '▶' }}
                </button>
                <button class="btn btn-sm btn-icon" @click="deleteTask(t.id)">🗑</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else class="empty-state">
        <div class="empty-state-icon">📋</div>
        <div class="empty-state-text">暂无订阅任务</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { api } from '@/api'

interface Task {
  id: string
  name: string
  keywords: string
  rules: string
  interval: string
  enabled: boolean
}

const tasks = ref<Task[]>([])

async function load() {
  try {
    const res = await api('/api/subscriptions')
    tasks.value = res || []
  } catch (e) {
    tasks.value = []
  }
}

async function addTask() {
  // Placeholder for now
  console.log('add task')
}

function toggleTask(t: Task) {
  t.enabled = !t.enabled
}

async function deleteTask(id: string) {
  try {
    await api(`/api/subscriptions/${id}`, { method: 'DELETE' })
    load()
  } catch (e) {
    console.error(e)
  }
}

onMounted(load)
</script>
