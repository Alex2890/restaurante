<template>
  <div class="contact-page">
    <h1>Contact Us</h1>
    
    <div class="contact-container">
      <div class="contact-info">
        <h2>Reservation & Inquiries</h2>
        <p class="address">
          <strong>Address:</strong><br>
          123 Gourmet Avenue<br>
          Culinary District<br>
          City, State 12345
        </p>
        
        <p class="phone">
          <strong>Phone:</strong><br>
          <a href="tel:+1234567890">(123) 456-7890</a>
        </p>
        
        <p class="email">
          <strong>Email:</strong><br>
          <a href="mailto:info@finerestaurant.com">info@finerestaurant.com</a>
        </p>
        
        <div class="hours">
          <h3>Hours of Operation</h3>
          <p>Tuesday - Thursday: 5:00 PM - 10:00 PM</p>
          <p>Friday - Saturday: 5:00 PM - 11:00 PM</p>
          <p>Sunday: 5:00 PM - 9:00 PM</p>
          <p>Monday: Closed</p>
        </div>
      </div>
      
      <div class="contact-form-container">
        <h2>Send us a Message</h2>
        <form @submit.prevent="submitForm" class="contact-form">
          <div class="form-group">
            <label for="name">Your Name</label>
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
            <label for="subject">Subject</label>
            <input 
              id="subject" 
              v-model="form.subject" 
              type="text" 
              required
              placeholder="Message subject"
            >
          </div>
          
          <div class="form-group">
            <label for="message">Message</label>
            <textarea 
              id="message" 
              v-model="form.message" 
              rows="5" 
              required
              placeholder="Your message"
            ></textarea>
          </div>
          
          <div v-if="error" class="error-message">{{ error }}</div>
          <div v-if="success" class="success-message">{{ success }}</div>
          
          <button type="submit" class="submit-btn" :disabled="loading">
            {{ loading ? 'Sending...' : 'Send Message' }}
          </button>
        </form>
      </div>
    </div>
    
    <div class="map-container">
      <h2>Find Us</h2>
      <div class="map">
        <!-- Map will be implemented later -->
        <p class="map-placeholder">Interactive map will be displayed here</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const form = ref({
  name: '',
  email: '',
  subject: '',
  message: ''
});

const loading = ref(false);
const error = ref('');
const success = ref('');

async function submitForm() {
  loading.value = true;
  error.value = '';
  success.value = '';
  
  try {
    // Here we would typically call an API to send the message
    // For now we'll just simulate a successful submission
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    success.value = 'Your message has been sent successfully. We will get back to you soon!';
    
    // Reset form
    form.value = {
      name: '',
      email: '',
      subject: '',
      message: ''
    };
  } catch (err) {
    error.value = 'There was an error sending your message. Please try again.';
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
/* Styling will be enhanced with TailwindCSS */
</style>