<template>
  <div class="home">
    <!-- Hero Section with Background Image -->
    <section class="relative h-screen flex items-center justify-center" :style="backgroundImage">
      
      <!-- Hero Content -->
      <div class="relative z-10 text-center px-6 max-w-4xl">
        <h1 class="text-5xl md:text-7xl font-serif text-cream mb-6 tracking-wider">Fine Dining Experience</h1>
        <p class="text-xl md:text-2xl text-pearl mb-10">Experience the epitome of culinary excellence</p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <router-link to="/menu" class="btn-primary">View Menu</router-link>
          <router-link to="/reservations" class="btn-secondary">Make Reservation</router-link>
        </div>
      </div>
    </section>

    <!-- Featured Dishes Section -->
    <section class="py-20 px-6 bg-cream">
      <div class="container mx-auto max-w-6xl">
        <h2 class="section-heading">Featured Dishes</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-10">
          <div class="dish-card bg-pearl rounded-lg shadow-md overflow-hidden" v-for="dish in featuredDishes" :key="dish.id">
            <div class="h-64 bg-slate bg-opacity-10 relative">
              <!-- Placeholder for dish image, to be replaced with actual images -->
              <div class="absolute inset-0 flex items-center justify-center text-slate">
                <span class="text-sm">Image coming soon</span>
              </div>
            </div>
            <div class="p-6">
              <h3 class="text-2xl font-serif text-burgundy mb-3">{{ dish.name }}</h3>
              <p class="text-charcoal">{{ dish.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- About Section -->
    <section class="py-20 px-6 bg-wood text-cream">
      <div class="container mx-auto max-w-4xl text-center">
        <h2 class="text-4xl font-serif mb-8 text-gold">About Us</h2>
        <p class="text-xl leading-relaxed mb-10">
          Nestled in the heart of the city, our restaurant celebrates the art of fine dining through a seamless fusion of tradition and innovation. We meticulously source exceptional ingredients from local artisans and farmers, transforming them with precise technique and creative vision. Each plate tells a story of passion, craftsmanship, and our unwavering commitment to creating transcendent culinary moments that linger in memory long after the final course.
        </p>
        <router-link to="/about" class="inline-block border-b-2 border-gold text-lg text-gold hover:text-cream transition duration-300">
          Learn More
        </router-link>
      </div>
    </section>

    <!-- Testimonials Section -->
    <section class="py-20 px-6 bg-pearl">
      <div class="container mx-auto max-w-6xl">
        <h2 class="section-heading">What Our Guests Say</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="bg-cream p-8 rounded-lg shadow-md" v-for="testimonial in testimonials" :key="testimonial.id">
            <div class="mb-6 text-gold">
              <!-- Star Icons -->
              <div class="flex">
                <svg v-for="i in 5" :key="i" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 fill-current" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118l-2.8-2.034c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
              </div>
            </div>
            <p class="text-charcoal italic mb-4 leading-relaxed">{{ testimonial.quote }}</p>
            <p class="text-burgundy font-semibold">{{ testimonial.author }}</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import heroImage from '@/assets/images/hero-image.jpg';

const backgroundImage = `background-image: url('${heroImage}'); background-size: cover; background-position: center;`;

const featuredDishes = ref([
  {
    id: 1,
    name: 'Truffle Risotto',
    description: 'Creamy risotto infused with black truffle and aged parmesan.'
  },
  {
    id: 2,
    name: 'Seared Scallops',
    description: 'Pan-seared scallops with citrus reduction and micro greens.'
  },
  {
    id: 3,
    name: 'Filet Mignon',
    description: 'Prime cut filet with red wine reduction and truffle butter.'
  }
]);

const testimonials = ref([
  {
    id: 1,
    quote: 'The most exquisite dining experience I have had in years. Every dish was a masterpiece.',
    author: 'James Williams'
  },
  {
    id: 2,
    quote: "Impeccable service and atmosphere. The chef's tasting menu is a journey worth taking.",
    author: 'Emily Thompson'
  },
  {
    id: 3,
    quote: 'From the moment we walked in, we knew we were in for something special. Will definitely return.',
    author: 'Robert Chen'
  }
]);
</script>

<style scoped>
/* Styling will be enhanced with TailwindCSS */
</style>