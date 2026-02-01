# vue

* vue2与vue3
  * 一个是OptionAPI，一个是CompositionAPI，vue2的api时配置风格的，data，function和watch都是明确分开的，要想扩展一个新功能就要在各自的位置去设计代码，一个功能被分成多个应用区域，选项所定义的属性都会暴露在函数内部的this上，它会指向当前的组件实例。而vue的api是组合风格的，在设计或者扩展一个新功能时候就可以在一个连续的区域，类似于一个大的function去扩展一个新功能。
  * 为什么选择vue3（各有优缺，只是vue3更贴近现在罢了）
    * 配置风格不便于维护和复用；
    * 组合式缺点是风格多样化，对于不同的人来说不规范，优点是方便配置。方便复用。

## 单文件组件

vue的单文件组件会将一个组件的逻辑（JS），模板（HTML）和样式（CSS）封装在同一个文件里。

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
    * 在需要修改很多性质时，我们常常不能把每一个都去改，也不能直接让reactive对象指向一个普通的对象，也不能把对象包上reactive。

```js
function(){
  //car = {brand:'奥托',price:1}//这么写页面不刷新
  //car = reactive({brand:'奥托',price:1})//这么写页面也不刷新
  Object.assign(car,{brand:'奥托',price:1})//正确写法,是覆盖上一个属性
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
let {name,age}=toRefs(person)//这样的话就可以直接像ref 那样通过.value来修改响应式数据了。
```

### 计算属性

通过以下代码，让fullName变成一个可读取可修改的变量

```js
let fullName = computed({
  //被获取时进行的操作
  get(){
    return ...//你想进行的操作，别忘了如果是ref，要在变量后加上.value
  }
  //被修改时进行的操作，set里面必须要有一个参数
  set(val){
    //你想进行的操作，别忘了.value
  }
})
```

## watch监视

* 作用：监视数据的变化
* 特点：只能监视以下四种数据
  * ref定义的数据
  * reactive定义的数据
  * 函数返回一个值（一个getter函数）
  * 一个包含上述内容的数组
* 情况：
  * 监视ref定义的基本类型的数据
  * 监视ref定义的对象类型的数据
  * 监视reactive定义的对象类型的数据

```js
// 监视参数不用加.value，因为只能监视ref定义的数据，不能监视ref定义的数据的value，会有警告，也不能使用。
watch(){sum,(newValue,oldValue)=>{
  console.log(...)
},{deep:ture,immediate:ture}}

// 监视参数为一个对象时，因为监视的其实是对象的地址值，所以如果只改变其中的属性的话，oldValue是和newValue没区别的，因为都是一个对象，都在一个地方，如果改变的是ref定义的对象，那么区别就会有所体现
watch(){sum,(newValue,oldValue)=>{
  console.log(...)
},{deep:ture,immediate:ture}}
```

***在实际开发中，一般通过只在watch参数中写value来规避新旧值相同的处境。***

* 监视reactive定义的对象类型的数据，默认开启深度监视  
* 若监视的是ref或者reactive定义的对象类型中的某个属性
  * 不是对象类型，就要用getter函数，即`()=>person.name`
  * 是对象类型时，推荐写成函数式，如果直接写的话，在不改变整个对象（就是不改变对象的地址值时），是可以观察到细枝末节的改变的，但是无法观察到整个对象的改变，而且old=new，因为watch直接观察的就是地址值。如果写成函数式，就可以观察到整个对象的变化，（注意这里的深度监视需要手动添加`{deep:ture}`）。
* watchEffect实现
  * 在打开后就会先监视一下，直接写.value，实现全自动监视，性能可能会差一点（其实可以忽略）

***  

## v-xx

* v-bind 使用 v-bind: ,简写为 : 的方式来放在html里来绑定样式
* v-on 使用 v-on: , 简写为 @ 的方式来放在html属性里来绑定渲染
* v-if v-else if v-else
* v-for
  * item in items 的特殊语法，可以完整的访问父作用域内的属性和变量，也支持使用可选的第二个参数表示当前项得到位置索引
  * 可以多层嵌套
  * 可以用of代替in
  * 可以用v-for来遍历一个对象的所有属性，遍历的顺序会基于对该对象调用object.values()的返回值决定
    * 可以提供第二个属性表示属性名
    * 第三个参数表示位置索引
  * v-for使用整数值时，会从1开始遍历到n（那个整数值）
  * 可以在`<template>`标签上使用v-for，多用于v-if与v-for在同一节点时的情况，因为v-if的优先级比v-for高，所以说v-if无法访问到v-for作用域内定义的变量别名，常常使用`<template>`上先使用v-for，然后在`<li>`或者`<ul>`上使用v-if
  * 通过key来管理，重用和重新排序现有的元素。（没懂，等到后面复习的时候再看看，不知道何意为）

***局部样式`<style scoped>`保证样式只服务本.vue,不会和其他vue搞混***

## 标签里的ref

```js
<h2 ref='title2'>qql</h2>

import {ref} from 'vue'

let title2 = ref()

function showH2(){
  console.log(title2.value)
}
```

***

## 生命周期钩子

* 每个vue组件实例在创建时都需要经理一系列的初始化步骤，在此过程中会运行生命周期钩子的函数，在特定阶段运行自己的代码
* onMounted钩子可以用来在组件完成初始渲染并创建dom节点后运行代码，还有其他钩子，在实例生命周期的不同阶段被调用，比如onUpdated和onUnmounted



