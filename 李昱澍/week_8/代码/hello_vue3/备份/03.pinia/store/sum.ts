import { defineStore } from 'pinia'
// export const useSumStore = defineStore('sum', {
//   state() {
//     return {
//       sum: 1,
//     }
//   },
//   getters: {
//     Sum10: (state) => state.sum * 10,
//   },
// })
// 相当于：
import { ref, computed } from 'vue'
export const useSumStore = defineStore('sum', () => {
  let sum = ref(1)
  let Sum10 = computed({
    get() {
      return sum.value * 10
    },
    set(value) {
      sum.value = value
    },
  })
  return { sum, Sum10 }
})
