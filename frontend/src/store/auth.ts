import { defineStore } from 'pinia'
import { ref } from 'vue'

import authApi from '../api/auth'


export const useAuthStore = defineStore('auth', () => {
  const isAuthenticated = ref(false)
  const isInitialized = ref(false)

  async function login(credentials: { username: string; password: string }) {
    try {
      await authApi.login({
        username: credentials.username,
        password: credentials.password,
      })
      await checkAuth()
      return true
    } catch (error) {
      isAuthenticated.value = false
      isInitialized.value = true
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

  async function checkAuth() {
    try {
      await authApi.me()
      isAuthenticated.value = true
    } catch {
      isAuthenticated.value = false
    }
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
