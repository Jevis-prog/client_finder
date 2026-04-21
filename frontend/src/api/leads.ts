import api from './axios'


export type Lead = {
  id: number
  external_id: number
  sender_id: number
  chat_id: number
  message_text: string
  is_lead: boolean | null
  reason: string | null
  processing_status: string
  username: string | null
  chat_title: string | null
}

export default {
  list(onlyValid = false) {
    return api.get<Lead[]>('/leads', {
      params: {
        only_valid: onlyValid,
      },
    })
  },
}
