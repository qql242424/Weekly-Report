<!-- 自定义事件 -->
<template>
  <div class="child5">
    <b>子组件的数据e1：</b>{{ e1 }}
    <br />
    <button @click="emit('sendE', e1)">将子组件的e1发送给父组件的e</button>
    <button @click="emit('addE')">e+1</button>
    <button @click="addE1">e1+1</button>
  </div>
</template>

<script setup lang="ts" name="Child5">
const emit = defineEmits(['sendE', 'addE'])
import { ref } from 'vue'
let e1 = ref(999)
function addE1() {
  e1.value++
}
</script>

<style scoped>
.child5 {
  background: linear-gradient(to right, rgb(255, 144, 144), rgb(209, 255, 209));
  border-radius: 15px;
  margin: 10px;
  padding: 10px;
}
button {
  margin: 5px;
}
</style>
