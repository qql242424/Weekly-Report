<template>
  <div class="sum">
    <b>Sum：</b>
    {{ sum }}
    <br />
    <b>Sum*10：</b>
    {{ Sum10 }}
    <br />
    <button @click="addSum">Sum+1</button>
  </div>
</template>

<script setup lang="ts" name="Sum">
import { useSumStore } from '@/store/sum'
import { storeToRefs } from 'pinia'
let sumStore = useSumStore()
let { sum, Sum10 } = storeToRefs(sumStore)
function addSum() {
  sum.value += 1
}
sumStore.$subscribe((mutate, state) => {
  console.log(`sumStore变化了,变化信息`, mutate, `新的sumStore:`, state)
})
</script>

<style scoped></style>
