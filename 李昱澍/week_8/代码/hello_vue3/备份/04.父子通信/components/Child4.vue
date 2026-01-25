<!-- slot -->
<template>
  <div class="child4">
    <h4>{{ title }}</h4>
    <slot></slot>
    <slot name="s1"></slot>
    <slot name="s2" :d="d"></slot>
  </div>
</template>

<script setup lang="ts" name="Child4">
import { reactive } from 'vue'
defineProps(['title'])
let d = reactive([
  { id: 'asd`1', content: '123' },
  { id: 'asd`2', content: '456' },
  { id: 'asd`3', content: '789' },
])
</script>

<style scoped>
.child4 {
  background: linear-gradient(to right, rgb(255, 144, 144), rgb(209, 255, 209));
  border-radius: 15px;
  margin: 10px;
  padding: 10px;
  width: 30%;
}
h4 {
  text-align: center;
  color: thistle;
  font-size: 18px;
  background-color: rgb(240, 248, 255, 0.8);
}
</style>
