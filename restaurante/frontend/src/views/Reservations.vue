<template>
  <div class="reservations-page">
    <h1>Make a Reservation</h1>
    
    <form @submit.prevent="submitReservation" class="reservation-form">
      <div class="form-group">
        <label for="name">Full Name</label>
        <input 
          id="name" 
          v-model="form.name" 
          type="text" 
          required
          placeholder="Your full name"
        >
      </div>
      
      <div class="form-group">
        <label for="email">Email Address</label>
        <input 
          id="email" 
          v-model="form.email" 
          type="email" 
          required
          placeholder="Your email address"
        >
      </div>
      
      <div class="form-group">
        <label for="phone">Phone Number</label>
        <input 
          id="phone" 
          v-model="form.phone" 
          type="tel" 
          required
          placeholder="Your phone number"
        >
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <label for="date">Date</label>
          <input 
            id="date" 
            v-model="form.date" 
            type="date" 
            required
            :min="minDate"
          >
        </div>
        
        <div class="form-group">
          <label for="time">Time</label>
          <select 
            id="time" 
            v-model="form.time" 
            required
          >
            <option v-for="time in availableTimes" :key="time" :value="time">{{ time }}</option>
          </select>
        </div>
      </div>
      
      <div class="form-group">
        <label for="guests">Number of Guests</label>
        <input 
          id="guests" 
          v-model.number="form.guests" 
          type="number" 
          min="1" 
          max="20" 
          required
        >
      </div>
      
      <div class="form-group">
        <label for="occasion">Special Occasion</label>
        <select id="occasion" v-model="form.occasion">
          <option value="">None</option>
          <option value="birthday">Birthday</option>
          <option value="anniversary">Anniversary</option>
          <option value="date">Date Night</option>
          <option value="business">Business Dinner</option>
          <option value="other">Other</option>
        </select>
      </div>
      
      <div class="form-group">
        <label for="notes">Special Requests</label>
        <textarea 
          id="notes" 
          v-model="form.notes" 
          rows="3" 
          placeholder="Any dietary restrictions or special requests"
        ></textarea>
      </div>
      
      <div v-if="error" class="error-message">{{ error }}</div>
      
      <button type="submit" class="submit-btn" :disabled="loading">
        {{ loading ? 'Processing...' : 'Make Reservation' }}
      </button>
    </form>
    
    <div v-if="successMessage" class="success-message">
      {{ successMessage }}
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useReservationStore } from '../stores/reservation';
import { useAuthStore } from '../stores/auth';

const reservationStore = useReservationStore();
const authStore = useAuthStore();

const loading = ref(false);
const error = ref('');
const successMessage = ref('');

// Calculate minimum date (today)
const minDate = computed(() => {
  const today = new Date();
  return today.toISOString().split('T')[0];
});

const availableTimes = [
  '17:00', '17:30', '18:00', '18:30',
  '19:00', '19:30', '20:00', '20:30',
  '21:00', '21:30'
];

const form = ref({
  name: '',
  email: '',
  phone: '',
  date: '',
  time: '',
  guests: 2,
  occasion: '',
  notes: ''
});

// Prefill form with user data if logged in
onMounted(() => {
  if (authStore.isAuthenticated && authStore.user) {
    form.value.name = authStore.user.name || '';
    form.value.email = authStore.user.email || '';
  }
});

async function submitReservation() {
  loading.value = true;
  error.value = '';
  successMessage.value = '';
  
  try {
    // First check availability
    const availabilityResponse = await reservationStore.checkAvailability(
      form.value.date,
      form.value.time,
      form.value.guests
    );
    
    if (!availabilityResponse.data.available) {
      error.value = 'Sorry, this time slot is no longer available. Please choose another time.';
      return;
    }
    
    await reservationStore.createReservation({
      name: form.value.name,
      email: form.value.email,
      phone: form.value.phone,
      date: form.value.date,
      time: form.value.time,
      party_size: form.value.guests,
      occasion: form.value.occasion,
      special_requests: form.value.notes
    });
    
    successMessage.value = 'Your reservation has been successfully confirmed! You will receive a confirmation email shortly.';
    // Reset form after successful submission
    form.value = {
      name: authStore.user?.name || '',
      email: authStore.user?.email || '',
      phone: '',
      date: '',
      time: '',
      guests: 2,
      occasion: '',
      notes: ''
    };
  } catch (err) {
    error.value = err.response?.data?.message || 'There was an error processing your reservation. Please try again.';
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
/* Styling will be enhanced with TailwindCSS */
</style>