<template>
  <div class="reports container">
    <h2>Reports</h2>

    <!-- Top N Most Favourited -->
    <section>
      <h3>Top {{ N }} Most Favourited</h3>
      <ul v-if="topFavs.length">
        <li v-for="u in topFavs" :key="u.profile.id">
          <router-link :to="`/profiles/${u.profile.id}`">
            {{ u.profile.parish }} (★ {{ u.count }})
          </router-link>
        </li>
      </ul>
      <p v-else>No one has been favourited yet.</p>
    </section>

    <!-- Your Favourites -->
    <section class="mt-4">
      <h3>Your Favourites</h3>
      <ul v-if="myFavs.length">
        <li v-for="p in myFavs" :key="p.id">
          <router-link :to="`/profiles/${p.id}`">{{ p.parish }}</router-link>
          <!-- broken-heart icon as the remove button -->
          <button
            class="remove-btn"
            @click="removeFavourite(p.id)"
            aria-label="Remove favourite"
            title="Remove from favourites"
          >💔</button>
          <!-- chat icon to message this user -->
          <router-link
            :to="`/messages/${p.user_id || p.id}`"
            class="chat-btn"
            title="Chat with {{ p.parish }}"
          >💬</router-link>
        </li>
      </ul>
      <p v-else>You haven’t favourited anyone yet.</p>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const N = 20
const topFavs = ref([])
const myFavs = ref([])

async function loadReports() {
  try {
    const { data: top } = await api.get(`/users/favourites/${N}`)
    topFavs.value = top

    const me = Number(localStorage.getItem('user_id'))
    const { data: mine } = await api.get(`/users/${me}/favourites`)
    myFavs.value = mine
  } catch (e) {
    console.error('Failed to load reports:', e)
  }
}

async function removeFavourite(profileId) {
  try {
    await api.delete(`/profiles/${profileId}/favourite`)
    await loadReports()
  } catch (e) {
    console.error('Failed to remove favourite:', e)
  }
}

onMounted(loadReports)
</script>

<style scoped>
.reports {
  padding: 2rem;
}
.mt-4 {
  margin-top: 1.5rem;
}
.reports ul {
  list-style: none;
  padding: 0;
}
.reports li {
  display: flex;
  align-items: center;
  margin: 0.5rem 0;
}
/* broken-heart button */
.remove-btn {
  background: transparent;
  border: none;
  cursor: pointer;
  margin-left: 0.5rem;
  font-size: 1.2rem;
  line-height: 1;
  padding: 0;
}
.remove-btn:hover {
  transform: scale(1.1);
}

/* chat icon link */
.chat-btn {
  margin-left: 0.3rem;
  font-size: 1.2rem;
  text-decoration: none;
}
.chat-btn:hover {
  transform: scale(1.1);
}
</style>
