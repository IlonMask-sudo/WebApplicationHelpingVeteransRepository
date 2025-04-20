import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const isAuthenticated = ref(false)

  // Логин волонтера (заглушка)
  const loginVolunteer = async (email, password) => {
    user.value = { email, role: 'volunteer' }
    isAuthenticated.value = true
    return true
  }

  // Логин ветерана (заглушка)
  const loginVeteran = async (email, password) => {
    user.value = { email, role: 'veteran' }
    isAuthenticated.value = true
    return true
  }

  const register = async (userData) => {
    // Здесь должна быть реализация API-запроса
    // Временная заглушка:
    return new Promise((resolve) => {
      setTimeout(() => {
        user.value = userData
        isAuthenticated.value = true
        resolve(true)
      }, 1000)
    })
  }

  // Выход
  const logout = () => {
    user.value = null
    isAuthenticated.value = false
  }

  return {
    user,
    isAuthenticated,
    loginVolunteer,
    loginVeteran,
    register,
    logout,
  }
})
