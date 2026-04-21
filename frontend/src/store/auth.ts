import { defineStore } from 'pinia'
import { ref } from 'vue'

import authApi from '../api/auth'
import { getCookie } from '../utils/cookies'
import { hashPassword } from '../utils/crypto'


export const useAuthStore = defineStore('auth', () => {
  const isAuthenticated = ref(false)
  const isInitialized = ref(false)

  async function login(credentials: { username: string; password: string }) {
    try {
      const passwordHash = await hashPassword(credentials.password)
      await authApi.login({
        username: credentials.username,
        password_hash: passwordHash,
      })
      isAuthenticated.value = Boolean(getCookie('access_token'))
      isInitialized.value = true
      return true
    } catch (error) {
      isAuthenticated.value = false
      throw error
    }
  }

  async function logout() {
    try {
      await authApi.logout()
    } finally {
      isAuthenticated.value = false
    }
  }

  function checkAuth() {
    const token = getCookie('access_token')
    isAuthenticated.value = Boolean(token)
    isInitialized.value = true
    return isAuthenticated.value
  }

  return {
    isAuthenticated,
    isInitialized,
    login,
    logout,
    checkAuth,
  }
})
