import api from './axios'


export default {
  login(payload: { username: string; password_hash: string }) {
    return api.post('/login', payload)
  },
  register(payload: { username: string; password: string }) {
    return api.post('/auth/register', payload)
  },
  logout() {
    return api.post('/logout')
  },
}
