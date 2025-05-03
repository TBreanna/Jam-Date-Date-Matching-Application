<template>
  <div class="reports container">
    <h2>Reports</h2>

    <section>
      <h3>Top {{ N }} Most Favoured Users</h3>
      <ul>
        <li v-for="u in topFavs" :key="u.user.id">
          {{ u.user.name }} (★ {{ u.count }})
        </li>
      </ul>
    </section>

    <section>
      <h3>Your Favourites</h3>
      <ul>
        <li v-for="p in myFavs" :key="p.id">
          {{ p.user.name }}
        </li>
      </ul>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const N        = 20
const topFavs  = ref([])
const myFavs   = ref([])

onMounted(async () => {
  try {
    // fetch top N most favourited users
    const res1 = await api.get(`/users/favourties/${N}`)
    topFavs.value = res1.data

    // retrieve current user ID (assumes you stored it on login)
    const storedUser = localStorage.getItem('user')
    const me = storedUser ? JSON.parse(storedUser).id : null

    if (me) {
      // fetch users this user has favourited
      const res2 = await api.get(`/users/${me}/favourites`)
      myFavs.value = res2.data
    }
  } catch (e) {
    console.error('Failed to load reports:', e)
  }
})
</script>

<style scoped>
.reports {
  padding: 2rem;
}
</style>
