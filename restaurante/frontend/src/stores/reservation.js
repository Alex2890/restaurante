import { defineStore } from 'pinia'
import { ref } from 'vue'
import ReservationService from '../services/reservation.service'

export const useReservationStore = defineStore('reservation', () => {
  const reservations = ref([])
  const loading = ref(false)
  const error = ref(null)

  async function fetchReservations() {
    loading.value = true
    error.value = null
    try {
      const response = await ReservationService.getReservations()
      reservations.value = response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to fetch reservations'
    } finally {
      loading.value = false
    }
  }

  async function createReservation(reservationData) {
    loading.value = true
    error.value = null
    try {
      const response = await ReservationService.createReservation(reservationData)
      reservations.value.push(response.data)
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to create reservation'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateReservation(id, reservationData) {
    loading.value = true
    error.value = null
    try {
      const response = await ReservationService.updateReservation(id, reservationData)
      const index = reservations.value.findIndex(r => r.id === id)
      if (index !== -1) {
        reservations.value[index] = response.data
      }
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to update reservation'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function cancelReservation(id) {
    loading.value = true
    error.value = null
    try {
      await ReservationService.deleteReservation(id)
      reservations.value = reservations.value.filter(r => r.id !== id)
      return true
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to cancel reservation'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    reservations,
    loading,
    error,
    fetchReservations,
    createReservation,
    updateReservation,
    cancelReservation
  }
})