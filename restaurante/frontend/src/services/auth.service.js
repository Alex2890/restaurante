import api from './api'

class AuthService {
  async login(credentials) {
    const response = await api.post('/auth/login', credentials)
    return response.data
  }

  async register(userData) {
    const response = await api.post('/auth/register', userData)
    return response.data
  }

  async googleLogin(googleUser) {
    const response = await api.post('/auth/google', {
      id_token: googleUser.credential
    })
    return response.data
  }

  async getProfile() {
    const response = await api.get('/auth/profile')
    return response.data
  }
}

export default new AuthService()