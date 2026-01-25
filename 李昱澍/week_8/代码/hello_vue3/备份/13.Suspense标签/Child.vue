<template>
  <div class="child">{{ data.hitokoto }}</div>
</template>

<script setup lang="ts" name="Child">
import axios from 'axios'
let { data } = await axios.get('https://v1.hitokoto.cn')
</script>

<style scoped>
.child {
  border: 1px solid #000;
  border-radius: 5px;
  background-color: pink;
  padding: 5px;
}
</style>
