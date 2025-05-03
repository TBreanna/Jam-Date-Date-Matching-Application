import { createRouter, createWebHistory } from 'vue-router'
import Home          from '@/views/Home.vue'
import Register      from '@/views/Register.vue'
import Login         from '@/views/Login.vue'
import CreateProfile from '@/views/CreateProfile.vue'
import ProfileView   from '@/views/Profile.vue'
import Reports       from '@/views/Reports.vue'
import LogoutView    from '@/views/LogoutView.vue'

const routes = [
  { path: '/',                   name: 'Home',           component: Home },
  { path: '/register',           name: 'Register',       component: Register },
  { path: '/login',              name: 'Login',          component: Login },
  { path: '/profiles/new',       name: 'CreateProfile',  component: CreateProfile },
  { path: '/profiles/:id',       name: 'ProfileView',    component: ProfileView, props: true },
  { path: '/profiles/favourites',name: 'Reports',        component: Reports },
  { path: '/logoutView',         name: 'LogoutView',     component: LogoutView },
]

export default createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})
