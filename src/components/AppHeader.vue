<template>
  <header>
    <h1>Jam-Date</h1>
    <p>Total profiles: {{ profiles.length }}</p>
  </header>
</template>

<script>
import api from '@/services/api'   // uses your alias

export default {
  name: 'AppHeader',
  data() {
    return { profiles: [] }
  },
  async created() {
    try {
      const res = await api.get('/profiles')
      this.profiles = res.data
    } catch (err) {
      console.error('Failed to load profiles:', err)
    }
  }
}
</script>
