<template>
  <div id="app">
    <h3>Pinia练习</h3>
    <div class="content">
      <Sum></Sum>
    </div>
    <div class="content">
      <Sentence></Sentence>
    </div>
  </div>
</template>
<script setup lang="ts" name="App">
import Sum from '@/components/Sum.vue'
import Sentence from './components/Sentence.vue'
</script>

<style scoped>
#app {
  border-radius: 15px;
  background-color: pink;
  padding: 10px;
  box-shadow: 0 0 10px;
}
.content {
  background: linear-gradient(to right, rgb(255, 144, 144), rgb(209, 255, 209));
  border-radius: 15px;
  width: 80%;
  margin: 10px;
  padding: 10px;
}
</style>
