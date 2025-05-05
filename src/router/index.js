// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import Home            from '@/views/Home.vue'
import Register        from '@/views/Register.vue'
import Login           from '@/views/Login.vue'
import CreateProfile   from '@/views/CreateProfile.vue'
import ProfileView     from '@/views/Profile.vue'
import MatchesView     from '@/views/MatchesView.vue'
import Reports         from '@/views/Reports.vue'
import MessageView     from '@/views/MessageView.vue'
import LogoutView      from '@/views/LogoutView.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { requiresAuth: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/profiles/new',
    name: 'CreateProfile',
    component: CreateProfile,
    meta: { requiresAuth: true }
  },
  {
    path: '/profiles/:id',
    name: 'ProfileView',
    component: ProfileView,
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/profiles/:id/matches',
    name: 'Matches',
    component: MatchesView,
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/profiles/favourites',
    name: 'Reports',
    component: Reports,
    meta: { requiresAuth: true }
  },
  {
    path: '/messages/:id',
    name: 'Messages',
    component: MessageView,
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/logout',
    name: 'Logout',
    component: LogoutView
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// redirect to /login if a protected page is accessed without a token
router.beforeEach((to, from, next) => {
  const requiresAuth = to.meta.requiresAuth
  const token        = localStorage.getItem('jwt')
  if (requiresAuth && !token) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
  } else {
    next()
  }
})

export default router
