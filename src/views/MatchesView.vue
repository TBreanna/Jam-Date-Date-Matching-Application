<template>
    <div class="matches container">
      <h2>Matches for Profile #{{ profileId }}</h2>
      <ul v-if="matches.length">
        <li v-for="m in matches" :key="m.id" class="match-item">
          <router-link :to="`/profiles/${m.id}`">
            {{ m.parish }} · Born {{ m.birth_year }} · Score: {{ m.match_score }}
          </router-link>
        </li>
      </ul>
      <p v-else>No matches found for this profile.</p>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useRoute }      from 'vue-router'
  import api                from '@/services/api'
  
  const route     = useRoute()
  const profileId = Number(route.params.id)
  const matches   = ref([])
  
  async function loadMatches() {
    try {
      const { data } = await api.get(`/profiles/matches/${profileId}`)
      matches.value = data
    } catch (e) {
      console.error('Failed to load matches:', e)
    }
  }
  
  onMounted(loadMatches)
  </script>
  
  <style scoped>
  .matches {
    padding: 2rem;
  }
  .match-item {
    margin: 0.5rem 0;
  }
  </style>
  