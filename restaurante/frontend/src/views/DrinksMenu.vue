<template>
  <div class="drinks-menu bg-cream min-h-screen py-12">
    <div class="container mx-auto px-6">
      <div class="flex justify-between items-center mb-10">
        <h1 class="section-heading">Drinks Menu</h1>
        <router-link to="/menu" class="text-burgundy hover:text-gold transition-colors">
          &larr; Back to Menu
        </router-link>
      </div>

      <!-- Search and Filters -->
      <div class="mb-12 bg-pearl p-6 rounded-lg shadow-md">
        <div class="flex flex-col md:flex-row gap-4 items-end mb-6">
          <div class="flex-grow">
            <label for="search" class="block text-charcoal mb-2">Search Drinks</label>
            <input 
              type="text" 
              id="search" 
              v-model="searchQuery" 
              @input="handleSearchInput"
              placeholder="Enter drink name..." 
              class="w-full px-4 py-2 border border-slate rounded-md focus:outline-none focus:ring-2 focus:ring-gold"
            >
          </div>
          <div class="w-full md:w-1/3">
            <label for="category" class="block text-charcoal mb-2">Filter by Category</label>
            <select 
              id="category" 
              v-model="selectedCategory" 
              @change="handleCategoryChange"
              class="w-full px-4 py-2 border border-slate rounded-md focus:outline-none focus:ring-2 focus:ring-gold bg-white"
            >
              <option value="">All Categories</option>
              <option v-for="category in categories" :key="category.strCategory" :value="category.strCategory">
                {{ category.strCategory }}
              </option>
            </select>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center items-center py-20">
        <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-burgundy"></div>
      </div>

      <!-- No Results Message -->
      <div v-else-if="drinks.length === 0" class="text-center py-16">
        <p class="text-xl text-charcoal">No drinks found. Try a different search term or category.</p>
      </div>

      <!-- Results Grid -->
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
        <div 
          v-for="drink in drinks" 
          :key="drink.idDrink" 
          class="bg-pearl rounded-lg overflow-hidden shadow-md hover:shadow-lg transition-shadow cursor-pointer group"
          @click="showDrinkDetails(drink.idDrink)"
        >
          <div class="relative h-48 overflow-hidden">
            <img 
              :src="drink.strDrinkThumb" 
              :alt="drink.strDrink" 
              class="w-full h-full object-cover transform group-hover:scale-105 transition-transform duration-300"
            >
            <div class="absolute inset-0 bg-burgundy bg-opacity-0 group-hover:bg-opacity-30 transition-all duration-300"></div>
          </div>
          <div class="p-4">
            <h3 class="text-burgundy font-serif text-xl mb-2 group-hover:text-gold transition-colors">{{ drink.strDrink }}</h3>
            <div class="flex justify-between items-center">
              <span class="text-sm text-slate">{{ drink.strCategory || selectedCategory }}</span>
              <span class="text-gold">&rarr;</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Drink Details Modal -->
      <div v-if="selectedDrink" class="fixed inset-0 bg-charcoal bg-opacity-80 flex items-center justify-center z-50 p-4">
        <div class="bg-cream rounded-lg max-w-3xl w-full max-h-[90vh] overflow-y-auto">
          <div class="relative">
            <button 
              @click="selectedDrink = null" 
              class="absolute top-4 right-4 bg-burgundy text-cream w-8 h-8 rounded-full flex items-center justify-center hover:bg-gold transition-colors"
            >
              &times;
            </button>
            <img 
              :src="selectedDrink.strDrinkThumb" 
              :alt="selectedDrink.strDrink" 
              class="w-full h-64 object-cover"
            >
          </div>
          <div class="p-6">
            <h2 class="text-3xl font-serif text-burgundy mb-2">{{ selectedDrink.strDrink }}</h2>
            <div class="flex flex-wrap gap-2 mb-4">
              <span class="bg-gold bg-opacity-20 text-burgundy px-3 py-1 rounded-full text-sm">
                {{ selectedDrink.strCategory }}
              </span>
              <span v-if="selectedDrink.strAlcoholic" class="bg-burgundy bg-opacity-10 text-burgundy px-3 py-1 rounded-full text-sm">
                {{ selectedDrink.strAlcoholic }}
              </span>
              <span v-if="selectedDrink.strGlass" class="bg-wood bg-opacity-10 text-wood px-3 py-1 rounded-full text-sm">
                {{ selectedDrink.strGlass }}
              </span>
            </div>
            
            <h3 class="text-xl text-wood mb-2 mt-6">Ingredients</h3>
            <ul class="grid grid-cols-1 md:grid-cols-2 gap-2 mb-6">
              <li v-for="(ingredient, index) in getDrinkIngredients(selectedDrink)" :key="index" class="flex items-center">
                <span class="text-gold mr-2">•</span>
                {{ ingredient.measure }} {{ ingredient.name }}
              </li>
            </ul>

            <h3 class="text-xl text-wood mb-2">Instructions</h3>
            <p class="text-charcoal whitespace-pre-line">{{ selectedDrink.strInstructions }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import MenuService from '../services/menu.service';

// State
const searchQuery = ref('');
const selectedCategory = ref('');
const categories = ref([]);
const drinks = ref([]);
const loading = ref(true);
const selectedDrink = ref(null);
const searchTimeout = ref(null);

// Fetch categories on component mount
onMounted(async () => {
  try {
    const categoriesData = await MenuService.getDrinkCategories();
    // Format categories from the API response
    categories.value = categoriesData.map(item => {
      return { strCategory: item.strCategory };
    });
    
    // Load a default category to show some initial drinks
    if (categories.value.length > 0) {
      selectedCategory.value = categories.value[0].strCategory;
      await fetchDrinksByCategory(selectedCategory.value);
    }
  } catch (error) {
    console.error('Failed to load drink categories:', error);
  } finally {
    loading.value = false;
  }
});

// Methods
const handleSearchInput = () => {
  // Debounce search input
  clearTimeout(searchTimeout.value);
  searchTimeout.value = setTimeout(async () => {
    if (searchQuery.value.trim()) {
      loading.value = true;
      selectedCategory.value = ''; // Clear category filter when searching
      try {
        drinks.value = await MenuService.searchDrinksByName(searchQuery.value);
      } catch (error) {
        console.error('Search error:', error);
        drinks.value = [];
      } finally {
        loading.value = false;
      }
    } else if (selectedCategory.value) {
      // If search is cleared but category is selected, show category drinks
      fetchDrinksByCategory(selectedCategory.value);
    } else {
      drinks.value = [];
    }
  }, 500);
};

const handleCategoryChange = async () => {
  if (selectedCategory.value) {
    searchQuery.value = ''; // Clear search query when selecting category
    await fetchDrinksByCategory(selectedCategory.value);
  } else if (searchQuery.value.trim()) {
    // If category is cleared but search has text, perform search
    handleSearchInput();
  } else {
    drinks.value = [];
  }
};

const fetchDrinksByCategory = async (category) => {
  loading.value = true;
  try {
    drinks.value = await MenuService.getDrinksByCategory(category);
  } catch (error) {
    console.error('Failed to fetch drinks by category:', error);
    drinks.value = [];
  } finally {
    loading.value = false;
  }
};

const showDrinkDetails = async (drinkId) => {
  loading.value = true;
  try {
    const drinkDetails = await MenuService.getDrinkById(drinkId);
    selectedDrink.value = drinkDetails;
  } catch (error) {
    console.error('Failed to fetch drink details:', error);
  } finally {
    loading.value = false;
  }
};

// Helper function to extract ingredients and measures
const getDrinkIngredients = (drink) => {
  if (!drink) return [];
  
  const ingredients = [];
  for (let i = 1; i <= 15; i++) {
    const ingredient = drink[`strIngredient${i}`];
    const measure = drink[`strMeasure${i}`];
    
    if (ingredient && ingredient.trim()) {
      ingredients.push({
        name: ingredient,
        measure: measure || ''
      });
    }
  }
  
  return ingredients;
};
</script>