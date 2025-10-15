// stores/user.js
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUserStore = defineStore('user', () => {
  const user = ref(null)
  const isLoggedIn = ref(false)

  function setUser(data) {
    user.value = data
    isLoggedIn.value = !!data
  }

  return { user, isLoggedIn, setUser }
})
