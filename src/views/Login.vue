<template>
  <div class="login container">
    <h2>Login</h2>
    <form @submit.prevent="login">
      <div><label>Username</label><input v-model="username" required/></div>
      <div><label>Password</label><input type="password" v-model="password" required/></div>
      <button type="submit">Log In</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'

const router = useRouter()
const username = ref('')
const password = ref('')

async function login() {
  try {
    const { data } = await api.post('/auth/login', { username: username.value, password: password.value })
    localStorage.setItem('jwt', data.access_token)
    router.push('/')
  } catch (e) {
    console.error('Login error:', e)
  }
}
</script>

<style scoped>
.login { padding: 2rem; }
.login div { margin-bottom: 1rem; }
</style>
