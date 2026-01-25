import { defineStore } from 'pinia'

export const useBStore = defineStore('b', {
  state() {
    return {
      b: 1,
    }
  },
  actions: {
    addB() {
      this.b++
    },
  },
})
