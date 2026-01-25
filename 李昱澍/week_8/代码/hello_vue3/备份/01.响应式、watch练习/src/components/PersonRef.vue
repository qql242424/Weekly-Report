<template>
  <div class="person-ref">
    <h2 ref="title">人</h2>
    <button @click="printTitle">打印标题</button>
  </div>
</template>
<script setup lang="ts" name="PersonRef">
//与dom标签有关的内容
import { ref } from 'vue'
let title = ref()
function printTitle() {
  console.log(title.value)
}
//与组件有关的内容
let name = '王五'
let age = 28
defineExpose({ name })
</script>
<style scoped>
.person-ref {
  background-color: lightgreen;
  border-radius: 10px;
  box-shadow: 0 0 10px;
  padding: 20px;
  margin: 10px;
}
</style>
