<!-- src/views/Profile.vue -->
<template>
  <div class="profile-detail container">
    <div v-if="profile">
      <img
        v-if="profile.photo_url"
        :src="profile.photo_url"
        alt="Profile Photo"
        class="profile-photo"
      />
      <h1>{{ profile.parish }}</h1>
      <p><strong>Born:</strong> {{ profile.birth_year }}</p>
      <p><strong>Sex:</strong> {{ profile.sex }}</p>
      <p><strong>Race:</strong> {{ profile.race }}</p>
      <p><strong>Description:</strong> {{ profile.description }}</p>
      <p><strong>Biography:</strong> {{ profile.biography }}</p>
      <p><strong>Height:</strong> {{ profile.height }} in</p>
      <p><strong>Favourite Cuisine:</strong> {{ profile.fav_cuisine }}</p>
      <p><strong>Favourite Colour:</strong> {{ profile.fav_colour }}</p>
      <p><strong>Favourite Subject:</strong> {{ profile.fav_school_subject }}</p>
      <p><strong>Political:</strong> {{ profile.political ? 'Yes' : 'No' }}</p>
      <p><strong>Religious:</strong> {{ profile.religious ? 'Yes' : 'No' }}</p>
      <p><strong>Family Oriented:</strong> {{ profile.family_oriented ? 'Yes' : 'No' }}</p>

      <!-- only non‐owners can add to favourites -->
      <button
        v-if="profile.user_id !== currentUserId"
        @click="addFavourite(profile.id)"
      >
        ❤️ Add to Favourites
      </button>

      <!-- owner can delete -->
      <button
        v-if="profile.user_id === currentUserId"
        @click="deleteProfile"
      >
        🗑️ Delete Profile
      </button>

      <!-- owner can see matches -->
      <button
        v-if="profile.user_id === currentUserId"
        @click="goToMatches"
      >
        🤝 Match Me
      </button>
    </div>

    <div v-else>
      Loading…
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/services/api'

const route         = useRoute()
const router        = useRouter()
const profile       = ref(null)
const currentUserId = Number(localStorage.getItem('user_id'))

// load profile on mount
onMounted(async () => {
  try {
    const { data } = await api.get(`/profiles/${route.params.id}`)
    profile.value = data
  } catch (err) {
    console.error('Error loading profile:', err)
  }
})

// add to favourites then go to Reports
async function addFavourite(id) {
  try {
    await api.post(`/profiles/${id}/favourite`)
    router.push({ name: 'Reports' })
  } catch (err) {
    console.error('Error adding favourite:', err)
  }
}

// delete own profile
async function deleteProfile() {
  if (!confirm('Are you sure you want to delete this profile?')) return
  try {
    await api.delete(`/profiles/${route.params.id}`)
    router.push({ name: 'Home' })
  } catch (err) {
    console.error('Delete failed:', err)
  }
}

// navigate to MatchesView
function goToMatches() {
  router.push({ name: 'Matches', params: { id: profile.value.id } })
}
</script>

<style scoped>
.profile-photo {
  max-width: 250px;
  border-radius: 4px;
  margin-bottom: 1rem;
}
.profile-detail p {
  margin: 0.25rem 0;
}
button {
  margin-right: 0.5rem;
  padding: 0.4rem 0.8rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
button:hover {
  opacity: 0.9;
}
</style>
