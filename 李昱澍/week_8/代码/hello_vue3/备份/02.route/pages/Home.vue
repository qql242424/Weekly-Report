<!-- 练习query参数 -->
<template>
  <div class="home">
    <!-- 导航区 -->
    <ul>
      <li v-for="c in categories" :key="c.id">
        <RouterLink
          class="link"
          :to="`/home/categories?id=${c.id}&content=${c.content}&text=${c.text}`"
          replace
          >{{ c.content }}
        </RouterLink>
      </li>
    </ul>
    <!-- 展示区 -->
    <span class="child">
      <RouterView></RouterView>
    </span>
    <!-- 编程式路由导航练习 -->
    <button @click="goNews">跳转到新闻</button>
  </div>
</template>

<script setup lang="ts" name="Home">
import { RouterLink, RouterView, useRouter } from 'vue-router'
const categories = [
  { id: 'asd1', content: '分类1', text: '111111111' },
  { id: 'asd2', content: '分类2', text: '222222222' },
  { id: 'asd3', content: '分类3', text: '333333333' },
]
let router = useRouter()
function goNews() {
  router.push('/news')
}
</script>

<style scoped>
.home {
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
