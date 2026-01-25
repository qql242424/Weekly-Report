<template>
  <button @click="isShow = true">我要弹窗</button>
  <teleport to="body">
    <div class="child" v-show="isShow">
      <h2>我是一个弹窗</h2>
      <p>我是弹窗中的一些内容</p>
      <button @click="isShow = false">关闭弹窗</button>
    </div>
  </teleport>
</template>

<script setup lang="ts" name="Child">
import { ref } from 'vue'
const isShow = ref(true)
</script>

<style scoped>
.child {
  border-radius: 5px;
  background-color: pink;
  padding: 5px;
  box-shadow: 0 0 10px;
  width: 200px;
  height: 160px;
  margin: 10px;
  position: fixed;
  text-align: center;
  left: 50%;
  margin-left: -100px;
  top: 10%;
}
</style>
