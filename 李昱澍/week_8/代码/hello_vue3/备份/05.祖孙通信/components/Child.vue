<template>
  <div class="child">
    <h3>子组件{{ id }}</h3>
    <p v-show="$attrs.show1">经过中间组件的数据：{{ $attrs }}</p>
    <Grandchild v-bind="$attrs" />
  </div>
</template>

<script setup lang="ts" name="Child">
import Grandchild from './Grandchild.vue'

defineProps(['id'])
</script>

<style scoped>
.child {
  background: pink;
  border-radius: 15px;
  margin: 10px;
  padding: 10px;
}
</style>
