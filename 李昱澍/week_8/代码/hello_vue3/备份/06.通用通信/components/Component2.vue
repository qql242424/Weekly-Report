<template>
  <div class="component2">
    <h3>组件2</h3>
    <b>a：</b>{{ a }}
    <br />
    <!-- <button @click="addA">a+1</button> -->
    <hr />

    <b>b：</b>{{ b }}
    <br />
    <button @click="addB">b+1</button>
  </div>
</template>

<script setup lang="ts" name="Component2">
//aContext
import { ref } from 'vue'
import emitter from '@/utils/emitter'
import { onUnmounted } from 'vue'
const a = ref(0)

emitter.on('send-a', (value: any) => {
  a.value = value
})
onUnmounted(() => {
  emitter.off('send-a')
})

//bContext
import { useBStore } from '@/stores/b'
import { storeToRefs } from 'pinia'
const bStore = useBStore()
const { addB } = bStore
const { b } = storeToRefs(bStore)
</script>

<style scoped>
.component2 {
  background: linear-gradient(to left, pink, rgb(199, 255, 199));
  border-radius: 15px;
  margin: 10px;
  padding: 10px;
  width: 45%;
}
h3 {
  text-align: center;
  background-color: rgb(240, 248, 255, 0.5);
}
</style>
