<template>
  <div class="father">
    <h3>父组件</h3>
    <b>a：</b>{{ a }}
    <br />
    <button @click="addA">a+1</button>
    <Child id="1 . $attrs" :a="a" v-bind="{ x: 2 }" :addA="addA" :show1="t" />
    <b>b：</b>{{ b }}
    <br />
    <button @click="addB">b+1</button>
    <Child id="2 . provide和inject" />
  </div>
</template>

<script setup lang="ts" name="Father">
import Child from './Child.vue'
import { provide, ref } from 'vue'
let t = ref(true)
//子组件1
let a = ref(1)
function addA() {
  a.value++
}
//子组件2
let b = ref(1)
function addB() {
  b.value++
}
provide('bContext', { b, addB })
</script>

<style scoped>
.father {
  background: lightpink;
  border-radius: 15px;
  margin: 10px;
  padding: 10px;
}
button {
  margin: 5px;
}
</style>
