<template>
  <div class="car">
    <h1>这是车</h1>
    <ul>
      <li v-for="c in cars" :key="c.id">一辆{{ c.type }}车</li>
    </ul>
    <button @click="changeType">更改第一辆车的品牌</button>

    <h2>测试：{{ obj.a.b.c }}</h2>
    <button @click="test">测试</button>
  </div>
</template>
<script setup name="Car" lang="ts">
import { reactive, ref } from 'vue'

let cars = reactive([
  { id: 'baoma', type: '宝马高端汽' },
  { id: 'benchi', type: '奔驰高端汽' },
])

function changeType() {
  cars[0]!.type = '金箭电动'
}

let obj = ref({ a: { b: { c: 666 } } })

function test() {
  obj.value.a.b.c = 999
}
</script>
<style scoped>
.car {
  background-color: pink;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 0 10px;
  margin: 10px;
}
</style>
