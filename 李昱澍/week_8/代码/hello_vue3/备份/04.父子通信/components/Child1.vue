<!-- props -->
<template>
  <div class="child1">
    <b>a：</b>{{ a }}
    <button @click="add">a+1</button>
  </div>
</template>

<script setup lang="ts" name="Child1">
let { a, add } = defineProps(['a', 'add'])
console.log(a)
</script>

<style scoped>
.child1 {
  background: linear-gradient(to right, rgb(255, 144, 144), rgb(209, 255, 209));
  border-radius: 15px;
  margin: 10px;
  padding: 10px;
}
</style>
