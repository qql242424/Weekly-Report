import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/pages/Home.vue'
import Categories from '@/pages/Categories.vue'
import News from '@/pages/News.vue'
import Details from '@/pages/Details.vue'
let router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      name: 'zhuye',
      path: '/home',
      component: Home,
      children: [
        {
          name: 'fenlei',
          path: 'categories',
          component: Categories,
          props(route) {
            return route.query
          },
        },
      ],
    },
    {
      name: 'xinwen',
      path: '/news',
      component: News,
      children: [
        {
          name: 'xiangqing',
          path: 'detail/:id/:title/:content',
          component: Details,
        },
      ],
    },
    {
      path: '/',
      redirect: '/home',
    },
  ],
})
export default router
