<template>
    <div>Logging out…</div>
  </template>
  
  <script setup>
  import { onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  
  const router = useRouter()
  
  onMounted(() => {
    localStorage.removeItem('jwt')
    router.push('/login')
  })
  </script>
  