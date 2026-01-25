<template>
  <div class="grandchild">
    <h3>孙组件</h3>
    <div v-if="show1">
      <b>a：</b>{{ a }}
      <br />
      <button @click="addA">a+1</button>
    </div>
    <div v-if="!show1">
      <b>b：</b>{{ b }}
      <br />
      <button @click="addB">b+1</button>
    </div>
  </div>
</template>

<script setup lang="ts" name="Grandchild">
import { inject } from 'vue'
defineProps(['a', 'addA', 'show1'])
let { b, addB } = inject('bContext', { b: 0, addB: () => {} })
</script>

<style scoped>
.grandchild {
  background: whitesmoke;
  border-radius: 15px;
  margin: 10px;
  padding: 10px;
}
</style>
