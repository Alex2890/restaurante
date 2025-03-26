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
        
        <!-- Loading State -->
        <div v-if="loading" class="flex justify-center items-center py-20">
          <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-burgundy"></div>
        </div>
        
        <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-10">
          <div 
            class="dish-card bg-pearl rounded-lg shadow-lg overflow-hidden transform hover:-translate-y-1 transition-all duration-300 hover:shadow-xl" 
            v-for="dish in featuredDishes" 
            :key="dish.idMeal"
          >
            <div class="h-64 relative overflow-hidden group">
              <img 
                :src="dish.strMealThumb" 
                :alt="dish.strMeal" 
                class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
              >
              <div class="absolute inset-0  bg-opacity-0 group-hover:bg-opacity-30 transition-all duration-300 flex items-center justify-center">
                <div class="scale-0 group-hover:scale-100 transition-transform duration-300">
                  <div class="bg-gold text-burgundy px-4 py-2 rounded-sm font-bold transform rotate-0">
                    {{ dish.strCategory }}
                  </div>
                </div>
              </div>
            </div>
            <div class="p-6">
              <h3 class="text-2xl font-serif text-burgundy mb-3 font-subheading">{{ dish.strMeal }}</h3>
              <p class="text-charcoal line-clamp-3 mb-4">
                {{ dish.strInstructions ? dish.strInstructions.slice(0, 120) + '...' : 'A delectable dish prepared with the finest ingredients.' }}
              </p>
              <div class="flex flex-wrap gap-2 mb-4">
                <span v-if="dish.strArea" class="text-sm text-slate italic">{{ dish.strArea }} Cuisine</span>
                <span v-if="dish.strTags" class="text-sm text-slate italic">• {{ dish.strTags }}</span>
              </div>
              <div class="mt-4 text-center">
                <router-link 
                  :to="'/menu/food'" 
                  class="inline-block px-4 py-2 border border-gold text-gold hover:bg-gold hover:text-burgundy font-bold transition-colors duration-300 rounded-sm"
                >
                  View Recipe &rarr;
                </router-link>
              </div>
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
import { ref, onMounted } from 'vue';
import heroImage from '@/assets/images/hero-image.jpg';
import MenuService from '../services/menu.service';

const backgroundImage = `background-image: url('${heroImage}'); background-size: cover; background-position: center;`;

const featuredDishes = ref([]);
const loading = ref(true);

// Function to fetch random meals
async function fetchRandomMeals() {
  loading.value = true;
  try {
    // Fetch a few random categories
    const categories = await MenuService.getMealCategories();
    let randomMeals = [];
    
    if (categories && categories.length > 0) {
      // Create an array of promises for fetching meals from random categories
      const fetchPromises = [];
      const randomCats = [...categories].sort(() => 0.5 - Math.random()).slice(0, 3);
      
      for (const category of randomCats) {
        fetchPromises.push(MenuService.getMealsByCategory(category.strCategory));
      }
      
      // Wait for all promises to resolve
      const results = await Promise.all(fetchPromises);
      
      // Process the results to get one random meal from each category
      for (const categoryMeals of results) {
        if (categoryMeals && categoryMeals.length > 0) {
          // Get a random meal from this category
          const randomMeal = categoryMeals[Math.floor(Math.random() * categoryMeals.length)];
          // Fetch full meal details to get more information
          const mealDetails = await MenuService.getMealById(randomMeal.idMeal);
          if (mealDetails) {
            randomMeals.push(mealDetails);
          }
          
          // If we have 3 meals, stop fetching
          if (randomMeals.length >= 3) {
            break;
          }
        }
      }
    }
    
    // If we couldn't get 3 meals from the categories, fall back to other categories
    if (randomMeals.length < 3) {
      // Try to fetch meals from other categories
      const remainingCategories = categories.filter(cat => 
        !randomMeals.some(meal => meal.strCategory === cat.strCategory)
      );
      
      for (let i = 0; randomMeals.length < 3 && i < remainingCategories.length; i++) {
        const categoryMeals = await MenuService.getMealsByCategory(remainingCategories[i].strCategory);
        if (categoryMeals && categoryMeals.length > 0) {
          const randomMeal = categoryMeals[Math.floor(Math.random() * categoryMeals.length)];
          const mealDetails = await MenuService.getMealById(randomMeal.idMeal);
          if (mealDetails && !randomMeals.some(meal => meal.idMeal === mealDetails.idMeal)) {
            randomMeals.push(mealDetails);
          }
        }
      }
    }
    
    // Update the featuredDishes with our random meals
    featuredDishes.value = randomMeals.slice(0, 3);
  } catch (error) {
    console.error('Error fetching random meals:', error);
    // Fallback to static data if API fails
    featuredDishes.value = [
      {
        idMeal: '1',
        strMeal: 'Truffle Risotto',
        strCategory: 'Italian',
        strMealThumb: 'https://www.themealdb.com/images/media/meals/wssvvs1511785879.jpg'
      },
      {
        idMeal: '2',
        strMeal: 'Seared Scallops',
        strCategory: 'Seafood',
        strMealThumb: 'https://www.themealdb.com/images/media/meals/rqtxvr1511792990.jpg'
      },
      {
        idMeal: '3',
        strMeal: 'Filet Mignon',
        strCategory: 'Beef',
        strMealThumb: 'https://www.themealdb.com/images/media/meals/1520084413.jpg'
      }
    ];
  } finally {
    loading.value = false;
  }
}

// Fetch random meals when component is mounted
onMounted(() => {
  fetchRandomMeals();
});

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
/* Additional utilities not provided by default in TailwindCSS */
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.dish-card {
  height: fit-content;
  display: flex;
  flex-direction: column;
}

.dish-card .p-6 {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.dish-card .text-center {
  margin-top: auto;
}
</style>