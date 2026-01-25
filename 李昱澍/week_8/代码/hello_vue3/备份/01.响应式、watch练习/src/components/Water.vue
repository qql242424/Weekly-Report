<template>
  <div class="water">
    <h1>这是水</h1>
    室温达到50℃，或水位达到20cm，立刻联系服务器 <br />
    水温达到100，或水位达到50，取消监视
    <h2 id="demo">水温：{{ temp }}</h2>
    <h2>水位：{{ height }}</h2>
    <button @click="changeTemp">水温+10</button>
    <button @click="changeHeight">水位+10</button>
  </div>
</template>

<script lang="ts" setup name="Water">
// 室温达到50℃，或水位达到20cm，立刻联系服务器
// 水温达到100，或水位达到50，取消监视

import { ref, watchEffect } from 'vue'

let temp = ref(0)
let height = ref(0)

function changeTemp() {
  temp.value += 10
}
function changeHeight() {
  height.value += 1
}

const stopWatch = watchEffect(() => {
  if (temp.value >= 50 || height.value >= 20) {
    console.log(document.getElementById('demo')?.innerText)
    console.log('联系服务器')
  }
  if (temp.value === 100 || height.value === 50) {
    console.log('清理了')
    stopWatch()
  }
})
</script>
<style scoped>
.water {
  background-color: lightyellow;
  border-radius: 10px;
  box-shadow: 0 0 10px;
  padding: 20px;
  margin: 10px;
}
button {
  margin-right: 10px;
}
</style>
