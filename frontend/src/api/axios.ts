import axios from 'axios'

import router from '../router'
import { useAuthStore } from '../store/auth'


const api = axios.create({
  baseURL: '/api/v1',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      const authStore = useAuthStore()
      authStore.isAuthenticated = false
      if (router.currentRoute.value.path !== '/login') {
        router.replace({ path: '/login', query: { reason: 'session_expired' } })
      }
    }
    return Promise.reject(error)
  },
)

export default api
