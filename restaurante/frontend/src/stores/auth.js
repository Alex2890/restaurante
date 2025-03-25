import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import AuthService from '../services/auth.service'
import { jwtDecode } from 'jwt-decode';

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || null)
  const user = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const isAuthenticated = computed(() => !!token.value)
  
  // Initialize user from token if exists
  if (token.value) {
    try {
      user.value = jwtDecode(token.value)
    } catch (err) {
      // Invalid token
      token.value = null
      localStorage.removeItem('token')
    }
  }

  async function login(credentials) {
    loading.value = true
    error.value = null
    try {
      const response = await AuthService.login(credentials)
      token.value = response.token
      user.value = jwtDecode(response.token)
      localStorage.setItem('token', response.token)
      return true
    } catch (err) {
      error.value = err.response?.data?.message || 'Authentication failed'
      return false
    } finally {
      loading.value = false
    }
  }

  async function loginWithGoogle(googleUser) {
    loading.value = true
    error.value = null
    try {
      const response = await AuthService.googleLogin(googleUser)
      token.value = response.token
      user.value = jwtDecode(response.token)
      localStorage.setItem('token', response.token)
      return true
    } catch (err) {
      error.value = err.response?.data?.message || 'Google authentication failed'
      return false
    } finally {
      loading.value = false
    }
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
  }

  return {
    token,
    user,
    loading,
    error,
    isAuthenticated,
    login,
    loginWithGoogle,
    logout
  }
})