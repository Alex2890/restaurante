<template>
  <header class="bg-burgundy shadow-lg">
    <div class="container mx-auto px-6 py-5">
      <div class="flex items-center justify-between">
        <div class="text-4xl font-bold tracking-wide font-brand">
          <span class="text-gold">Noir</span>
          <span class="text-gold"> Et</span>
          <span class="text-cream"> Or</span>
        </div>
        
        <!-- Desktop Navigation -->
        <nav class="hidden md:flex space-x-12">
          <router-link 
            v-for="route in routes" 
            :key="route.path" 
            :to="route.path" 
            class="text-cream hover:text-gold transition duration-300 font-nav text-xl tracking-wide"
            active-class="text-gold border-b-2 border-gold pb-1"
          >
            {{ route.name }}
          </router-link>
        </nav>
        
        <!-- Mobile Menu Button -->
        <div class="md:hidden">
          <button @click="toggleMobileMenu" class="text-cream hover:text-gold focus:outline-none">
            <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7"></path>
            </svg>
          </button>
        </div>
      </div>
      
      <!-- Mobile Menu -->
      <div v-if="mobileMenuOpen" class="md:hidden mt-4 pb-2 border-t border-gold pt-3">
        <router-link 
          v-for="route in routes" 
          :key="route.path" 
          :to="route.path" 
          class="block py-3 text-cream hover:text-gold transition duration-300 font-nav text-xl"
          active-class="text-gold font-bold"
          @click="mobileMenuOpen = false"
        >
          {{ route.name }}
        </router-link>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue';

const mobileMenuOpen = ref(false);

const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value;
};

// Routes definition - these should match the routes in router/routes.js
const routes = [
  { path: '/', name: 'Home' },
  { path: '/menu', name: 'Menu' },
  { path: '/reservations', name: 'Reservations' },
  { path: '/about', name: 'About' },
  { path: '/contact', name: 'Contact' }
];
</script>