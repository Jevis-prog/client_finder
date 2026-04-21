<template>
  <main class="stats-page">
    <section class="topbar">
      <div class="brand">
        <div class="brand-mark">CF</div>
        <div>
          <strong>Client Finder Admin</strong>
          <div class="text-muted">Статистика лидов и обработки</div>
        </div>
      </div>

      <div class="topbar-actions">
        <router-link class="nav-link" to="/">Лиды</router-link>
        <button class="q-btn bg-grey-2 text-dark" :disabled="loading" @click="loadStats">
          {{ loading ? 'Обновляем...' : 'Обновить' }}
        </button>
        <button class="q-btn bg-grey-2 text-dark" @click="handleLogout">
          Выйти
        </button>
      </div>
    </section>

    <section class="hero-layout">
      <div class="hero-copy">
        <h1>Сводка по лидам</h1>
        <p class="text-muted">
          Круговая диаграмма показывает соотношение всех обработанных лидов и тех, которые помечены как валидные.
        </p>
      </div>

      <div class="chart-card">
        <div class="pie-chart" :style="pieStyle">
          <div class="pie-center">
            <strong>{{ validPercent }}%</strong>
            <span>is_lead=true</span>
          </div>
        </div>

        <div class="chart-numbers">
          <div>
            <span class="metric-caption">Всего лидов</span>
            <strong>{{ stats.total_leads }}</strong>
          </div>
          <div>
            <span class="metric-caption">Валидных</span>
            <strong>{{ stats.valid_leads }}</strong>
          </div>
        </div>
      </div>
    </section>

    <section class="metrics-grid">
      <article class="metric-card accent">
        <span class="metric-caption">Всего лидов</span>
        <strong class="metric-value">{{ stats.total_leads }}</strong>
      </article>

      <article class="metric-card">
        <span class="metric-caption">Лидов с is_lead=true</span>
        <strong class="metric-value">{{ stats.valid_leads }}</strong>
      </article>

      <article class="metric-card">
        <span class="metric-caption">Всего сообщений</span>
        <strong class="metric-value">{{ stats.total_messages }}</strong>
      </article>

      <article class="metric-card">
        <span class="metric-caption">Обработано сообщений</span>
        <strong class="metric-value">{{ stats.processed_messages }}</strong>
      </article>

      <article class="metric-card">
        <span class="metric-caption">Обрабатывает в сутки</span>
        <strong class="metric-value">{{ stats.processed_last_day }}</strong>
      </article>

      <article class="metric-card">
        <span class="metric-caption">Обрабатывает в час</span>
        <strong class="metric-value">{{ stats.processed_last_hour }}</strong>
      </article>
    </section>

    <div v-if="error" class="error-banner">{{ error }}</div>
  </main>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

import statsApi, { type Stats } from '../api/stats'
import { useAuthStore } from '../store/auth'


const router = useRouter()
const authStore = useAuthStore()
const loading = ref(false)
const error = ref('')
const stats = ref<Stats>({
  total_messages: 0,
  processed_messages: 0,
  total_leads: 0,
  valid_leads: 0,
  processed_last_day: 0,
  processed_last_hour: 0,
})

const validPercent = computed(() => {
  if (!stats.value.total_leads) {
    return 0
  }

  return Math.round((stats.value.valid_leads / stats.value.total_leads) * 100)
})

const pieStyle = computed(() => ({
  background: `conic-gradient(var(--accent) 0deg ${validPercent.value * 3.6}deg, var(--surface-soft) ${validPercent.value * 3.6}deg 360deg)`,
}))

const loadStats = async () => {
  try {
    loading.value = true
    error.value = ''
    const { data } = await statsApi.get()
    stats.value = data
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Не удалось загрузить статистику.'
  } finally {
    loading.value = false
  }
}

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}

onMounted(() => {
  loadStats()
})
</script>

<style scoped>
.stats-page {
  display: grid;
  gap: 26px;
  padding: 28px clamp(20px, 4vw, 48px);
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

.text-muted {
  color: var(--text-muted);
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

.hero-layout {
  display: grid;
  grid-template-columns: minmax(280px, 1.1fr) minmax(280px, 420px);
  gap: 24px;
}

.hero-copy,
.chart-card,
.metric-card {
  background: linear-gradient(180deg, rgba(255, 251, 246, 0.94) 0%, rgba(248, 239, 228, 0.88) 100%);
  border-radius: 28px;
  border: 1px solid rgba(82, 56, 38, 0.08);
  box-shadow: 0 20px 40px rgba(62, 38, 20, 0.1);
}

.hero-copy {
  padding: 32px;
}

.hero-copy h1 {
  margin: 0 0 12px;
  font-size: clamp(30px, 4vw, 44px);
}

.hero-copy p {
  margin: 0;
  max-width: 48ch;
  line-height: 1.6;
}

.chart-card {
  padding: 28px;
  display: grid;
  gap: 22px;
  justify-items: center;
}

.pie-chart {
  width: 244px;
  height: 244px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  box-shadow: inset 0 0 0 12px rgba(255, 250, 244, 0.36);
}

.pie-center {
  width: 134px;
  height: 134px;
  border-radius: 50%;
  background: linear-gradient(180deg, rgba(255, 251, 246, 0.98) 0%, rgba(245, 236, 224, 0.94) 100%);
  display: grid;
  place-items: center;
  text-align: center;
  box-shadow: inset 0 0 0 1px rgba(82, 56, 38, 0.08);
}

.pie-center strong {
  font-size: 30px;
  line-height: 1;
}

.pie-center span {
  color: var(--text-muted);
  font-size: 13px;
}

.chart-numbers {
  width: 100%;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.chart-numbers > div {
  padding: 16px;
  border-radius: 18px;
  background: rgba(239, 229, 215, 0.74);
  display: grid;
  gap: 8px;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
}

.metric-card {
  padding: 24px;
  display: grid;
  gap: 10px;
}

.metric-card.accent {
  background: linear-gradient(145deg, var(--accent) 0%, #844224 100%);
  color: #fff;
}

.metric-caption {
  font-size: 14px;
  color: var(--text-muted);
}

.metric-card.accent .metric-caption {
  color: rgba(255, 255, 255, 0.82);
}

.metric-value {
  font-size: clamp(28px, 5vw, 40px);
  line-height: 1;
}

.error-banner {
  padding: 16px 18px;
  border-radius: 14px;
  background: #fff0ef;
  color: #b42318;
}

@media (max-width: 900px) {
  .hero-layout {
    grid-template-columns: 1fr;
  }

  .topbar {
    flex-direction: column;
    align-items: flex-start;
  }

  .topbar-actions {
    width: 100%;
    flex-wrap: wrap;
  }
}
</style>
