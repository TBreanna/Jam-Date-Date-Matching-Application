// src/services/api.js
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL  // e.g. "http://localhost:5001/api"
})

// Automatically attach JWT from localStorage to every request
api.interceptors.request.use(config => {
  const token = localStorage.getItem('jwt')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
}, error => Promise.reject(error))

export default api
