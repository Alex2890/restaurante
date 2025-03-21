<template>
  <div class="login-page">
    <div class="login-container">
      <h1>Sign In</h1>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="email">Email</label>
          <input 
            id="email" 
            v-model="form.email" 
            type="email" 
            required
            placeholder="Your email address"
          >
        </div>
        
        <div class="form-group">
          <label for="password">Password</label>
          <input 
            id="password" 
            v-model="form.password" 
            type="password" 
            required
            placeholder="Your password"
          >
        </div>
        
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
        
        <button type="submit" class="submit-btn" :disabled="loading">
          {{ loading ? 'Signing in...' : 'Sign In' }}
        </button>
        
        <div class="divider">or</div>
        
        <GoogleLogin :callback="handleGoogleLogin" />
        
        <p class="register-link">
          Don't have an account? <router-link to="/register">Register</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import { GoogleLogin } from 'vue3-google-login';

const router = useRouter();
const authStore = useAuthStore();

const form = ref({
  email: '',
  password: ''
});

const loading = ref(false);
const error = ref('');

async function handleLogin() {
  loading.value = true;
  error.value = '';
  
  try {
    const success = await authStore.login({
      email: form.value.email,
      password: form.value.password
    });
    
    if (success) {
      router.push('/');
    }
  } catch (err) {
    error.value = 'Invalid email or password';
  } finally {
    loading.value = false;
  }
}

async function handleGoogleLogin(response) {
  loading.value = true;
  error.value = '';
  
  try {
    const success = await authStore.loginWithGoogle(response);
    
    if (success) {
      router.push('/');
    }
  } catch (err) {
    error.value = 'Google login failed. Please try again.';
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
/* Styling will be enhanced with TailwindCSS */
</style>