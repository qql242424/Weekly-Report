<template>
  <div class="component1">
    <h3>组件1</h3>
    <b>a：</b>{{ a }}
    <br />
    <button @click="sendA">把a传给组件2</button>
    <button @click="addA">a+1</button>
    <hr />

    <b>b：</b>{{ b }}
    <br />
    <button @click="addB">b+1</button>
  </div>
</template>

<script setup lang="ts" name="Component1">
import { ref } from 'vue'
//aContext
import emitter from '@/utils/emitter'
let a = ref(1)
function sendA() {
  emitter.emit('send-a', a.value)
}
function addA() {
  a.value++
  sendA()
}
// bContext
import { useBStore } from '@/stores/b'
import { storeToRefs } from 'pinia'
const bStore = useBStore()
const { addB } = bStore
const { b } = storeToRefs(bStore)
</script>

<style scoped>
.component1 {
  background: linear-gradient(to right, pink, rgb(199, 255, 199));
  border-radius: 15px;
  margin: 10px;
  padding: 10px;
  width: 45%;
}
h3 {
  text-align: center;
  background-color: rgb(240, 248, 255, 0.5);
}
button {
  margin: 5px;
}
</style>
