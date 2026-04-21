import api from './axios'


export default {
  login(payload: { username: string; password: string }) {
    return api.post('/login', payload)
  },
  me() {
    return api.get('/me')
  },
  logout() {
    return api.post('/logout')
  },
}
