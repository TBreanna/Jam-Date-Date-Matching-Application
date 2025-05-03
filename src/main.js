// src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// import the global stylesheet
import './assets/global.css'

createApp(App)
  .use(router)
  .mount('#app')
