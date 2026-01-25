<!-- $refs和$parent -->
<template>
  <div class="child3">
    <b>孩子的数据c1:</b> {{ c1 }}
    <br />
    <b>父亲的数据c：</b>{{ (<any>$parent).c }}
    <br />
    <button @click="changeC($parent)"> 更改父亲的数据c为999 </button>
  </div>
</template>

<script setup lang="ts" name="Child3">
import { ref } from 'vue'
let c1 = ref(100)
defineExpose({ c1 })
function changeC(parent: any) {
  parent.c=999
}
</script>

<style scoped>
.child3 {
  background: linear-gradient(to right, rgb(255, 144, 144), rgb(209, 255, 209));
  border-radius: 15px;
  margin: 10px;
  padding: 10px;
}
button {
  margin: 5px;
}
</style>
