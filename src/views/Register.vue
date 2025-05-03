<template>
    <div class="register container">
      <h2>Register</h2>
      <form @submit.prevent="register">
        <div><label>Name</label><input v-model="name" required/></div>
        <div><label>Username</label><input v-model="username" required/></div>
        <div><label>Email</label><input type="email" v-model="email" required/></div>
        <div><label>Password</label><input type="password" v-model="password" required/></div>
        <button type="submit">Sign Up</button>
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import api from '@/services/api'
  
  const router = useRouter()
  const name     = ref('')
  const username = ref('')
  const email    = ref('')
  const password = ref('')
  
  async function register() {
    try {
      await api.post('/register', { name: name.value, username: username.value, email: email.value, password: password.value })
      router.push('/login')
    } catch (e) {
      console.error('Register error:', e)
    }
  }
  </script>
  
  <style scoped>
  .register { padding: 2rem; }
  .register div { margin-bottom: 1rem; }
  </style>
  