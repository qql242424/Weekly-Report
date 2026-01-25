<template>
  <div class="news">
    <!-- 导航区 -->
    <ul>
      <li v-for="d in details" :key="d.id">
        <RouterLink
          class="link"
          :to="{
            name: 'xiangqing',
            params: {
              id: d.id,
              title: d.title,
              content: d.content,
            },
          }"
          >{{ d.title }}</RouterLink
        >
      </li>
    </ul>
    <!-- 展示区 -->
    <span class="child">
      <RouterView></RouterView>
    </span>
  </div>
</template>

<script setup lang="ts" name="News">
import { RouterLink, RouterView } from 'vue-router'
const details = [
  { id: 'qwe1', title: '1号新闻', content: '111' },
  { id: 'qwe2', title: '2号新闻', content: '222' },
  { id: 'qwe3', title: '3号新闻', content: '333' },
]
</script>

<style scoped>
.news {
  margin: 10px;
  padding: 10px;
}
.link {
  text-decoration: none;
  color: greenyellow;
}
.child {
  display: block;
  margin-top: 20px;
  background-color: aliceblue;
  border-radius: 10px;
  padding: 10px;
  height: 300px;
}
</style>
