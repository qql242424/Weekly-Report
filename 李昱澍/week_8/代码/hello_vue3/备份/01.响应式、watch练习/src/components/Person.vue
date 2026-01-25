<template>
  <div class="person">
    <h1>这是人</h1>
    姓名：{{ name }}
    <button @click="changeName">改名</button>
  </div>
</template>
<script setup name="Person" lang="ts">
import { ref } from 'vue'
let name = ref('张三')
function changeName() {
  if (name.value === '李四') name.value = '张三'
  else name.value = '李四'
}
</script>
<style scoped>
.person {
  background-color: skyblue;
  box-shadow: 0 0 10px;
  border-radius: 10px;
  padding: 20px;
  margin: 10px;
}
</style>
