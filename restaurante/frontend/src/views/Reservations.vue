<template>
  <div class="min-h-screen bg-cream py-16 px-6">
    <div class="container mx-auto max-w-4xl">
      <!-- Page Header -->
      <div class="text-center mb-12">
        <h1 class="section-heading">Reserve Your Table</h1>
        <p class="text-charcoal text-xl max-w-2xl mx-auto">Experience the epitome of fine dining at Noir Et Or. Complete the form below to secure your perfect dining experience.</p>
      </div>
      
      <!-- Success Message -->
      <div v-if="successMessage" class="bg-emerald bg-opacity-10 border-l-4 border-emerald rounded p-6 mb-10 transition-all duration-500 ease-in-out">
        <div class="flex items-start">
          <div class="flex-shrink-0">
            <!-- Success Icon -->
            <svg class="h-6 w-6 text-emerald mt-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <div class="ml-4">
            <p class="text-emerald font-medium text-lg">Reservation Confirmed</p>
            <p class="text-charcoal mt-2">{{ successMessage }}</p>
          </div>
        </div>
      </div>
      
      <!-- Form Card -->
      <div class="bg-pearl shadow-lg rounded-lg overflow-hidden">
        <!-- Golden Accent Bar -->
        <div class="h-2 bg-gold"></div>
        
        <!-- Form Content -->
        <div class="p-8 md:p-10">
          <form @submit.prevent="submitReservation" class="space-y-6">
            <!-- Guest Information Section -->
            <div>
              <h2 class="text-2xl font-serif text-burgundy mb-6 font-subheading">Guest Information</h2>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="form-control">
                  <label for="name" class="block text-charcoal mb-2 font-medium">Full Name</label>
                  <input 
                    id="name" 
                    v-model="form.name" 
                    type="text" 
                    required
                    placeholder="Your full name"
                    class="w-full px-4 py-3 border border-slate rounded focus:outline-none focus:ring-2 focus:ring-gold focus:border-transparent"
                  >
                </div>
                
                <div class="form-control">
                  <label for="email" class="block text-charcoal mb-2 font-medium">Email Address</label>
                  <input 
                    id="email" 
                    v-model="form.email" 
                    type="email" 
                    required
                    placeholder="Your email address"
                    class="w-full px-4 py-3 border border-slate rounded focus:outline-none focus:ring-2 focus:ring-gold focus:border-transparent"
                  >
                </div>
                
                <div class="form-control md:col-span-2">
                  <label for="phone" class="block text-charcoal mb-2 font-medium">Phone Number</label>
                  <input 
                    id="phone" 
                    v-model="form.phone" 
                    type="tel" 
                    required
                    placeholder="Your phone number"
                    class="w-full px-4 py-3 border border-slate rounded focus:outline-none focus:ring-2 focus:ring-gold focus:border-transparent"
                  >
                </div>
              </div>
            </div>
            
            <!-- Reservation Details Section -->
            <div>
              <h2 class="text-2xl font-serif text-burgundy mb-6 font-subheading">Reservation Details</h2>
              <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div class="form-control">
                  <label for="date" class="block text-charcoal mb-2 font-medium">Date</label>
                  <input 
                    id="date" 
                    v-model="form.date" 
                    type="date" 
                    required
                    :min="minDate"
                    class="w-full px-4 py-3 border border-slate rounded focus:outline-none focus:ring-2 focus:ring-gold focus:border-transparent"
                    :class="{'border-emerald': form.date && form.time && timeSlotAvailable, 'border-burgundy': form.date && form.time && !timeSlotAvailable}"
                  >
                </div>
                
                <div class="form-control">
                  <label for="time" class="block text-charcoal mb-2 font-medium">Time</label>
                  <select 
                    id="time" 
                    v-model="form.time" 
                    required
                    class="w-full px-4 py-3 border border-slate rounded focus:outline-none focus:ring-2 focus:ring-gold focus:border-transparent appearance-none bg-white bg-no-repeat bg-right pr-10"
                    style="background-image: url('data:image/svg+xml;charset=UTF-8,%3csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 24 24\' fill=\'none\' stroke=\'%234a4a4a\' stroke-width=\'2\' stroke-linecap=\'round\' stroke-linejoin=\'round\'%3e%3cpolyline points=\'6 9 12 15 18 9\'%3e%3c/polyline%3e%3c/svg%3e'); background-size: 24px; background-position: right 10px center;"
                    :class="{'border-emerald': form.date && form.time && timeSlotAvailable, 'border-burgundy': form.date && form.time && !timeSlotAvailable}"
                  >
                    <option value="" disabled selected>Select time</option>
                    <option v-for="time in availableTimes" :key="time" :value="time">{{ time }}</option>
                  </select>
                </div>
                
                <div class="form-control">
                  <label for="guests" class="block text-charcoal mb-2 font-medium">Number of Guests</label>
                  <div class="flex border border-slate rounded"
                    :class="{'border-emerald': form.date && form.time && timeSlotAvailable, 'border-burgundy': form.date && form.time && !timeSlotAvailable}">
                    <button 
                      type="button" 
                      @click="decrementGuests" 
                      class="px-4 py-3 bg-pearl hover:bg-slate hover:bg-opacity-10 text-charcoal font-bold focus:outline-none"
                      :disabled="form.guests <= 1"
                    >−</button>
                    <input 
                      id="guests" 
                      v-model.number="form.guests" 
                      type="number" 
                      min="1" 
                      max="20" 
                      required
                      class="w-full px-4 py-3 text-center border-none focus:outline-none focus:ring-0"
                      readonly
                    >
                    <button 
                      type="button" 
                      @click="incrementGuests" 
                      class="px-4 py-3 bg-pearl hover:bg-slate hover:bg-opacity-10 text-charcoal font-bold focus:outline-none"
                      :disabled="form.guests >= 20"
                    >+</button>
                  </div>
                </div>
                
                <!-- Availability Message -->
                <div v-if="form.date && form.time" class="md:col-span-3 mt-2">
                  <div v-if="checkingAvailability" class="flex items-center text-slate">
                    <svg class="animate-spin -ml-1 mr-2 h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Checking availability...
                  </div>
                  <div v-else-if="availabilityMessage" 
                    :class="{
                      'text-emerald flex items-center': timeSlotAvailable,
                      'text-burgundy flex items-center': !timeSlotAvailable
                    }">
                    <svg v-if="timeSlotAvailable" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                    </svg>
                    <svg v-else class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                    </svg>
                    {{ availabilityMessage }}
                  </div>
                </div>
                
                <div class="form-control md:col-span-3">
                  <label for="occasion" class="block text-charcoal mb-2 font-medium">Special Occasion</label>
                  <select 
                    id="occasion" 
                    v-model="form.occasion"
                    class="w-full px-4 py-3 border border-slate rounded focus:outline-none focus:ring-2 focus:ring-gold focus:border-transparent appearance-none bg-white bg-no-repeat bg-right pr-10"
                    style="background-image: url('data:image/svg+xml;charset=UTF-8,%3csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 24 24\' fill=\'none\' stroke=\'%234a4a4a\' stroke-width=\'2\' stroke-linecap=\'round\' stroke-linejoin=\'round\'%3e%3cpolyline points=\'6 9 12 15 18 9\'%3e%3c/polyline%3e%3c/svg%3e'); background-size: 24px; background-position: right 10px center;"
                  >
                    <option value="">None</option>
                    <option value="birthday">Birthday</option>
                    <option value="anniversary">Anniversary</option>
                    <option value="date">Date Night</option>
                    <option value="business">Business Dinner</option>
                    <option value="other">Other</option>
                  </select>
                </div>
                
                <div class="form-control md:col-span-3">
                  <label for="notes" class="block text-charcoal mb-2 font-medium">Special Requests</label>
                  <textarea 
                    id="notes" 
                    v-model="form.notes" 
                    rows="4" 
                    placeholder="Any dietary restrictions or special requests"
                    class="w-full px-4 py-3 border border-slate rounded focus:outline-none focus:ring-2 focus:ring-gold focus:border-transparent"
                  ></textarea>
                  <p class="text-slate text-sm mt-2">Our culinary team will make every effort to accommodate your requests.</p>
                </div>
              </div>
            </div>
            
            <!-- Error Message -->
            <div v-if="error" class="border-l-4 border-burgundy bg-amber-400 bg-opacity-5 p-4 rounded">
              <div class="flex">
                <div class="flex-shrink-0">
                  <svg class="h-5 w-5 text-burgundy" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                  </svg>
                </div>
                <div class="ml-3">
                  <p class="text-burgundy text-sm font-medium">{{ error }}</p>
                </div>
              </div>
            </div>
            
            <!-- Submit Button -->
            <div class="pt-4">
              <button 
                type="submit" 
                class="w-full bg-gold text-charcoal font-bold py-4 rounded shadow hover:bg-opacity-90 transition-all duration-300 focus:outline-none focus:ring-4 focus:ring-gold focus:ring-opacity-50"
                :disabled="loading || (form.date && form.time && !timeSlotAvailable) || checkingAvailability"
                :class="{
                  'opacity-75 cursor-not-allowed': loading || (form.date && form.time && !timeSlotAvailable) || checkingAvailability,
                  'bg-burgundy text-cream hover:bg-burgundy hover:bg-opacity-90': form.date && form.time && !timeSlotAvailable
                }"
              >
                <span v-if="loading" class="flex items-center justify-center">
                  <span class="mr-2">
                    <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                  </span>
                  Processing...
                </span>
                <span v-else>Reserve My Table</span>
              </button>
            </div>
            
            <!-- Fine Print -->
            <div class="text-center text-slate text-sm">
              <p>By making a reservation, you agree to our reservation policy.</p>
              <p class="mt-1">A credit card may be required to secure reservations for large parties or special events.</p>
            </div>
          </form>
        </div>
      </div>
      
      <!-- Contact Info -->
      <div class="text-center mt-10">
        <p class="text-charcoal">For parties larger than 10 or special events, please call us directly at</p>
        <p class="text-burgundy font-bold text-lg mt-1">(555) 123-4567</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useReservationStore } from '../stores/reservation';
