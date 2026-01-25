<template>
  <div class="details">
    <h5>id:{{ route.params.id }}</h5>
    <h5>title:{{ route.params.title }}</h5>
    <h5>content:{{ route.params.content }}</h5>
  </div>
</template>

<script setup lang="ts" name="Details">
import { useRoute } from 'vue-router'
let route = useRoute()
console.log(route)
</script>

<style scoped></style>
