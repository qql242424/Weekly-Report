<template>
  <div id="app">
    {{ sum1 }}
    <button @click="addA1">a1+1</button>
    <button @click="addSum1">sum1+1</button>
    <hr />
    {{ sum2 }}
    <button @click="addA2">a2+1</button>
    <button @click="addSum2">sum2+1</button>
    <hr />
    {{ sum3 }}
    <button @click="addSum3">sum3+1</button>
    <hr />
    {{ sum4 }}
    <!-- <button @click="addSum4">sum4+1</button> -->
  </div>
</template>

<script setup lang="ts" name="App">
import { ref, reactive, readonly, shallowReadonly } from 'vue'

let sum1 = reactive({ a: 1, b: 2 })
sum1 = readonly(sum1)
function addA1() {
  sum1.a += 1
}
function addSum1() {
  Object.assign(sum1, { a: 2, b: 3 })
}

let sum2 = reactive({ a: 1, b: 2 })
sum2 = shallowReadonly(sum1)
function addA2() {
  sum2.a += 1
}
function addSum2() {
  Object.assign(sum2, { a: 2, b: 3 })
}

let sum3 = ref(1)
sum3 = readonly(sum3)
function addSum3() {
  sum3.value += 1
}

// let sum4 = ref(1)
let sum4 = shallowReadonly({ a: 1 })
// function addSum4() {
//   sum4.value += 1
// }

console.log('sum1', sum1)
console.log('sum2', sum2)
console.log('sum3', sum3)
console.log('sum4', sum4)
</script>

<style scoped>
#app {
  border-radius: 5px;
  background-color: #eee;
  padding: 10px;
  box-shadow: 0 0 10px;
}
</style>
