import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router/routes'
import vue3GoogleLogin from 'vue3-google-login'
import './assets/index.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(vue3GoogleLogin, {
  clientId: 'YOUR_GOOGLE_CLIENT_ID' // This will need to be updated with your actual client ID
})

app.mount('#app')