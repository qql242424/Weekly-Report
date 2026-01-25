<template>
  <div id="app">
    {{ sum1 }}
    <button @click="addA1">a1+1</button>
    <button @click="addSum1">sum1+1</button>
    <br />
    {{ sum2 }}
    <button @click="addA2">a2+1</button>
    <button @click="addSum2">sum2+1</button>
  </div>
</template>

<script setup lang="ts" name="App">
import { shallowRef, shallowReactive } from 'vue'
let sum1 = shallowRef({ a: 1, b: 2 })
function addA1() {
  sum1.value.a += 1
}
function addSum1() {
  sum1.value = { a: 2, b: 3 }
}

let sum2 = shallowReactive({ a: 1, b: 2 })
function addA2() {
  sum2.a += 1
}
function addSum2() {
  Object.assign(sum2, { a: 2, b: 3 })
}
</script>

<style scoped>
#app {
  border-radius: 5px;
  background-color: #eee;
  padding: 10px;
  box-shadow: 0 0 10px;
}
</style>
