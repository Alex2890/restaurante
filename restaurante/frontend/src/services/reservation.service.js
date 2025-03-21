import api from './api'

class ReservationService {
  async getReservations() {
    return await api.get('/reservations')
  }

  async getReservation(id) {
    return await api.get(`/reservations/${id}`)
  }

  async createReservation(reservationData) {
    return await api.post('/reservations', reservationData)
  }

  async updateReservation(id, reservationData) {
    return await api.put(`/reservations/${id}`, reservationData)
  }

  async deleteReservation(id) {
    return await api.delete(`/reservations/${id}`)
  }

  async checkAvailability(date, time, partySize) {
    return await api.get('/reservations/availability', {
      params: { date, time, partySize }
    })
  }
}

export default new ReservationService()