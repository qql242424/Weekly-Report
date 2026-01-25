<template>
  <div id="app"></div>
</template>

<script setup lang="ts" name="App">
import { toRaw, markRaw } from 'vue'

let a = { a: 1 }
let b = markRaw({ a: 1 })

console.log(toRaw(a))
console.log(b)
</script>

<style scoped>
#app {
  border-radius: 5px;
  background-color: #eee;
  padding: 10px;
  box-shadow: 0 0 10px;
}
</style>
