import { defineStore } from 'pinia'
import axios from 'axios'
interface Sentence {
  id: string
  content: string
}
export const useSentenceStore = defineStore('sentence', {
  state() {
    return {
      sentenceList:
        JSON.parse(localStorage.getItem('sentenceList') as string) || ([] as Sentence[]),
    }
  },
  actions: {
    async getASentence() {
      let {
        data: { uuid: id, hitokoto: content },
      } = await axios.get('https://v1.hitokoto.cn')
      let s = { id, content }
      this.sentenceList.push(s)
    },
  },
})
