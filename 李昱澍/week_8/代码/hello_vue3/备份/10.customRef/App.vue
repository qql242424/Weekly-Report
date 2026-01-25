<template>
  <div id="app"></div>
</template>

<script setup lang="ts" name="App">
import useMsgRef from './useMsgRef'
let msg = useMsgRef('你好', 1000)
console.log(msg.value)
</script>

<style scoped>
#app {
  border-radius: 5px;
  background-color: #eee;
  padding: 10px;
  box-shadow: 0 0 10px;
}
</style>
