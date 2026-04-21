<template>
  <main class="dashboard-page">
    <section class="topbar">
      <div class="brand">
        <div class="brand-mark">CF</div>
        <div>
          <strong>Client Finder Admin</strong>
          <div class="text-muted">Лиды и результаты анализа</div>
        </div>
      </div>

      <div class="topbar-actions">
        <router-link class="nav-link" to="/stats">Статистика</router-link>
        <button class="q-btn bg-grey-2 text-dark" @click="handleLogout">
          Выйти
        </button>
      </div>
    </section>

    <section class="panel">
      <div class="panel-head">
        <div>
          <h1>Лиды</h1>
          <p class="text-muted">
            Сообщения, которые бот пометил как потенциальные клиентские запросы.
          </p>
        </div>

        <div class="panel-actions">
          <label class="filter-toggle">
            <input v-model="onlyValid" type="checkbox" />
            <span>Только валидные</span>
          </label>

          <button class="q-btn bg-grey-2 text-dark" :disabled="loading" @click="loadLeads">
            {{ loading ? 'Обновляем...' : 'Обновить' }}
          </button>
        </div>
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
const onlyValid = ref(false)

const loadLeads = async () => {
  try {
    loading.value = true
    error.value = ''
    const { data } = await leadsApi.list(onlyValid.value)
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
  gap: 26px;
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
  padding: 20px 24px;
  border-radius: 26px;
  background: linear-gradient(135deg, rgba(34, 29, 26, 0.94) 0%, rgba(64, 45, 31, 0.92) 100%);
  box-shadow: 0 24px 48px rgba(53, 31, 17, 0.18);
  color: #fff5eb;
}

.brand {
  display: flex;
  gap: 12px;
  align-items: center;
}

.brand-mark {
  width: 48px;
  height: 48px;
  border-radius: 16px;
  display: grid;
  place-items: center;
  background: linear-gradient(135deg, #f2c28c 0%, #d57a48 100%);
  color: #442010;
  font-weight: 700;
}

.panel {
  background: linear-gradient(180deg, rgba(255, 251, 246, 0.92) 0%, rgba(248, 239, 228, 0.88) 100%);
  border: 1px solid rgba(82, 56, 38, 0.08);
  border-radius: 28px;
  padding: 28px;
  box-shadow: 0 20px 40px rgba(62, 38, 20, 0.1);
}

.panel-head {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: flex-start;
  margin-bottom: 16px;
}

.topbar-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.nav-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 42px;
  padding: 0 16px;
  border-radius: 14px;
  background: rgba(255, 244, 232, 0.12);
  color: #fff5eb;
  text-decoration: none;
  border: 1px solid rgba(255, 229, 201, 0.12);
}

.panel-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.filter-toggle {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 11px 14px;
  border-radius: 14px;
  background: rgba(239, 229, 215, 0.8);
  color: #5b4d42;
  font-size: 14px;
  border: 1px solid rgba(82, 56, 38, 0.06);
}

.panel h1 {
  margin: 0 0 12px;
}

.panel p {
  margin: 0;
}

.empty-state {
  padding: 22px;
  border-radius: 20px;
  border: 1px dashed rgba(82, 56, 38, 0.16);
  background: rgba(239, 229, 215, 0.66);
}

.lead-list {
  display: grid;
  gap: 12px;
}

.lead-card {
  border: 1px solid rgba(82, 56, 38, 0.08);
  border-radius: 22px;
  padding: 18px;
  display: grid;
  gap: 12px;
  background:
    linear-gradient(180deg, rgba(255, 251, 246, 0.96) 0%, rgba(243, 233, 220, 0.9) 100%);
  box-shadow: 0 14px 26px rgba(62, 38, 20, 0.06);
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
  padding: 7px 12px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
  background: rgba(201, 111, 59, 0.14);
  color: var(--accent-strong);
}
</style>
