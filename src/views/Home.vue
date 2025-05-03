<template>
  <div class="home container">
    <h1>Latest Profiles</h1>
    <ul v-if="profiles.length">
      <li v-for="p in profiles" :key="p.id">
        <router-link :to="`/profiles/${p.id}`">
          {{ p.parish }} · Born {{ p.birth_year }} · {{ p.sex }}
        </router-link>
      </li>
    </ul>
    <p v-else>No profiles found.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const profiles = ref([])

onMounted(async () => {
  try {
    const res = await api.get('/profiles')
    profiles.value = res.data
  } catch (e) {
    console.error('Failed loading profiles:', e)
  }
})
</script>

<style scoped>
.home { padding: 2rem; }
.home ul { list-style: none; padding: 0; }
.home li { margin: 0.5rem 0; }
</style>
