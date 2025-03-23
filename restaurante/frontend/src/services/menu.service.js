import axios from 'axios';

// TheMealDB API service
const mealDbBaseUrl = 'https://www.themealdb.com/api/json/v1/1';
// TheCocktailDB API service
const cocktailDbBaseUrl = 'https://www.thecocktaildb.com/api/json/v1/1';

class MenuService {
  // Food API methods
  async searchMealsByName(name) {
    try {
      const response = await axios.get(`${mealDbBaseUrl}/search.php?s=${name}`);
      return response.data.meals || [];
    } catch (error) {
      console.error('Error searching meals by name:', error);
      throw error;
    }
  }

  async getMealCategories() {
    try {
      const response = await axios.get(`${mealDbBaseUrl}/categories.php`);
      return response.data.categories || [];
    } catch (error) {
      console.error('Error fetching meal categories:', error);
      throw error;
    }
  }

  async getMealsByCategory(category) {
    try {
      const response = await axios.get(`${mealDbBaseUrl}/filter.php?c=${category}`);
      return response.data.meals || [];
    } catch (error) {
      console.error('Error fetching meals by category:', error);
      throw error;
    }
  }

  async getMealById(id) {
    try {
      const response = await axios.get(`${mealDbBaseUrl}/lookup.php?i=${id}`);
      return response.data.meals ? response.data.meals[0] : null;
    } catch (error) {
      console.error('Error fetching meal by id:', error);
      throw error;
    }
  }

  // Drinks API methods
  async searchDrinksByName(name) {
    try {
      const response = await axios.get(`${cocktailDbBaseUrl}/search.php?s=${name}`);
      return response.data.drinks || [];
    } catch (error) {
      console.error('Error searching drinks by name:', error);
      throw error;
    }
  }

  async getDrinkCategories() {
    try {
      const response = await axios.get(`${cocktailDbBaseUrl}/list.php?c=list`);
      return response.data.drinks || [];
    } catch (error) {
      console.error('Error fetching drink categories:', error);
      throw error;
    }
  }

  async getDrinksByCategory(category) {
    try {
      const response = await axios.get(`${cocktailDbBaseUrl}/filter.php?c=${category}`);
      return response.data.drinks || [];
    } catch (error) {
      console.error('Error fetching drinks by category:', error);
      throw error;
    }
  }

  async getDrinkById(id) {
    try {
      const response = await axios.get(`${cocktailDbBaseUrl}/lookup.php?i=${id}`);
      return response.data.drinks ? response.data.drinks[0] : null;
    } catch (error) {
      console.error('Error fetching drink by id:', error);
      throw error;
    }
  }
}

export default new MenuService();