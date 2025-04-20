import { createRouter, createWebHistory } from 'vue-router'
import DefaultLayout from '@/layouts/default.vue'
import EmptyLayout from '@/layouts/empty.vue'
import VeteranPage from '@/views/home/VeteranPage.vue'
import VolunteerPage from '@/views/home/VolunteerPage.vue'
import LoginPage from '@/views/auth/LoginPage.vue'
import RegisterPage from '@/views/auth/RegisterPage.vue'

const routes = [
  {
    path: '/',
    redirect: '/auth/login',
  },
  {
    path: '/home',
    component: DefaultLayout,
    children: [
      {
        path: 'veteran',
        name: 'VeteranPage',
        component: VeteranPage,
        meta: { requiresAuth: true },
      },
      {
        path: 'volunteer',
        name: 'VolunteerPage',
        component: VolunteerPage,
        meta: { requiresAuth: true },
      },
    ],
  },
  {
    path: '/auth',
    component: EmptyLayout,
    children: [
      {
        path: 'login',
        name: 'Login',
        component: LoginPage,
      },
      {
        path: 'register',
        name: 'Register',
        component: RegisterPage,
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router
