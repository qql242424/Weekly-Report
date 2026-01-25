<template>
  <div class="sentence">
    <b>莫名其妙的句子：</b>
    <ul>
      <li v-for="s in sentenceList" :key="s.id">{{ s.content }}</li>
    </ul>
    <button @click="getASentence">再来一句</button>
  </div>
</template>

<script setup lang="ts" name="Sentence">
import { useSentenceStore } from '@/store/sentence'
import { storeToRefs } from 'pinia'
let sentenceStore = useSentenceStore()
const { getASentence } = sentenceStore
let { sentenceList } = storeToRefs(sentenceStore)

sentenceStore.$subscribe((mutation, state) => {
  localStorage.setItem('sentenceList', JSON.stringify(state.sentenceList))
})
</script>

<style scoped></style>
