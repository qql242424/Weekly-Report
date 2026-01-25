<!-- v-model -->
<template>
  <div class="child2">
    <!-- 组件间的v-model -->
    <input
      type="text"
      :value="modelValue"
      @input="emit('update:modelValue', (<HTMLInputElement>$event.target).value)"
    />
  </div>
</template>

<script setup lang="ts" name="Child2">
defineProps(['modelValue'])
const emit = defineEmits(['update:modelValue'])
</script>

<style scoped>
.child2 {
  background: linear-gradient(to right, rgb(255, 144, 144), rgb(209, 255, 209));
  border-radius: 15px;
  margin: 10px;
  padding: 10px;
}
input {
  border: 2px solid orange;
  border-radius: 8px;
  padding: 4px 8px;
  font-size: 16px;
  color: crimson;
  background-color: blanchedalmond;
}
</style>
