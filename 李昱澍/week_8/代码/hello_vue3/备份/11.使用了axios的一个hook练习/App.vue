<template>
  <div id="app">
    <button @click="getDog">来一张小狗！</button>
    <hr />
    <img v-for="(u, index) in DogList" :key="index" :src="u" />
  </div>
</template>

<script setup lang="ts" name="App">
import useDog from './useDog'
let { DogList, getDog } = useDog()
</script>

<style scoped>
#app {
  border-radius: 5px;
  background-color: pink;
  padding: 10px;
  box-shadow: 0 0 10px;
}
button {
  margin-bottom: 10px;
}
img {
  height: 200px;
  margin-right: 10px;
}
</style>
