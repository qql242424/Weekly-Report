<template>
  <div id="app">
    <h2>路由练习</h2>
    <!-- 导航区 -->
    <div class="navigate">
      <RouterLink class="link" to="/home">主页</RouterLink>
      <RouterLink class="link" to="/news">新闻</RouterLink>
    </div>
    <!-- 展示区 -->
    <div class="content">
      <RouterView> </RouterView>
    </div>
  </div>
</template>

<script setup lang="ts" name="App">
import { RouterLink, RouterView } from 'vue-router'
</script>

<style scoped>
#app {
  border-radius: 15px;
  background-color: pink;
  padding: 10px;
  box-shadow: 0 0 10px;
}
.content {
  background: linear-gradient(to right, rgb(255, 144, 144), rgb(209, 255, 209));
  border-radius: 15px;
  width: 100%;
  height: 700px;
}
.link {
  text-decoration: none;
  margin: 3px;
  padding: 1px;
  border-radius: 8px;
  background-color: rgb(255, 254, 192);
  color: black;
}
</style>
