<template>
  <div class="menu-page bg-cream py-16 min-h-screen">
    <div class="container mx-auto px-6">
      <h1 class="section-heading mb-16">Our Menu</h1>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-10 max-w-5xl mx-auto">
        <!-- Food Menu Card -->
        <router-link to="/menu/food" class="relative rounded-lg overflow-hidden shadow-xl group cursor-pointer h-80">
          <div 
            class="absolute inset-0 bg-cover bg-center transition-transform duration-500 group-hover:scale-110"
            style="background-image: url('https://images.unsplash.com/photo-1514326640560-7d063ef2aed5?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80');"
          ></div>
          <div class="absolute inset-0 bg-burgundy bg-opacity-60 group-hover:bg-opacity-70 transition-all duration-300"></div>
          <div class="absolute inset-0 flex items-center justify-center flex-col">
            <h2 class="text-4xl font-serif text-gold mb-2">Food</h2>
            <p class="text-cream">Discover our exquisite dishes</p>
            <div class="mt-6 border-b-2 border-gold w-12 group-hover:w-24 transition-all duration-300"></div>
          </div>
        </router-link>
        
        <!-- Drinks Menu Card -->
        <router-link to="/menu/drinks" class="relative rounded-lg overflow-hidden shadow-xl group cursor-pointer h-80">
          <div 
            class="absolute inset-0 bg-cover bg-center transition-transform duration-500 group-hover:scale-110"
            style="background-image: url('https://images.unsplash.com/photo-1470337458703-46ad1756a187?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80');"
          ></div>
          <div class="absolute inset-0 bg-burgundy bg-opacity-60 group-hover:bg-opacity-70 transition-all duration-300"></div>
          <div class="absolute inset-0 flex items-center justify-center flex-col">
            <h2 class="text-4xl font-serif text-gold mb-2">Drinks</h2>
            <p class="text-cream">Explore our signature drinks</p>
            <div class="mt-6 border-b-2 border-gold w-12 group-hover:w-24 transition-all duration-300"></div>
          </div>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
// Main menu page - selection between food and drinks
</script>