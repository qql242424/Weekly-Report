<template>
  <div>
    <Person />
    <Car />
    <Water />
    <PersonRef ref="ren" />
    <button @click="printRen">打印人</button>
  </div>
</template>
<script setup lang="ts" name="App">
import Person from './components/Person.vue'
import Car from './components/Car.vue'
import Water from './components/Water.vue'
import PersonRef from './components/PersonRef.vue'
import { ref } from 'vue'
let ren = ref()
function printRen() {
  console.log(ren.value)
  console.log(ren.value.name)
  console.log(ren.value.age)
}
</script>
<style></style>
