<template>
  <main class="dashboard-page">
    <section class="topbar">
      <div class="brand">
        <div class="brand-mark">CF</div>
        <div>
          <strong>Client Finder Admin</strong>
          <div class="text-muted">Заготовка админки</div>
        </div>
      </div>

      <button class="q-btn bg-grey-2 text-dark" @click="handleLogout">
        Выйти
      </button>
    </section>

    <section class="panel">
      <div class="panel-head">
        <div>
          <h1>Лиды</h1>
          <p class="text-muted">
            Сообщения, которые бот пометил как потенциальные клиентские запросы.
          </p>
        </div>

        <button class="q-btn bg-grey-2 text-dark" :disabled="loading" @click="loadLeads">
          {{ loading ? 'Обновляем...' : 'Обновить' }}
        </button>
      </div>

      <div v-if="error" class="text-negative">{{ error }}</div>

      <div v-if="!leads.length && !loading" class="empty-state">
        Пока нет лидов для отображения.
      </div>

      <div v-else class="lead-list">
        <article v-for="lead in leads" :key="lead.id" class="lead-card">
          <div class="lead-meta">
            <strong>{{ lead.chat_title || `Chat ${lead.chat_id}` }}</strong>
            <span class="text-muted">{{ lead.username || `User ${lead.sender_id}` }}</span>
          </div>
          <p class="lead-text">{{ lead.message_text }}</p>
          <div class="lead-footer">
            <span class="status-pill">{{ lead.processing_status }}</span>
            <span class="text-muted">{{ lead.reason || 'Без пояснения' }}</span>
          </div>
        </article>
      </div>
    </section>
  </main>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

import leadsApi, { type Lead } from '../api/leads'
import { useAuthStore } from '../store/auth'


const router = useRouter()
const authStore = useAuthStore()
const leads = ref<Lead[]>([])
const loading = ref(false)
const error = ref('')

const loadLeads = async () => {
  try {
    loading.value = true
    error.value = ''
    const { data } = await leadsApi.list()
    leads.value = data
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Не удалось загрузить лиды.'
  } finally {
    loading.value = false
  }
}

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}

onMounted(() => {
  loadLeads()
})
</script>

<style scoped>
.dashboard-page {
  display: grid;
  gap: 24px;
  padding: 28px clamp(20px, 4vw, 48px);
}

.text-muted {
  color: var(--text-muted);
}

.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 18px 22px;
  border-radius: 18px;
  background: var(--surface);
  box-shadow: 0 18px 36px rgba(20, 20, 30, 0.06);
}

.brand {
  display: flex;
  gap: 12px;
  align-items: center;
}

.brand-mark {
  width: 44px;
  height: 44px;
  border-radius: 14px;
  display: grid;
  place-items: center;
  background: var(--accent-soft);
  color: var(--accent);
  font-weight: 700;
}

.panel {
  background: var(--surface);
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 16px 32px rgba(20, 20, 30, 0.06);
}

.panel-head {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: flex-start;
  margin-bottom: 16px;
}

.panel h1 {
  margin: 0 0 12px;
}

.panel p {
  margin: 0;
}

.empty-state {
  padding: 18px;
  border-radius: 16px;
  border: 1px dashed var(--border-soft);
  background: var(--surface-soft);
}

.lead-list {
  display: grid;
  gap: 12px;
}

.lead-card {
  border: 1px solid var(--border-soft);
  border-radius: 16px;
  padding: 16px;
  display: grid;
  gap: 10px;
  background: var(--surface-soft);
}

.lead-meta {
  display: flex;
  justify-content: space-between;
  gap: 12px;
}

.lead-text {
  margin: 0;
  white-space: pre-wrap;
  line-height: 1.5;
}

.lead-footer {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: center;
}

.status-pill {
  padding: 6px 12px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
  background: var(--accent-soft);
  color: var(--accent);
}
</style>
