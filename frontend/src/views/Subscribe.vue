<template>
  <div class="subscribe-page">
    <n-page-header title="订阅管理" subtitle="管理自动搜索与下载任务" style="margin-bottom: 24px;">
      <template #extra>
        <n-button @click="load" size="small">🔄 刷新</n-button>
      </template>
    </n-page-header>

    <n-card :bordered="false" embedded style="margin-bottom: 16px;">
      <n-form inline :model="newSub" @submit.prevent="add">
        <n-form-item label="关键词">
          <n-input v-model:value="newSub.keyword" placeholder="番号或关键词" @keyup.enter="add" style="width: 240px;" />
        </n-form-item>
        <n-form-item label="演员">
          <n-input v-model:value="newSub.actor" placeholder="可选" style="width: 160px;" />
        </n-form-item>
        <n-form-item>
          <n-button type="primary" html-type="submit">➕ 添加订阅</n-button>
        </n-form-item>
      </n-form>
    </n-card>

    <n-card :bordered="false" embedded>
      <n-data-table
        :columns="columns"
        :data="subscribes"
        :bordered="false"
        :striped="true"
        :pagination="{ pageSize: 10 }"
        size="small"
      />
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, h } from 'vue'
import type { DataTableColumns } from 'naive-ui'
import { useMessage } from 'naive-ui'
import { getSubscribes, createSubscribe, toggleSubscribe, deleteSubscribe } from '../api'

const message = useMessage()
const subscribes = ref<any[]>([])
const newSub = ref({ keyword: '', actor: '' })

const columns: DataTableColumns<any> = [
  { title: '关键词', key: 'keyword', ellipsis: { tooltip: true } },
  { title: '演员', key: 'actor', ellipsis: { tooltip: true } },
  {
    title: '状态',
    key: 'enabled',
    width: 80,
    render(row) {
      return h('n-tag', { type: row.enabled ? 'success' : 'default', size: 'small', round: true }, () => row.enabled ? '启用' : '禁用')
    },
  },
  {
    title: '操作',
    key: 'actions',
    width: 120,
    render(row) {
      return h('div', { style: 'display: flex; gap: 4px;' }, [
        h('n-button', {
          size: 'small',
          quaternary: true,
          type: row.enabled ? 'warning' : 'success',
          onClick: () => toggle(row.id),
        }, () => row.enabled ? '禁用' : '启用'),
        h('n-button', {
          size: 'small',
          quaternary: true,
          type: 'error',
          onClick: () => remove(row.id),
        }, () => '删除'),
      ])
    },
  },
]

async function load() {
  try {
    subscribes.value = await getSubscribes()
  } catch {}
}

async function add() {
  if (!newSub.value.keyword.trim()) return
  try {
    await createSubscribe(newSub.value.keyword, newSub.value.actor)
    newSub.value = { keyword: '', actor: '' }
    message.success('添加成功')
    await load()
  } catch {
    message.error('添加失败')
  }
}

async function toggle(id: number) {
  try {
    await toggleSubscribe(id)
    await load()
  } catch {}
}

async function remove(id: number) {
  try {
    await deleteSubscribe(id)
    message.success('已删除')
    await load()
  } catch {}
}

onMounted(load)
</script>

<style scoped>
.subscribe-page { max-width: 960px; }
</style>
