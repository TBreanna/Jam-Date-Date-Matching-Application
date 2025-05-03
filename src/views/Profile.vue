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
      <p>
        <strong>Political:</strong>
        <span>{{ profile.political ? 'Yes' : 'No' }}</span>
      </p>
      <p>
        <strong>Religious:</strong>
        <span>{{ profile.religious ? 'Yes' : 'No' }}</span>
      </p>
      <p>
        <strong>Family Oriented:</strong>
        <span>{{ profile.family_oriented ? 'Yes' : 'No' }}</span>
      </p>
      <button @click="addFavourite(profile.id)">
        ❤️ Add to Favourites
      </button>
    </div>
    <div v-else>
      Loading…
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute }       from 'vue-router'
import api                 from '@/services/api'

const route   = useRoute()
const profile = ref(null)

onMounted(async () => {
  try {
    const { data } = await api.get(`/profiles/${route.params.id}`)
    profile.value = data
  } catch (err) {
    console.error('Error loading profile:', err)
  }
})

async function addFavourite(id) {
  try {
    await api.post(`/profiles/${id}/favourite`)
    alert('Added to favourites!')
  } catch (err) {
    console.error('Error adding favourite:', err)
  }
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
</style>
