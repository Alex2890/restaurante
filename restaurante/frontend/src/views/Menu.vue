<template>
  <div class="menu-page bg-cream py-16 min-h-screen">
    <div class="container mx-auto px-6">
      <h1 class="section-heading mb-16">Our Menu</h1>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-10 max-w-5xl mx-auto">
        <!-- Food Menu Card -->
        <router-link to="/menu/food" class="relative rounded-lg overflow-hidden shadow-xl group cursor-pointer h-80">
          <div 
            class="absolute inset-0 bg-cover bg-center transition-transform duration-500 group-hover:scale-110"
            :style="foodCardStyle"
          >
          </div>          
          <div class="absolute inset-0 flex items-center justify-center flex-col">
            <h2 class="text-7xl font-serif text-gold font-extrabold mb-2">Food</h2>
            <p class="text-xl text-white font-extrabold">Discover our exquisite dishes</p>
            <div class="mt-6 border-b-2 border-gold w-12 group-hover:w-24 transition-all duration-300"></div>
          </div>
        </router-link>
        
        <!-- Drinks Menu Card -->
        <router-link to="/menu/drinks" class="relative rounded-lg overflow-hidden shadow-xl group cursor-pointer h-80">
          <div 
            class="absolute inset-0 bg-cover bg-center transition-transform duration-500 group-hover:scale-110"
            :style="drinkCardStyle"
          >
          </div>          
          <div class="absolute inset-0 flex items-center justify-center flex-col">
            <h2 class="text-7xl font-serif text-gold font-extrabold mb-2">Drinks</h2>
            <p class="text-xl text-white font-extrabold">Explore our signature drinks</p>
            <div class="mt-6 border-b-2 border-gold w-12 group-hover:w-24 transition-all duration-300"></div>
          </div>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import foodCard from '@/assets/images/foodCard.jpg';
import drinkCard from '@/assets/images/drinkCard.jpg';

const foodCardStyle = `background-image: url('${foodCard}'); background-size: cover; background-position: center;`;
const drinkCardStyle = `background-image: url('${drinkCard}'); background-size: cover; background-position: center;`;
</script>