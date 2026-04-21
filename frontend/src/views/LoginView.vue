<template>
  <div class="auth-page">
    <div class="auth-shell">
      <section class="auth-panel">
        <div class="auth-badge">
          <div class="brand-mark">CF</div>
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
  width: min(560px, 100%);
  display: grid;
}

.brand-mark {
  width: 56px;
  height: 56px;
  border-radius: 20px;
  display: grid;
  place-items: center;
  background: linear-gradient(140deg, var(--accent) 0%, #5a2d1a 100%);
  color: #fff;
  font-weight: 700;
  box-shadow: 0 18px 34px rgba(90, 45, 26, 0.28);
}

.auth-panel {
  background:
    linear-gradient(180deg, rgba(255, 252, 248, 0.96) 0%, rgba(250, 241, 230, 0.92) 100%);
  border: 1px solid rgba(82, 56, 38, 0.08);
  border-radius: 32px;
  padding: 34px;
  box-shadow: 0 28px 60px rgba(62, 38, 20, 0.12);
  min-height: 380px;
  display: grid;
  align-content: start;
  gap: 24px;
  position: relative;
  overflow: hidden;
}

.auth-panel::before {
  content: "";
  position: absolute;
  inset: 0 auto auto 0;
  width: 100%;
  height: 8px;
  background: linear-gradient(90deg, var(--accent) 0%, #d9a066 55%, #6c8c7f 100%);
}

.auth-badge {
  display: flex;
  gap: 12px;
  align-items: center;
  justify-content: center;
  padding: 18px;
  border-radius: 22px;
  background: rgba(239, 229, 215, 0.7);
  border: 1px solid rgba(82, 56, 38, 0.06);
}

.form-stack {
  display: grid;
  gap: 16px;
}

.button-stack {
  display: grid;
  gap: 10px;
  margin-top: 10px;
}
</style>
