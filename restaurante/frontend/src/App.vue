<template>
  <div class="app min-h-screen flex flex-col">
    <Navbar />
    <main class="flex-grow">
      <router-view />
    </main>
    <footer class="bg-gray-800 text-white py-6">
      <div class="container mx-auto px-6 text-center">
        <p>&copy; {{ new Date().getFullYear() }} Fine Dining Restaurant. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import Navbar from './components/Navbar.vue';
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Lato:wght@300;400;500;700&display=swap');

.font-serif {
  font-family: 'Playfair Display', serif;
}

body {
  font-family: 'Lato', sans-serif;
}
</style>