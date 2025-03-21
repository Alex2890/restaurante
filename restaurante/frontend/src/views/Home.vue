<template>
  <div class="home">
    <section class="hero">
      <div class="hero-content">
        <h1>Fine Dining Experience</h1>
        <p>Experience the epitome of culinary excellence</p>
        <div class="cta-buttons">
          <router-link to="/menu" class="btn btn-primary">View Menu</router-link>
          <router-link to="/reservations" class="btn btn-secondary">Make Reservation</router-link>
        </div>
      </div>
    </section>

    <section class="featured">
      <h2>Featured Dishes</h2>
      <div class="dishes">
        <div class="dish-card" v-for="dish in featuredDishes" :key="dish.id">
          <div class="dish-image"><!-- Image will be added later --></div>
          <div class="dish-info">
            <h3>{{ dish.name }}</h3>
            <p>{{ dish.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <section class="about-preview">
      <h2>About Our Restaurant</h2>
      <p>Founded on the principles of exceptional quality and impeccable service, our restaurant brings together the finest ingredients and culinary expertise to create memorable dining experiences.</p>
      <router-link to="/about" class="learn-more">Learn More</router-link>
    </section>

    <section class="testimonials">
      <h2>What Our Guests Say</h2>
      <div class="testimonial-slider">
        <div class="testimonial" v-for="testimonial in testimonials" :key="testimonial.id">
          <p class="quote">{{ testimonial.quote }}</p>
          <p class="author">- {{ testimonial.author }}</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue';

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