<template>
  <div class="create-profile container">
    <h2>New Profile</h2>
    <form @submit.prevent="submitProfile" enctype="multipart/form-data">
      <div><label>Description</label>
        <input v-model="form.description" required />
      </div>
      <div><label>Parish</label>
        <input v-model="form.parish" required />
      </div>
      <div><label>Biography</label>
        <textarea v-model="form.biography" required/>
      </div>
      <div><label>Sex</label>
        <input v-model="form.sex" required/>
      </div>
      <div><label>Race</label>
        <input v-model="form.race" required/>
      </div>
      <div><label>Birth Year</label>
        <input v-model.number="form.birth_year" type="number" required/>
      </div>
      <div><label>Height</label>
        <input v-model.number="form.height" type="number" required/>
      </div>
      <div><label>Favorite Cuisine</label>
        <input v-model="form.fav_cuisine" />
      </div>
      <div><label>Favorite Colour</label>
        <input v-model="form.fav_colour" />
      </div>
      <div><label>Favorite School Subject</label>
        <input v-model="form.fav_school_subject" />
      </div>
      <div>
        <label><input type="checkbox" v-model="form.political" /> Political</label>
        <label><input type="checkbox" v-model="form.religious" /> Religious</label>
        <label><input type="checkbox" v-model="form.family_oriented" /> Family Oriented</label>
      </div>
      <div>
        <label>Photo</label>
        <input type="file" @change="onFileChange" />
      </div>
      <button type="submit">Create Profile</button>
    </form>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'

const router = useRouter()
const form = reactive({
  description: '',
  parish: '',
  biography: '',
  sex: '',
  race: '',
  birth_year: null,
  height: null,
  fav_cuisine: '',
  fav_colour: '',
  fav_school_subject: '',
  political: false,
  religious: false,
  family_oriented: false
})
const file = ref(null)

function onFileChange(e) {
  file.value = e.target.files[0]
}

async function submitProfile() {
  const fd = new FormData()
  Object.entries(form).forEach(([k,v]) => fd.append(k, v))
  if (file.value) fd.append('photo', file.value)

  try {
    await api.post('/profiles', fd, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    router.push('/')
  } catch (err) {
    console.error('Create profile failed:', err)
  }
}
</script>

<style scoped>
.create-profile { padding: 2rem; }
.create-profile div { margin-bottom: 1rem; }
</style>
