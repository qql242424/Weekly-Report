<template>
  <div id="app">
    <h3>我是App组件</h3>
    <Child />
  </div>
</template>
<script setup lang="ts" name="App">
import Child from './Child.vue'
</script>
<style scoped>
#app {
  border-radius: 5px;
  background-color: #eee;
  padding: 10px;
  box-shadow: 0 0 10px;
  width: 400px;
  height: 600px;
}
</style>