import { useAuthStore } from '../stores/auth';

const reservationStore = useReservationStore();
const authStore = useAuthStore();

const loading = ref(false);
const checkingAvailability = ref(false);
const error = ref('');
const successMessage = ref('');
const timeSlotAvailable = ref(true);
const availabilityMessage = ref('');

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

function incrementGuests() {
  if (form.value.guests < 20) {
    form.value.guests++;
  }
}

function decrementGuests() {
  if (form.value.guests > 1) {
    form.value.guests--;
  }
}

// Prefill form with user data if logged in
onMounted(() => {
  if (authStore.isAuthenticated && authStore.user) {
    form.value.name = authStore.user.name || '';
    form.value.email = authStore.user.email || '';
    form.value.phone = authStore.user.phone || '';
  }
});

// Check availability when date, time, or guests change
watch(
  [() => form.value.date, () => form.value.time, () => form.value.guests],
  async ([newDate, newTime, newGuests], [oldDate, oldTime, oldGuests]) => {
    // Only check if we have both date and time
    if (newDate && newTime && newGuests) {
      // Avoid unnecessary checks if none of these values changed
      if (newDate === oldDate && newTime === oldTime && newGuests === oldGuests) {
        return;
      }
      
      checkingAvailability.value = true;
      availabilityMessage.value = '';
      
      try {
        const response = await reservationStore.checkAvailability(
          newDate,
          newTime,
          newGuests
        );
        
        timeSlotAvailable.value = response.data.available;
        
        if (response.data.available) {
          availabilityMessage.value = 'This time slot is available!';
        } else {
          availabilityMessage.value = 'Sorry, this time slot is no longer available. Please choose another time.';
        }
      } catch (err) {
        console.error('Error checking availability:', err);
        timeSlotAvailable.value = false;
        availabilityMessage.value = 'Unable to check availability. Please try again.';
      } finally {
        checkingAvailability.value = false;
      }
    } else {
      // Reset availability state if we don't have complete information
      timeSlotAvailable.value = true;
      availabilityMessage.value = '';
    }
  }
);

async function submitReservation() {
  // Form validation
  if (!form.value.date || !form.value.time || !form.value.name || !form.value.email || !form.value.phone) {
    error.value = 'Please fill out all required fields.';
    return;
  }
  
  loading.value = true;
  error.value = '';
  successMessage.value = '';
  
  try {
    // Double-check availability to prevent race conditions
    const availabilityResponse = await reservationStore.checkAvailability(
      form.value.date,
      form.value.time,
      form.value.guests
    );
    
    if (!availabilityResponse.data.available) {
      error.value = 'Sorry, this time slot is no longer available. Please choose another time.';
      timeSlotAvailable.value = false;
      availabilityMessage.value = 'Sorry, this time slot is no longer available. Please choose another time.';
      return;
    }
    
    // Format phone number if needed (optional)
    const formattedPhone = form.value.phone.replace(/\D/g, '');
    
    // Create reservation
    await reservationStore.createReservation({
      name: form.value.name,
      email: form.value.email,
      phone: formattedPhone,
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
/* Only include styles that can't be handled by Tailwind */
input[type="date"] {
  color-scheme: light;
}

/* Remove number input spinners */
input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
input[type="number"] {
  -moz-appearance: textfield;
}
</style>