<template>
  <div id="app">
    <h3>我是App组件</h3>
    <Suspense>
      <template v-slot:default>
        <Child />
      </template>
      <template v-slot:fallback>
        <h3>加载中.......</h3>
      </template>
    </Suspense>
  </div>
</template>
<script setup lang="ts" name="App">
import Child from './Child.vue'
</script>
<style scoped>
#app {
  border: solid 1px #000;
  border-radius: 5px;
  background-color: #eee;
  padding: 10px;
}
</style>
