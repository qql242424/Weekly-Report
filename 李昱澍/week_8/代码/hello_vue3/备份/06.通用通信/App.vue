<template>
  <div id="app">
    <h3>组件通信3：通用通信</h3>
    其中a与addA使用mitt、
    <br />b与addB使用pinia
    <div class="components">
      <Component1 />
      <Component2 />
    </div>
  </div>
</template>

<script setup lang="ts" name="App">
import Component1 from './components/Component1.vue'
import Component2 from './components/Component2.vue'
</script>

<style scoped>
#app {
  padding: 20px;
  border-radius: 20px;
  box-shadow: 0 0 10px;
}
.components {
  display: flex;
  justify-content: space-evenly;
}
</style>
