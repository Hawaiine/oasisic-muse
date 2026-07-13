<template>
  <div class="subscribe-page">
    <h1 class="page-title">订阅管理</h1>
    <div class="add-form">
      <input v-model="keyword" placeholder="关键词 / 番号" class="input" @keyup.enter="add" />
      <input v-model="actor" placeholder="演员（可选）" class="input" />
      <button class="btn btn-primary" @click="add">添加订阅</button>
    </div>
    <div class="list">
      <div v-for="item in subscribes" :key="item.id" class="list-item">
        <div class="item-info">
          <div class="item-keyword">{{ item.keyword }}</div>
          <div class="item-actor" v-if="item.actor">{{ item.actor }}</div>
        </div>
        <div class="item-actions">
          <span class="badge" :class="item.enabled ? 'badge-green' : 'badge-gray'">
            {{ item.enabled ? '启用' : '禁用' }}
          </span>
          <button class="btn btn-sm" @click="toggle(item.id)">切换</button>
          <button class="btn btn-sm btn-danger" @click="remove(item.id)">删除</button>
        </div>
      </div>
      <div v-if="subscribes.length === 0" class="empty">暂无订阅，添加一个吧</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getSubscribes, createSubscribe, toggleSubscribe, deleteSubscribe } from '../api'

const keyword = ref('')
const actor = ref('')
const subscribes = ref<any[]>([])

async function load() {
  const res = await getSubscribes()
  subscribes.value = (res as any).items || []
}

async function add() {
  if (!keyword.value.trim()) return
  await createSubscribe(keyword.value.trim(), actor.value.trim())
  keyword.value = ''
  actor.value = ''
  await load()
}

async function toggle(id: number) {
  await toggleSubscribe(id)
  await load()
}

async function remove(id: number) {
  await deleteSubscribe(id)
  await load()
}

onMounted(load)
</script>

<style scoped>
.subscribe-page { max-width: 700px; }
.page-title { font-size: 24px; margin-bottom: 20px; color: #e1e8ed; }
.add-form { display: flex; gap: 8px; margin-bottom: 20px; flex-wrap: wrap; }
.input { flex: 1; min-width: 150px; padding: 10px 14px; border-radius: 8px; border: 1px solid #2a3040; background: #1a1f2e; color: #e1e8ed; font-size: 14px; }
.input::placeholder { color: #556; }
.btn { padding: 10px 18px; border-radius: 8px; border: none; cursor: pointer; font-size: 14px; background: #2a3040; color: #e1e8ed; }
.btn-primary { background: #1d9bf0; color: #fff; }
.btn-sm { padding: 6px 12px; font-size: 12px; }
.btn-danger { background: #f4212e; color: #fff; }
.list { display: flex; flex-direction: column; gap: 8px; }
.list-item { display: flex; justify-content: space-between; align-items: center; padding: 14px 16px; background: #1a1f2e; border-radius: 10px; }
.item-info { display: flex; flex-direction: column; gap: 2px; }
.item-keyword { font-size: 15px; color: #e1e8ed; }
.item-actor { font-size: 12px; color: #8899a6; }
.item-actions { display: flex; align-items: center; gap: 8px; }
.badge { padding: 3px 10px; border-radius: 20px; font-size: 12px; }
.badge-green { background: #00ba7c20; color: #00ba7c; border: 1px solid #00ba7c; }
.badge-gray { background: #2a3040; color: #8899a6; }
.empty { text-align: center; padding: 40px; color: #556; font-size: 14px; }
</style>