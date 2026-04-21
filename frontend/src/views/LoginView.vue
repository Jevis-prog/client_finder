<template>
  <div class="auth-page">
    <div class="auth-shell">
      <section class="auth-panel">
        <div class="auth-badge">
          <div class="brand-mark">CF</div>
          <div>
            <div class="text-subtitle1">Client Finder Admin</div>
            <div class="text-muted">Веб, Telegram-боты и автоматизация</div>
          </div>
        </div>

        <div class="auth-title">
          <h1>Вход в админку</h1>
          <p class="text-muted">Управление лидами, сообщениями и ручной модерацией.</p>
        </div>

        <div class="form-stack">
          <div class="q-input q-field q-field--outlined">
            <div class="q-field__inner">
              <input
                v-model="form.username"
                class="q-field__native"
                type="text"
                placeholder="Имя пользователя"
              />
            </div>
          </div>

          <div class="q-input q-field q-field--outlined">
            <div class="q-field__inner">
              <input
                v-model="form.password"
                class="q-field__native"
                type="password"
                placeholder="Пароль"
              />
            </div>
          </div>

          <div v-if="error" class="text-negative">
            {{ error }}
          </div>

          <div class="button-stack">
            <button
              class="q-btn bg-primary text-white full-width"
              :disabled="loading"
              @click="handleLogin"
            >
              {{ loading ? 'Входим...' : 'Войти' }}
            </button>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { useAuthStore } from '../store/auth'


const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const form = ref({
  username: '',
  password: '',
})

const loading = ref(false)
const error = ref('')

watch(
  () => route.query.reason,
  (reason) => {
    if (reason === 'session_expired') {
      error.value = 'Сессия истекла. Войдите снова.'
    }
  },
  { immediate: true },
)

const handleLogin = async () => {
  try {
    loading.value = true
    error.value = ''
    await authStore.login(form.value)
    router.push('/')
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Ошибка входа. Проверьте данные.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 32px;
}

.text-muted {
  color: var(--text-muted);
}

.auth-shell {
  width: min(520px, 100%);
  display: grid;
}

.brand-mark {
  width: 48px;
  height: 48px;
  border-radius: 16px;
  display: grid;
  place-items: center;
  background: var(--accent);
  color: #fff;
  font-weight: 700;
}

.auth-panel {
  background: var(--surface);
  border-radius: 24px;
  padding: 28px;
  box-shadow: 0 18px 36px rgba(20, 20, 30, 0.08);
  min-height: 420px;
  display: grid;
  align-content: start;
  gap: 18px;
}

.auth-badge {
  display: flex;
  gap: 12px;
  align-items: center;
  padding: 12px 16px;
  border-radius: 16px;
  background: var(--surface-soft);
}

.auth-title {
  text-align: center;
}

.auth-title h1 {
  margin: 0 0 8px;
  font-size: 32px;
}

.auth-title p {
  margin: 0;
}

.form-stack {
  display: grid;
  gap: 14px;
}

.button-stack {
  display: grid;
  gap: 10px;
  margin-top: 6px;
}
</style>
