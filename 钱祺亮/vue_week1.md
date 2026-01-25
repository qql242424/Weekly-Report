# vue

* vue2与vue3
  * 一个是OptionAPI，一个是CompositionAPI，vue2的api时配置风格的，data，function和watch都是明确分开的，要想扩展一个新功能就要在各自的位置去设计代码，一个功能被分成多个应用区域，而vue的api时组合风格的，在设计或者扩展一个新功能时候就可以在一个连续的区域，类似于一个大的function去扩展一个新功能。
  * 为什么选择vue3（各有优缺，只是vue3更贴近现在罢了）
    * 配置风格不便于维护和复用；
    * 组合式缺点是风格多样化，对于不同的人来说不规范，优点是方便配置。方便复用。

## setup

* setup是vue3中的一个新的配置项，值是一个函数。
* console.log(this)，setup()函数里的this是underfined，所以说不能用this.name来表示该方法内的name变量来和引入的变量name进行区分了。
* setup返回值也可能是一个渲染函数。
* setup和vue2中的data，methods
  * 可以同时存在；
  * data可以通过this关键词去读到setup里的元素，因为setup的生命周期比data早，而且要注意要用this关键词去调用，否则调用无效。

```js
  data(){
    return {
        a:100,
        c:this.name//必须要有this
    }
  },
  methods:{
    b(){
        console.log('b')
    }
  },
  setup(){
    let name = '张三'
    let age = 18
  }
```

* 不能在setup里面去试图调用data里的元素，不能从旧的vue2的语法里去调用在vue3的语法里。
* 没有在setup里交出的元素，在html里是拿不到的。

```js
<script lang="ts" setup>//表明语言是ts，可以替代setup()
    let a = 10
</script>
```

* 有两个setup的script标签，一般来说一个是来说明组件名字的，一个是用来配置vue3组件的。（也可以通过一个插件来实现对插件文件名字的修改，现版本已经无需插件了，直接使用）  

## 响应式数据

* 在vue2里，把数据放在data，就是响应式数据（数据代理和数据劫持），vue3中则是ref。
* ref定义基本类型数据

```js
import {ref} from vue
let name = ref("张三")
let age = ref(18)//这样就可以把这个元素变成一个类似于对象。然后就可以实现响应式。数据就是动态的了。
```

* reactive定义对象类型数据

```js
<script lang = 'ts' setup name = 'person'>
  let car = reactive({brand : "奔驰" ， price : 100})_
 {/* 跟ref()很像 */}

  function changePrime(){
    car.price += 10;
  }
</script>
```

* 原对象在经过响应式处理后就变成了响应式数据  
* ref也可以对象类型的响应式数据，表面上是ref实现的，但实际上是使用的reactive来实现的。
* 区别
  * ref创建的变量必须使用.value（可以使用volar插件自动添加.value）
  * reactive重新分配一个新对象，会失去响应式。
    * 在需要修改很多性质时，我们常常不能把每一个都去改，也不能直接让reactive对象指向一个普通的json，也不能把json包上reactive。

```js
function(){
  //car = {brand:'奥托',price:1}//这么写页面不刷新
  //car = reactive({brand:'奥托',price:1})//这么写页面也不刷新
  Object,assign(car,{brand:'奥托',price:1})//正确写法,是覆盖上一个属性
}
```

* ref是直接可以改的

```js
car.value = ({brand:'奥托',price:1})//不管如何修改，始终是ref响应式
```

***实际开发时全是ref，层级太高的话就得用reactive，只是.value影响代码整洁***

* toRefs的作用就是把一个reactive作用的对象变成多个ref作用的对象

```js
let person = {
  name = '张三',
  age = 18
}
let {name,age}=toRefs(person)//这样的话就可以直接像ref那样通过.value来修改响应式数据了。
```
