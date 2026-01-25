//引入
import { createApp } from 'vue'
import App from './App.vue'
import { createPinia } from 'pinia'
//创建应用对象
const app = createApp(App)
const pinia = createPinia()
app.use(pinia)
//挂载
app.mount('#app')
