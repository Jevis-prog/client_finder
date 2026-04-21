import api from './axios'


export type Stats = {
  total_messages: number
  processed_messages: number
  total_leads: number
  valid_leads: number
  processed_last_day: number
  processed_last_hour: number
}

export default {
  get() {
    return api.get<Stats>('/stats')
  },
}
