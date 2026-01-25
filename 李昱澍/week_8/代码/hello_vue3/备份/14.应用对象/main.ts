import { createApp } from 'vue'
import App from './App.vue'
const app = createApp(App)
app.directive('beauty', (element, { value }) => {
  element.innerText += value
  element.style.color = 'pink'
})

app.mount('#app')
