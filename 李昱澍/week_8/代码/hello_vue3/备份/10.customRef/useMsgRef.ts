import { customRef } from 'vue'
let timer: number
export default function (initValue: string, delay: number) {
  let msg = customRef((track, trigger) => {
    return {
      get() {
        track()
        return initValue
      },
      set(value) {
        clearTimeout(timer)
        timer = setTimeout(() => {
          initValue = value
          trigger()
        }, delay)
      },
    }
  })
  return msg
}
