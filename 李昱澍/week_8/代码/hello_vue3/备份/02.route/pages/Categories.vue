<!-- 练习query参数 -->
<template>
  <div class="categories">
    <h5>id：{{ id }}</h5>
    <h5>content：{{ content }}</h5>
    <h5>text：{{ text }}</h5>
  </div>
</template>

<script setup lang="ts" name="Categories">
let { id, content, text } = defineProps(['id', 'content', 'text'])
</script>

<style scoped></style>
