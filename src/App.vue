<template>
  <div id="app">
    <nav class="navbar">
      <!-- left side: links -->
      <div class="nav-links">
        <router-link to="/">Home</router-link>
        <router-link to="/register">Register</router-link>
        <router-link to="/login">Login</router-link>
        <router-link to="/profiles/new">New Profile</router-link>
        <router-link to="/profiles/favourites">Reports</router-link>
        <router-link to="/logout">Logout</router-link>
      </div>
      <!-- right side: theme switch + flag + title -->
      <div class="nav-controls">
        <button class="theme-switch" @click="toggleTheme">
          {{ isDark ? '☀️ Light' : '🌙 Dark' }}
        </button>
        <div class="brand">
          <img :src="flag" alt="Jamaican Flag" class="flag" />
          <div class="app-title">Jam-Date</div>
        </div>
      </div>
    </nav>

    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
// adjust this to your actual path or alias
import flag from '/Users/Cley/Downloads/1/info3180-vuejs-flask working app/src/assets/jm.png'

const isDark = ref(false)

onMounted(() => {
  const saved = localStorage.getItem('theme')
  if (saved) isDark.value = saved === 'dark'
  else isDark.value = window.matchMedia('(prefers-color-scheme: dark)').matches
  applyTheme()
})

watch(isDark, () => {
  applyTheme()
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
})

function applyTheme() {
  document.body.classList.toggle('dark', isDark.value)
}

function toggleTheme() {
  isDark.value = !isDark.value
}
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 1rem;
  background: var(--bg);
  border-bottom: 1px solid #ccc;
}

.nav-links a {
  margin-right: 1rem;
  text-decoration: none;
}
.nav-links a.router-link-active {
  font-weight: bold;
  text-decoration: underline;
}

.nav-controls {
  display: flex;
  align-items: center;
}

/* Brand block: stack flag + title */
.brand {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-left: 0.5rem;
}

.flag {
  height: 24px;
  width: auto;
  border-radius: 2px;
}

/* Gradient text for “Jam-Date” */
.app-title {
  margin-top: 0.25rem;
  font-size: 1rem;
  font-weight: bold;
  /* black → green → gold */
  background: linear-gradient(
    to right,
    #000000 0%,
    #009b3a 50%,
    #ffd100 100%
  );
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  /* smooth fade if theme toggles */
  transition: background var(--transition-smooth);
}

.theme-switch {
  background: transparent;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  margin-right: 0.5rem;
}

.main-content {
  padding: 2rem;
}
</style>
