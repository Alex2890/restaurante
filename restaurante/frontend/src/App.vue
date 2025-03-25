<template>
  <div class="app min-h-screen flex flex-col">
    <Navbar />
    <main class="flex-grow">
      <router-view />
    </main>
    <footer class="bg-burgundy text-cream py-6">
      <div class="container mx-auto px-6 text-center">
        <p>&copy; {{ new Date().getFullYear() }} <span class="text-gold">Noir Et Or</span>. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import Navbar from './components/Navbar.vue';
</script>