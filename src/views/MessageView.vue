<template>
    <div class="messages container">
      <h2>Chat with {{ otherName }}</h2>
      <div class="history">
        <div
          v-for="m in messages"
          :key="m.id"
          :class="['msg', m.from_me ? 'sent' : 'received']"
        >
          <p>{{ m.content }}</p>
          <small>{{ new Date(m.timestamp).toLocaleString() }}</small>
        </div>
      </div>
      <form @submit.prevent="send">
        <input
          v-model="newMsg"
          placeholder="Type a message…"
          required
        />
        <button type="submit">Send</button>
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useRoute }       from 'vue-router'
  import api                 from '@/services/api'
  
  const route      = useRoute()
  const otherId    = Number(route.params.id)
  const messages   = ref([])
  const newMsg     = ref('')
  const otherName  = ref('')
  
  async function loadConversation() {
    try {
      const { data } = await api.get(`/messages/${otherId}`)
      messages.value = data
    } catch (e) {
      console.error('Failed to load messages:', e)
    }
  }
  
  async function send() {
    try {
      await api.post('/messages', {
        recipient_id: otherId,
        content: newMsg.value
      })
      newMsg.value = ''
      await loadConversation()
    } catch (e) {
      console.error('Send failed:', e)
    }
  }
  
  onMounted(async () => {
    // load conversation
    await loadConversation()
    // (optional) fetch the other user's name
    const meId = Number(localStorage.getItem('user_id'))
    if (otherId === meId) {
      otherName.value = 'yourself'
    } else {
      const { data: u } = await api.get(`/users/${otherId}`)
      otherName.value = u.name
    }
  })
  </script>
  
  <style scoped>
  .messages { padding: 2rem; display: flex; flex-direction: column; }
  .history { flex: 1; overflow-y: auto; margin-bottom: 1rem; }
  .msg { max-width: 60%; margin: 0.5rem 0; padding: 0.5rem; border-radius: 8px; }
  .sent { align-self: flex-end; background: var(--primary); color: #fff; }
  .received { align-self: flex-start; background: #eee; }
  form { display: flex; }
  input { flex: 1; padding: 0.5rem; }
  button { margin-left: 0.5rem; }
  </style>
  