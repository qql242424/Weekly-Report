import { reactive } from 'vue'
import axios from 'axios'
export default function () {
  let DogList = reactive<string[]>([])
  async function getDog() {
    try {
      let dog = await axios.get('https://dog.ceo/api/breed/pembroke/images/random')
      DogList.push(dog.data.message)
    } catch (error) {
      alert(error)
    }
  }
  return { DogList, getDog }
}
