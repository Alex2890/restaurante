<template>
  <div class="menu-page">
    <h1>Our Menu</h1>
    
    <div class="menu-categories">
      <button 
        v-for="category in categories" 
        :key="category" 
        @click="activeCategory = category"
        :class="{ active: activeCategory === category }"
        class="category-btn">
        {{ category }}
      </button>
    </div>
    
    <div class="menu-items">
      <div 
        v-for="item in filteredItems" 
        :key="item.id"
        class="menu-item">
        <div class="item-info">
          <h3>{{ item.name }}</h3>
          <p class="description">{{ item.description }}</p>
          <p class="price">${{ item.price.toFixed(2) }}</p>
          <div class="dietary-tags">
            <span v-if="item.vegetarian" class="tag vegetarian">Vegetarian</span>
            <span v-if="item.vegan" class="tag vegan">Vegan</span>
            <span v-if="item.glutenFree" class="tag gluten-free">Gluten Free</span>
          </div>
        </div>
        <div class="item-image"><!-- Will be replaced with actual image --></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const categories = ['Appetizers', 'Entrees', 'Desserts', 'Drinks'];
const activeCategory = ref('Appetizers');

const menuItems = ref([
  // Appetizers
  {
    id: 1,
    name: 'Truffle Arancini',
    description: 'Crispy risotto balls with black truffle and mozzarella center',
    price: 16.50,
    category: 'Appetizers',
    vegetarian: true,
    vegan: false,
    glutenFree: false
  },
  {
    id: 2,
    name: 'Seared Scallops',
    description: 'Fresh scallops with citrus glaze and microgreens',
    price: 19.00,
    category: 'Appetizers',
    vegetarian: false,
    vegan: false,
    glutenFree: true
  },
  {
    id: 3,
    name: 'Garden Salad',
    description: 'Seasonal greens with housemade vinaigrette and toasted seeds',
    price: 14.00,
    category: 'Appetizers',
    vegetarian: true,
    vegan: true,
    glutenFree: true
  },
  
  // Entrees
  {
    id: 4,
    name: 'Filet Mignon',
    description: '8oz prime filet with red wine reduction and truffle butter',
    price: 42.00,
    category: 'Entrees',
    vegetarian: false,
    vegan: false,
    glutenFree: true
  },
  {
    id: 5,
    name: 'Herb Crusted Salmon',
    description: 'Wild-caught salmon with herbs, lemon, and seasonal vegetables',
    price: 36.00,
    category: 'Entrees',
    vegetarian: false,
    vegan: false,
    glutenFree: true
  },
  {
    id: 6,
    name: 'Wild Mushroom Risotto',
    description: 'Creamy arborio rice with seasonal wild mushrooms and aged parmesan',
    price: 28.00,
    category: 'Entrees',
    vegetarian: true,
    vegan: false,
    glutenFree: true
  },
  
  // Desserts
  {
    id: 7,
    name: 'Chocolate Soufflé',
    description: 'Warm chocolate soufflé with vanilla bean ice cream',
    price: 14.00,
    category: 'Desserts',
    vegetarian: true,
    vegan: false,
    glutenFree: false
  },
  {
    id: 8,
    name: 'Crème Brûlée',
    description: 'Classic vanilla bean custard with caramelized sugar',
    price: 12.00,
    category: 'Desserts',
    vegetarian: true,
    vegan: false,
    glutenFree: true
  },
  
  // Drinks
  {
    id: 9,
    name: 'Signature Cocktail',
    description: 'House specialty with small-batch bourbon and bitters',
    price: 15.00,
    category: 'Drinks',
    vegetarian: true,
    vegan: true,
    glutenFree: true
  },
  {
    id: 10,
    name: 'Wine Pairing',
    description: 'Selection of wines curated to complement your meal',
    price: 24.00,
    category: 'Drinks',
    vegetarian: true,
    vegan: true,
    glutenFree: true
  }
]);

const filteredItems = computed(() => {
  return menuItems.value.filter(item => item.category === activeCategory.value);
});
</script>

<style scoped>
/* Styling will be enhanced with TailwindCSS */
</style>