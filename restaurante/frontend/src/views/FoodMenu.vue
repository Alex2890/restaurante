<template>
  <div class="food-menu bg-cream min-h-screen py-12">
    <div class="container mx-auto px-6">
      <div class="flex justify-between items-center mb-10">
        <h1 class="section-heading">Food Menu</h1>
        <router-link to="/menu" class="text-burgundy hover:text-gold transition-colors">
          &larr; Back to Menu
        </router-link>
      </div>

      <!-- Search and Filters -->
      <div class="mb-12 bg-pearl p-6 rounded-lg shadow-md">
        <div class="flex flex-col md:flex-row gap-4 items-end mb-6">
          <div class="flex-grow">
            <label for="search" class="block text-charcoal mb-2">Search Meals</label>
            <input 
              type="text" 
              id="search" 
              v-model="searchQuery" 
              @input="handleSearchInput"
              placeholder="Enter meal name..." 
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
      <div v-else-if="meals.length === 0" class="text-center py-16">
        <p class="text-xl text-charcoal">No meals found. Try a different search term or category.</p>
      </div>

      <!-- Results Grid -->
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
        <div 
          v-for="meal in meals" 
          :key="meal.idMeal" 
          class="bg-pearl rounded-lg overflow-hidden shadow-md hover:shadow-lg transition-shadow cursor-pointer group"
          @click="showMealDetails(meal.idMeal)"
        >
          <div class="relative h-48 overflow-hidden">
            <img 
              :src="meal.strMealThumb" 
              :alt="meal.strMeal" 
              class="w-full h-full object-cover transform group-hover:scale-105 transition-transform duration-300"
            >
            <div class="absolute inset-0 bg-burgundy bg-opacity-0 group-hover:bg-opacity-30 transition-all duration-300"></div>
          </div>
          <div class="p-4">
            <h3 class="text-burgundy font-serif text-xl mb-2 group-hover:text-gold transition-colors">{{ meal.strMeal }}</h3>
            <div class="flex justify-between items-center">
              <span class="text-sm text-slate">{{ meal.strCategory || selectedCategory }}</span>
              <span class="text-gold">&rarr;</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Meal Details Modal -->
      <div v-if="selectedMeal" class="fixed inset-0 bg-charcoal bg-opacity-80 flex items-center justify-center z-50 p-4">
        <div class="bg-cream rounded-lg max-w-3xl w-full max-h-[90vh] overflow-y-auto">
          <div class="relative">
            <button 
              @click="selectedMeal = null" 
              class="absolute top-4 right-4 bg-burgundy text-cream w-8 h-8 rounded-full flex items-center justify-center hover:bg-gold transition-colors"
            >
              &times;
            </button>
            <img 
              :src="selectedMeal.strMealThumb" 
              :alt="selectedMeal.strMeal" 
              class="w-full h-64 object-cover"
            >
          </div>
          <div class="p-6">
            <h2 class="text-3xl font-serif text-burgundy mb-2">{{ selectedMeal.strMeal }}</h2>
            <div class="flex flex-wrap gap-2 mb-4">
              <span class="bg-gold bg-opacity-20 text-burgundy px-3 py-1 rounded-full text-sm">
                {{ selectedMeal.strCategory }}
              </span>
              <span v-if="selectedMeal.strArea" class="bg-burgundy bg-opacity-10 text-burgundy px-3 py-1 rounded-full text-sm">
                {{ selectedMeal.strArea }}
              </span>
            </div>
            
            <h3 class="text-xl text-wood mb-2 mt-6">Ingredients</h3>
            <ul class="grid grid-cols-1 md:grid-cols-2 gap-2 mb-6">
              <li v-for="(ingredient, index) in getMealIngredients(selectedMeal)" :key="index" class="flex items-center">
                <span class="text-gold mr-2">•</span>
                {{ ingredient.measure }} {{ ingredient.name }}
              </li>
            </ul>

            <h3 class="text-xl text-wood mb-2">Instructions</h3>
            <p class="text-charcoal whitespace-pre-line">{{ selectedMeal.strInstructions }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import MenuService from '../services/menu.service';

// State
const searchQuery = ref('');
const selectedCategory = ref('');
const categories = ref([]);
const meals = ref([]);
const loading = ref(true);
const selectedMeal = ref(null);
const searchTimeout = ref(null);

// Fetch categories on component mount
onMounted(async () => {
  try {
    categories.value = await MenuService.getMealCategories();
    // Load a default category to show some initial meals
    if (categories.value.length > 0) {
      selectedCategory.value = categories.value[0].strCategory;
      await fetchMealsByCategory(selectedCategory.value);
    }
  } catch (error) {
    console.error('Failed to load meal categories:', error);
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
        meals.value = await MenuService.searchMealsByName(searchQuery.value);
      } catch (error) {
        console.error('Search error:', error);
        meals.value = [];
      } finally {
        loading.value = false;
      }
    } else if (selectedCategory.value) {
      // If search is cleared but category is selected, show category meals
      fetchMealsByCategory(selectedCategory.value);
    } else {
      meals.value = [];
    }
  }, 500);
};

const handleCategoryChange = async () => {
  if (selectedCategory.value) {
    searchQuery.value = ''; // Clear search query when selecting category
    await fetchMealsByCategory(selectedCategory.value);
  } else if (searchQuery.value.trim()) {
    // If category is cleared but search has text, perform search
    handleSearchInput();
  } else {
    meals.value = [];
  }
};

const fetchMealsByCategory = async (category) => {
  loading.value = true;
  try {
    meals.value = await MenuService.getMealsByCategory(category);
  } catch (error) {
    console.error('Failed to fetch meals by category:', error);
    meals.value = [];
  } finally {
    loading.value = false;
  }
};

const showMealDetails = async (mealId) => {
  loading.value = true;
  try {
    const mealDetails = await MenuService.getMealById(mealId);
    selectedMeal.value = mealDetails;
  } catch (error) {
    console.error('Failed to fetch meal details:', error);
  } finally {
    loading.value = false;
  }
};

// Helper function to extract ingredients and measures
const getMealIngredients = (meal) => {
  if (!meal) return [];
  
  const ingredients = [];
  for (let i = 1; i <= 20; i++) {
    const ingredient = meal[`strIngredient${i}`];
    const measure = meal[`strMeasure${i}`];
    
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