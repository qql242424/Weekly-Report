# （一）基础知识
## 一、简介
1. 2020年9月18日官方发布 地址：[Release v3.0.0 One Piece · vuejs/core](https://github.com/vuejs/core/releases/tag/v3.0.0)
2. 性能提升：打包大小减少、初次渲染与更新渲染都快、内存占用少。
3. 源码升级：使用Proxy代替defineProperty实现响应式、重写虚拟DOM的实现和Tree-Shaking。
4. TS支持：更支持TS。
5. 新特性：

① Composition API（组合式API）：setup、ref与reactive、computed、watch

② 新的内置组件：Fragment、Teleport、Suspense

③ 其他改变：新的生命周期钩子、data 选项应始终被声明为一个函数、移除keyCode支持作为v-on的修饰符

## 二、一些基本要求
1. 创建vue3工程：推荐基于 vite 创建。

vite是新一代前端构建工具，**官网：**[https://vitejs.cn](https://vitejs.cn/)、[官方文档](https://cn.vuejs.org/guide/quick-start.html#creating-a-vue-application)

优势：启动快、对TypeScript和CSS等支持开箱即用、按需编译，不用等整个应用编译完成。

<font style="background-color:#FBE4E7;">具体操作：终端中，目标目录下 npm create vue@latest</font>

<font style="color:#8A8F8D;">（也可基于vue-cli创建）</font>

2. Vue3兼容Vue2语法，且对根标签（最外层包裹的唯一标签）的数量没有任何限制（2要求有且只有一个）
3. vue文件内可写三种标签：<template>写html结构、<style>、<script> 建议声明为ts（在后面加lang = 'ts'，内部依旧可以写js代码）

【template内】

① 插值表达式；{{变量名}}将脚本中的变量直接加入html中。如果想要实现双向绑定：

② 绑定事件：`<button @click="函数名">按钮提示<button/>`的方式为按钮绑定事件

## 三、vue3自身结构概述
1. **文件分层详解**

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2025/png/60403056/1767180609986-eab6673c-ddf8-4453-951a-48ba9cccb967.png)

【要点】

（1）index.html是Vite项目的入口文件，在项目最外层。

（2）加载index.html后，Vite解析<script type="module" src="/src/main.ts"></script>所指向的脚本。

（3）通过createApp函数创建一个应用实例。

2. **App.vue和main.ts的详细代码**

```vue
<!-- App.vue -->
<template>
  <div class="app">
    <h1>Hello,vue</h1>
  </div>
</template>
<script setup lang="ts" name="App"></script>
<!-- vue2写法：
<script lang="ts">
  export default {//默认暴露，提供接口
    name:'App' //组件名
  }
</script> -->
<style>
  .app {
    background-color: pink;
    box-shadow: 0 0 10px;
    border-radius: 10px;
    padding: 20px;
  }
</style>
```

```vue
import {createApp} from 'vue'//创建应用，相当于花盆。vue表示vue库。
import App from './App.vue'//引入App组件，相当于根基
createApp(App).mount('#app')
//前半部分：以App为根组件创建应用（将根种到花盆里）。
//后半部分：将应用放置于id为app的地方（把花盆摆放到某位置）。mount表示挂载。
```

3. **components文件夹内书写其他组件与引入**

书写组件时，要在ts中通过name属性暴露组件名。（vue3不用了）

在根标签内，首先在template内加上组件名单标签，<font style="color:#8A8F8D;">如：<Person/>；</font>

再在script内进行引入，<font style="color:#8A8F8D;">如：import Person from './components/Person.vue'</font>

如果是vue2还要注册组件<font style="color:#8A8F8D;"> components:{Person}</font>，vue3不用。

# （二）核心语法
## 一、Composition组合式API
### 组合式API
Vue2是OptionsAPI（配置API），数据、方法、计算等分别分散在data、methods、computed等属性中。修改需求是要分别修改，不便于维护和复用。

而Vue3的API设计是组合风格的，用函数的方式将同一功能的数据、方法等组合，更简便。它是通过setup实现的。

### setup概述
Vue3中的一个新的配置项，是一个函数。

组件中所用到的数据、方法、计算属性、监视等均配置在setup中。

```vue
export default {
    name:'Person',
    setup(){
      let name = '张三'
      
      function changeName(){
        name = 'zhang-san' //注意：此时这么修改name页面是不变化的
        console.log(name)
      }
      
      return {name,changeAge}
    }
  }
```

【要点】

（1）模板只可以使用setup函数所返回对象的内容

（2）在函数中访问this是undefined

（3）setup函数最先执行，会在beforeCreate之前调用

### setup 的返回值
（1）若返回一个**对象**，则模板内可以使用对象中的属性、方法等

（2）若返回一个（渲染）**函数**，则可以通过该函数的返回值自定义渲染内容，例如：

```jsx
setup(){
  return ()=> '你好啊！'
}
```

此时直接在页面中渲染该函数的返回值，较少用

### setup 与 Options API 的关系
二者可以同时存在与使用，发生冲突时setup优先。

且setup是最早的生命周期，故配置api可以使用this读取到其内部的属性与方法；但setup内不能访问到配置api的内容。

### 使setup独立的语法糖
```vue
<!-- 在原有的script之外再编写一个有setup属性的script标签 -->
<script setup lang="ts">
  let name = '张三'
  function changName(){
    name = '李四'//注意：此时这么修改name页面是不变化的
  }
</script>
```

这样就不用管什么返回值了，在模板中都能用。

此时一个脚本只写setup，一个脚本单纯命名，略有不便，可以借助`vite`中的插件进一步简化:

Step01.`npm i vite-plugin-vue-setup-extend -D`

Step02.`vite.config.ts`内修改成为以下的代码：

```jsx
import { defineConfig } from 'vite'
import VueSetupExtend from 'vite-plugin-vue-setup-extend'

export default defineConfig({
  plugins: [ VueSetupExtend() ]
})
```

Step03.`<script setup lang="ts" name="Person">`，标签内写setup函数的内容，也不需要返回值了，十分方便。

这是一个项目级依赖，每次新建一个项目都要写一遍

## 二、响应式
### 基本数据类型：ref
之前的数据都是固定不变的，本处初步实现定义响应式变量。

**【实现方法】**

Step01.脚本标签内先用`import {ref} from 'vue'`引入ref

Step02.声明变量时写为`let 变量名 = ref(初始值)`。

Step03.除声明外，修改与使用响应式变量时均用`变量名.value`读取值。

**【要点】**

（1）脚本中操作数据需要.value，模板中不需要，直接使用即可。

（2）ref函数实际上返回一个 RefImpl 的实例对象，简称ref对象 或 ref，它的value属性才是响应式的。

```vue
<script setup lang="ts" name="Person">
  import {ref} from 'vue'

  let name = ref('张三')

  function changeName(){
    name.value = '李四'
  }
</script>
```

### 对象类型：reactive
reactive函数会返回一个Proxy的实例对象，即响应式对象。

**【语法】**`let 对象名= reactive(源对象)`

```vue
<template>
  <div class="game">
    <h2>游戏列表：</h2>
    <ul>
      <li v-for="g in games" :key="g.id">{{ g.name }}</li>
    </ul>
    //v-for：Vue内置指令，用于循环渲染列表。
    //结合后面的g in games遍历响应式数组games，为每项生成一个<li>标签
    //:key="g.id" 给循环生成的每一个 <li> 绑定唯一标识
    <h2>测试：{{obj.a.b.c.d}}</h2>
    <button @click="changeFirstGame">修改第一游戏</button>
    <button @click="test">测试</button>
  </div>
</template>
<script lang="ts" setup name="Game">
import { reactive } from 'vue'
  
let games = reactive([
  { id: 'game01', name: '英雄联盟' },
  { id: 'game02', name: '王者荣耀' },
])
let obj = reactive({a:{b:{c:666}}})

function changeFirstGame() {
  games[0].name = '流星蝴蝶剑'
}
function test(){
  obj.a.b.c = 999
}
</script>
```

**【要点】**

（1）reactive定义的响应式数据是深层次的，一直到最内层都是响应式。

（2）不是只能接受对象，对象类型的都可以（如数组等）

（3）ref接收的数据也可以是对象类型，不过其实内部调用的是reactive函数。

### ref与reactive的对比
（1）ref可以接收任意类型数据，reactiv只能定义对象类型。

（2）访问ref所创建变量的值必须使用.value（volar插件可设置自动添加.value），reactive直接用。

（3）reactive重新分配一个新对象，会**失去**响应式（可以使用`Object.assign(原响应式对象，新对象)`整体替换）。ref不会，可以直接赋值，即使赋常量依旧是响应式。

```vue
<script lang="ts" setup>
  let car = reactive({brand:"宝马"});
  function changeBrand(){
    car = reactive({brand:"奔驰"});
  }
</script>
//这种情况下执行完函数页面的显示也不会改变。
//将第3行整体替换为：
    //Object.assign(car,{brand:"奔驰"});即可
```

【选择原则】

基本类型必须使用ref，层级不深的响应式对象都可以，层级深的或表单较多用reactive。（ref也可以深层次，但是用的少）

### toRefs 与 toRef
将响应式对象中的属性转换为ref对象。二者功能一致，但toRefs可以批量转换。

此时响应式属性与响应式对象是双向绑定的，同时改变。

当对象属性数量较多时比较方便定义与访问。

```vue
<template>
  <div class="person">
    <h2>年龄：{{person.age}}</h2>
    <h2>性别：{{person.gender}}</h2>
    <button @click="changeAge">修改年龄</button>
    <button @click="changeGender">修改性别</button>
  </div>
</template>
<script lang="ts" setup name="Person">
  import {ref,reactive,toRefs,toRef} from 'vue'

  let person = reactive({name:'张三', age:18, gender:'男'})
    
  // 用toRefs将对象中的2个属性批量取出，且依然保持响应式的能力
  let {name,gender} =  toRefs(person)
  // 用toRef将对象中的age属性取出，且依然保持响应式的能力
  let age = toRef(person,'age')


  function changeAge(){
    age.value += 1
  }
  function changeGender(){
    gender.value = '女'
  }
</script>
```

### 标签的ref属性
用于注册模板引用。

+ 有点类似于局部变量。

所有组件最终都会加载到根组件中渲染，因此，如果组件a与b中，分别用相同的id 命名并使用了 某dom元素，二者使用的 均为 较早渲染的那个元素。

如果用ref代替id给dom加标签就不会有这种问题了。此时，脚本调用的只会是本组件内框架中的dom元素。

+ 同理，style后写上scoped，表示样式只作用于本组件内的模板。

【语法】**标签内**写`ref="ref值"`，**脚本内 **引入ref、`let ref值 = ref()`

【用法】

（1）用在普通标签上，得到 <u>本组件内唯一的</u>、<u>仅在本组件内使用的 </u>dom节点。

```vue
<template>
  <h2 ref="title">人</h2>
  <button @click="printTitle">打印标题</button>
</template>

<script setup lang="ts" name="PersonRef">
//与dom标签有关的内容
import { ref } from 'vue'
let title = ref()
function printTitle() {
  console.log(title.value)
  // 此处直接打印所有内容，即<h2>人</h2>
  // 此时title是一个ref变量，它的value属性才是所标记的内容
}

//与组件有关的内容
let name = '王五'
let age = 28
defineExpose({ name })// 此处name是name:name.value的简写
</script>
```

（2）用在组件标签上，得到组件实例对象。

此时父组件 可且仅可 访问子组件内用 <font style="background-color:#FBE4E7;">defineExpose</font> 暴露的内容

```vue
<template>
  <PersonRef ref="ren" />
  <button @click="printRen">打印人</button>
</template>
<script lang="ts" setup name="App">
  import PersonRef from './components/PersonRef.vue'
  import {ref} from 'vue'

  let ren = ref()

  function printRen(){
    console.log(ren)
    console.log(ren.value)
    //此处组件自动变成ref变量，必须用value才能访问整个组件内容。
    
    console.log(ren.value.name)
    //只有暴露过的内容才可被父组件访问,是不是响应式都无所谓

    console.log(ren.value.age)//undefined
  }
</script>
```

## 三、computed
**作用：**根据已有数据计算出新数据。

**语法：**computed本质是一个函数。

该函数的参数可为一个函数，参数函数的返回值即为数据。但此时得到的结果是只读的。

想要可以更改，则该函数的参数为一个对象

```vue
<template>
    姓：<input type="text" v-model="firstName"> <br>
    名：<input type="text" v-model="lastName"> <br>
      <!-- input标签中的value属性表示填入表单的值。
      用v-bind:value简写为:value可单向访问脚本中的变量
      用v-model:value简写为v-model实现与变量的双向绑定 -->
    全名：<span>{{fullName}}</span> <br>
    <button @click="changeFullName">直接更改全名</button>
</template>

<script setup lang="ts" name="App">
  import {ref,computed} from 'vue'

  let firstName = ref('zhang')
  let lastName = ref('san')

  let fullName = computed({
    get(){
      return firstName.value + '-' + lastName.value
    },
    set(val){
      firstName.value = val.split('-')[0]
      lastName.value = val.split('-')[1]
      //split函数进行分隔。 val.split('-')表示一个分割后的数组。
      //此外，val.split(0,1)表示截取第一个字母得到的字符串，val.split(1)表示除了首字母外的。
    }
  })

  function changeFullName(){fullName.value = 'li-si'} 
</script>
```

## 四、watch
监视数据的变化（和Vue2中的watch作用一致）。

### 语法
<font style="background-color:#FBE4E7;">watch（ 监视的变量 ， 回调函数  </font><font style="color:#8A8F8D;background-color:#FBE4E7;">[，配置对象] </font><font style="background-color:#FBE4E7;">）</font>

+ 所监视对象可能为：`ref`定义的数据、`reactive`定义的数据、返回一个值的`函数`（getter函数）<font style="color:#8A8F8D;">、一个响应式对象内的参数对象</font>或包含这些内容的`数组`
+ 回调函数有两个参数，分别是newValue和oldValue。

对于某个基本类型的数据，二者分别传输新、旧值；但如果监视的是对象类型的数据，只改变对象内属性时两个参数均为最新值，对象的地址改变时参数才会分别是新、旧对象。

+ 配置对象是一个对象，配置项以属性的形式存在。常用的有：开启深度监视`{deep:true}` 、立即执行（页面加载完成后先执行一下回调函数）`{immediate:true}` 

### 几种情况
（1）监视 **ref** 定义的数据

基本类型：直接写数据名即可，监视value的改变。

对象类型：也是直接写数据名，监视对象的地址值。若想监视对象内部的数据，要手动开启深度监视。

（2）监视 **reactive** 定义的数据

自动开深度监视，且无法关闭。由于无法整体赋新对象，新旧值永远相同。

（3）监视响应式对象类型的**某个属性**

若该属性值是基本类型，`所监视的对象`要写成函数形式 `() => 响应式对象.属性`。此时新旧值不同。

若该属性值仍为对象，`所监视的对象`可以写为：

对象名`响应式对象.属性对象`。此时默认关注属性变化，但整个对象变化时无法监视

更推荐函数形式，`() => 响应式对象.属性对象`。此时监视地址值，可手动开深度监视。

（4）监视上述的多个数据，可将它们放在一个**数组**内

### watchEffect
比较智能的自动监视函数。当需要监视的属性项目较多时使用，可以自动判断所监视的内容。

运行时，它会先<font style="color:rgba(0, 0, 0, 0.85);">立即执行一次回调函数。之后，每当追踪的数据变化时都会执行回调函数。它返回一个</font><font style="color:rgb(0, 0, 0) !important;">停止监听函数</font><font style="color:rgb(0, 0, 0);">，调用该函数可终止监听。</font>

> watch 要明确指出监视的数据
>
> watchEffect 不用明确指出，函数中用到哪些属性，就监视哪些
>

```vue
  // 需求：室温>=50℃，或 水位>=20cm 时联系服务器
  // 用watch实现
  watch([temp,height],(value)=>{
    const [newTemp,newHeight] = value
    if(newTemp >= 50 || newHeight >= 20){
      console.log('联系服务器')
    }
  })
  // 用watchEffect实现
  const stopWtach = watchEffect(()=>{
    if(temp.value >= 50 || height.value >= 20){
      console.log('联系服务器')
    }
    // 水温达到100，或水位达到50，取消监视
    if(temp.value === 100 || height.value === 50){
      console.log('取消监视')
      stopWtach()
    }
  })
```

## 五、props
### 前置ts知识
【TS文件内语法】

（1）定义接口：`<font style="color:#F1A2AB;">interface</font> 接口名 { 接口内容键值对 }`，其中键为所规定的变量名，值为数据类型且首字母小写。必须项键值对为`键 = 值`，可选项为`键 ?= 值`。只是对格式的限制，顺序不必相同

（2）定义自定义类型 ：`type 类型名 = 类型情况`，类型情况可能用到泛型（即用尖括号控制数据类型））

（3）想在外界文件中使用，均要暴露。

【vue文件内语法】

（1）引入接口与类型时均要加`type`关键字

（2）使用ts规范定义变量的格式为`变量名:规范名 = ...`

（3）遇到要响应的情况，更推荐`变量名 = reactive<规范名>(...)`的形式

```javascript
// 定义一个接口，限制每个Person对象的格式
export interface PersonInter {
   id:string //首字母不可大写
   name:string
   age:number
   }
// 定义一个自定义类型Persons
export type Persons = Array<PersonInter> //“泛型”，用尖括号表示可写的数据类型
// 等同于export type Persons = PersonInter[]
```

```vue
<script setup lang="ts" name="PersonTs">
import { type PersonInter, type Persons } from '@/types'
//@等价于src,整个vue工程内都可以这样简写
let person: PersonInter = {
  id: '001',
  name: '张三',
  age: 1,
}
//Persons相当于Array<PersonInter>
let personList = reactive<Persons>[
  { id: '002', name: '李四', age: 2 },
  { id: '003', name: '王五', age: 3 },
]
</script>
```

### props知识
prop即属性

（1）父组件向子组件传参：在框架内的子组件标签中直接写，如`a = "哈哈"`

（2）子组件接收参数：先引入defineProps，再用`defineProps(['传参变量名'])`接收。此时子组件模板中可以直接使用变量，但子组件脚本中无法使用。用let x = ...接收，则数组x内即为参数列表。

（3）需要注意的是，传参时变量前加：是v-bind:的简写，表示绑定表达式或vue数据。

```vue
<template>
	<Person :list="persons"/>
</template>
  
<script lang="ts" setup name="App">
  import Person from './components/Person.vue'
  import {reactive} from 'vue'
    import {type Persons} from './types'
  
    let persons = reactive<Persons>([
     {id:'e98219e12',name:'张三',age:18},
      {id:'e98219e13',name:'李四',age:19},
       {id:'e98219e14',name:'王五',age:20}
     ])
   </script>
```

```vue
<template>
<div class="person">
 <ul>
     <li v-for="item in list" :key="item.id">
        {{item.name}}--{{item.age}}
      </li>
    </ul>
   </div>
   </template>
  
<script lang="ts" setup name="Person">
import {defineProps} from 'vue'
import {type PersonInter} from '@/types'
  
  // 第一种写法：仅接收
// const props = defineProps(['list'])
  
  // 第二种写法：接收+限制类型
// defineProps<{list:Persons}>()
  
  // 第三种写法：接收+限制类型+指定默认值+限制必要性
let props = withDefaults(defineProps<{list?:Persons}>(),{
     list:()=>[{id:'asdasg01',name:'小猪佩奇',age:18}]
  })
   console.log(props)
  </script>
```

## 六、生命周期
均要先引入再使用

Vue组件实例创建时，会在合适时期调用特定函数，这些函数统称为<font style="color:#AD1A2B;">生命周期钩子</font><font style="color:#8A8F8D;">=生命周期函数=生命周期</font>

##### 【Vue2的生命周期】
创建：beforeCreate、created

挂载：beforeMount、mounted

更新：beforeUpdate、updated

销毁：beforeDestroy、destroyed

##### 【Vue3的生命周期】
创建：setup

挂载：onBeforeMount、<font style="background-color:#FBE4E7;">onMounted</font>

更新：onBeforeUpdate、<font style="background-color:#FBE4E7;">onUpdated</font>

卸载：<font style="background-color:#FBE4E7;">onBeforeUnmount</font>、onUnmounted

##### 【用法】
引入后，将想要执行的函数以 `生命周期函数的参数` 形式传入，如

`<font style="color:#8A8F8D;">onMounted(()=>{console.log('挂载完毕')})</font>`

## 七、自定义hook
本质是一个函数，将组合式api封装。实现代码复用, 使setup函数更清晰。

其中甚至可以写生命周期钩子，是实现配置式api的重要工具。

实现方式为：

Step01. 在hooks文件夹中创建一个use开头的ts文件

Step02. ts内暴露一个函数，在函数内封装数据与方法

Step03. 函数返回包含所有数据与方法的对象

Step04. 组件内引入use开头的该单词，直接解构=use单词（）后即可使用

```javascript
import {reactive,onMounted} from 'vue'
import axios from 'axios'

export default function(){
  let dogList = reactive<string[]>([])

  async function getDog(){
    try {
      let {data} = await axios.get('https://dog.ceo/api/breed/pembroke/images/random')
      dogList.push(data.message)
    } catch (error) {
      alert(error)
    }
  }
  // 挂载钩子
  onMounted(()=>{
    getDog()
  })
  return {dogList,getDog}
}
```

```vue
<template>
  <div id="app">
    <button @click="getDog">来一张小狗！</button>
    <hr />
    <img v-for="(u, index) in DogList" :key="index" :src="u" />
    //注意是小括号，顺序表示内容与编号
  </div>
</template>

<script setup lang="ts" name="App">
import useDog from './useDog'
let { DogList, getDog } = useDog()
</script>
```

# （三） 路由
## 一、基础概念
1. 路由route：对应关系

路由器router：多个路由的管理工具

2. 路由配置放在route文件夹内，路由组件放在 pages 或 views 内，一般组件放在 components 内。
3. 点击导航后视觉上“消失” 的路由组件，默认是被卸载了，需要时再挂载。

## 二、使用步骤
下载、路由规则、安装、使用

1. 先下载 ：npm i vue-router
2. 建立路由配置文件夹与文件src/route/index.ts。

引入路由创建和历史记录创建（createRouter和createWebHistory）

调用路由创建函数，传入对象作为参数。对象要有history属性（值为历史记录方法）和routes属性（值为一个对象数组，每个对象内又有path、component等属性）。调用结果返为router

```typescript
import {createRouter,createWebHistory} from 'vue-router'
import Home from '@/pages/Home.vue'

const router = createRouter({
  history:createWebHistory(),
  routes:[
    {
      path:'/home',
      component:Home
    }
  ]
})
export default router
```

3. main.ts中引入并安装路由router

```javascript
import router from './router/index'
app.use(router)//安装路由
```

4. 组件中使用时，要引入RouterLink和RouterView。

控制跳转处（导航栏）使用RouterLink双标签，标签内用to属性标明路径。

跳转展示处使用RouterView双标签标注。

```vue
<template>
  <div class="app">
    <h2 >Vue路由测试</h2>
    <!-- 导航区 -->
    <div class="navigate">
      <RouterLink to="/home" active-class="active">首页</RouterLink>
    </div>
    <!-- 展示区 -->
    <div class="main-content">
      <RouterView></RouterView>
    </div>
  </div>
</template>
<script lang="ts" setup name="App">
  import {RouterLink,RouterView} from 'vue-router'  
</script>
```



## 三、一些语法
### 路由器工作模式
##### history模式
history:createWebHistory()

url美观，不带有#，更接近传统的url。但需要服务端配合处理路径问题，否则刷新会有`404`错误。大部分面向客户网页都用这个。

##### hash模式
history:createWebHashHistory()

兼容性更好，不需要服务器端处理路径。但不太美观、SEO优化方面相对较差。一般是后台管理系统。

### to的两种写法
##### 字符串写法
直接写to，不加冒号

```vue
<RouterLink to="/home">主页</RouterLink>
```

##### 对象写法
要加冒号

```vue
<RouterLink :to="{path:'/home'}">Home</RouterLink>
```

### 命名路由
命名：配置文件内，route数组内每个对象内新增name属性，值即为名字

```javascript
routes:[{
    name:'zhuye',
    path:'/home',
    component:Home
  }]
```

作用：完全相当于路径，直接使用可简化跳转与传参。

```vue
<router-link :to="{name:'zhuye'}">跳转到主页</router-link>
```

### 嵌套路由
多层/，写了一层路由后还要继续跳转

Step01. 编写子路由组件

Step02. 在routes数组的某对象中使用children属性配置路由规则，路径开头的/不要写，直接写单词即可

Step03. 在父组件内写RouterLink时必须为完整路径、展示处写上RouterView

### 路由传参
参数的传递在RouterLink标签内的to属性内完成，均可用字符串和对象写法。

接收均要先引入。如果要解构一定要用toRefs（route）保存响应性

```javascript
import {useRoute} from 'vue-router'
const route = useRoute()
```

##### query参数
传参：字符串写法中，路径结尾用?引起参数列表，参数直接写作`键=值`格式，多个参数用&连接。

    对象写法，用值为对象的query配置项传递。

接收：route.query

##### params参数
params参数传递前要在路由规则中提前占位。

传参：字符串写法中，直接按照写好的规则写url。

    对象写法中，必须使用name配置项不能用path，值为对象的params配置项内传递各参数。

接收：route.params

### 路由的props配置
开启配置后，路由参数可以作为props传给组件。组件内只需用defineProps接收一下即可直接使用，比较方便。

开启本配置有三种方法，均在子路径内的route规则内写。

```javascript
//布尔值写法，只能传params参数
props:true
//函数写法，传递返回的对象中的键值对，一般搭配query参数使用
props(route){return route.query}
// 对象写法，把对象中的键值对作为props传递
props:{a:1,b:2,c:3}
```

### replace属性
本属性决定路由跳转时，浏览器历史记录的模式。

浏览器历史记录的两种写入方式：push追加历史记录（默认值）、replace替换当前记录。想要更改为replace只需在RouterLink标签内加上`replace`，即<RouterLink replace>

### 编程式导航
脱离RouterLink实现路由跳转

```javascript
import {useRoute,useRouter} from 'vue-router'

const route = useRoute()
const router = useRouter()
```

route.query或route.parmas传参，router.push或router.replace更改记录存储模式。

在函数内实现路由跳转：route.push(①)，①处写to可为的字符串或对象。

使用场景：条件跳转。

### 重定向
将特定的路径，重新定向到已有路由。

可以给网页指定初始页面用。写了下面的代码，进入页面直接跳转到home页。

```javascript
{ path:'/', redirect:'/home'}
```

# （四）pinia
一个状态管理工具。“状态”可以简单认为是数据，因此实际上用它存一些复用的数据。

## 一、搭建 pinia 环境
Step01. cmd中安装pinia：npm install pinia

Step02. 配置，main.ts内安装pinia

```typescript
import { createPinia } from 'pinia'
const pinia = createPinia()
app.use(pinia)
```

## 二、语法
### 数据存取
Stpe01. 先在src内新建store文件夹，store是pinia的具象化。它是pinia的使用场景。

（store是一个保存状态和业务逻辑的实体，每个组件都可以读取、写入它。它有三个概念：state、action、getter，分别相当于data、methods、 computed ）

其内部存储ts文件，文件名必须体现其内存放数据的类别。

Step02.  ts文件内先引入defineStore，再以store的形式定义并暴露要用到的数据。

defineStore（）第一个字符串参数充当id，一般与文件同名；

第二个参数为含state（函）、actions（对）和getter（对）的对象。而state函数依旧返回一个对象，对象内部的属性才是真正的数据。

返回值推荐hooks的命名形式。

```typescript
import {defineStore} from 'pinia'

export const useSumStore = defineStore('sum',{
  state(){
    return {
      sum:6
    }
  },
  actions:{},
  getters:{}
})
```

Step03.  组件内使用，先引入useXxxStore函数，再调用并赋值。

返回一个响应式对象，之前存的数据以ref的形式保留为一个属性键值对，直接用.调用即可。

> <font style="color:#F1A2AB;">reactive内的ref以及拆包过了，不用再.value就能用</font>
>

```vue
<template>
  <h2>当前求和为：{{ sumStore.sum }}</h2>
</template>

<script setup lang="ts" name="Count">
  import {useSumStore} from '@/store/sum'
  const sumStore = useSumStore()
</script>
```

### 数据修改
##### （1）直接修改
```typescript
sumStore.sum = 6
```

##### （2）patch方法批量修改
patch:碎片。参数为一个对象，键值对表示将哪些内容改为新值，没写的不会变。

```typescript
sumStore.$patch({
  sum:6
})
```

##### （3）使用action修改
可以编写一些复杂的业务逻辑，便于复用。

store内的数据和方法都可以直接用点访问、actions内访问state的数据用this代表store。

```javascript
  actions: {
    changeSum() {
        this.sum = 6
      }
    },
}
```

```javascript
sumStore.changeSum()
```

### getters
当state中的数据需处理后再使用时，可以使用getters配置。getters内引用state的数据不用this.而用state.

```javascript
getters:{
  bigSum:(state):number => state.sum *10,
  upperSchool():string{
    return this.school.toUpperCase()
  }
}
```

```javascript
const {increment} = sumStore
let {sum,school,bigSum,upperSchool} = storeToRefs(countStore)
```

## 二、几个函数
### storeToRefs
将store中state内的数据转为ref对象，需要先引入。

使用Vue提供的toRefs将转换参数store中的所有内容，开销较大。但pinia提供的storeToRefs只转换数据。

```vue
  import { useSumStore } from '@/store/sum'
  import { storeToRefs } from 'pinia'
    
  const sumStore = useSumStore()
  const {sum} = storeToRefs(sumStore)
```

### $subscribe
监听state及其变化。函数的参数为一个回调函数，参数函数有修改信息、数据两个参数。

```typescript
talkStore.$subscribe((mutate,state)=>{
  console.log('LoveTalk',mutate,state)
  localStorage.setItem('talk',JSON.stringify(state.talkList))
  //将talkList存在本地，这样刷新后(即使重启浏览器)依然可以显示原来的列表。
  //LocalStorage里只存储字符串，要将数组转为json
})
```

```typescript
state(){
  return {
    talkList:JSON.parse(localStorage.getItem('talkList') as string) || []
  }
}
actions:{
  async getATalk(){
    //连续解构赋值+重命名
    let {data:{content:title}} = await axios.get('')
    let obj = {id:nanoid(),title}
    this.talkList.unshift(obj)
  }
}
```

## 三、组合式写法
上面都是配置式写法，数据与方法分开写了。将共同实现一个功能的数据与方法放在一起就是组合式写法。

组合式写法中，将defineStore的第二个参数写为一个函数，函数的返回值为期待调用的数据与方法，函数内容以setup函数为标准写即可。

```typescript
export const useSumStore = defineStore('sum',()=>{
  let sum = ref(1)
  function changeSum(){
    sum = 6
  }
  return {sum,changeSum}
})
```

# （五）组件通信
组件通信即组件之间的数据传递。

**Vue3组件通信和Vue2的区别：**使用mitt代替事件总线、pinia替代vuex、.sync优化到v-model中、$listeners合并到$attrs中、删去$children。

**常见搭配形式：**

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/60403056/1768665256016-b9c42afd-5d2f-4214-8ab2-9ac1d6bd29d5.png)

**<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">props 父传子，emit子传父，v-model双向绑，refs 父控子，$parent 子控父，slot 传结构</font>**。

## 一、props
使用频率最高的一种通信方式，**父→子**。

Child标签写在父组件内，变量和函数均可传递。<font style="color:#8A8F8D;">eg.<Child :a="a" :add="add"/></font>

是复制传递，此时子组件中接受到的变量只有值且非响应式，无法在子组件中直接更改，必须借助父组件传来的方法。调用父组件方法时等同于直接在父组件内调用该方法。

## 二、v-model
父子互传。平时用不到，直接写即可；封装ui组件库时，在“子组件”内要用到。

1. html标签上的v-model

v-model的本质：双向绑定=两个单向绑定。动态值实现数据到页面，input事件实现页面到数据。

<input type="text" v-model="userName">相当于：

```vue
<input 
  type="text" 
  :value="userName" 
  @input="userName =(<HTMLInputElement>$event.target).value"
  //event：事件对象,target:事件源,<>断言相当于as，表示其不为null
>
```

2. 组件标签上的v-model

此时本质：:moldeValue ＋ update:modelValue事件。

<Child v-model="userName"/>相当于：

```vue
<Child :modelValue="userName" @update:modelValue="userName = $event"/>
```

在子组件中，分别用defineProps和defineEmits接收参数modelValue和事件update:modelValue(赋给emits)。

子组件内的input要拆成两个单向绑定：`<font style="color:#F1A2AB;background-color:#FBE4E7;">:value="modelValue"</font>`<font style="color:#F1A2AB;background-color:#FBE4E7;">+</font>`<font style="color:#F1A2AB;background-color:#FBE4E7;">@input="emits('update:modelValue',(<HTMLInputElement>$event.target).value"</font>`

3. 可以用v-model:a代替v-model从，从而更换value。此时modelValue改为a、事件改为update:a，即可在组件标签上双向绑定多个值。

## 三、$refs 与 $parent
$refs：所有ref标识过的DOM元素or组件实例。值为一个reactive对象，内部所有属性均为reactive对象，分别对应每个实例。

> <font style="color:#F1A2AB;">对象的遍历使用for (let key in refs){</font>
>
> <font style="color:#F1A2AB;">console.log(refs[key])</font>
>
> <font style="color:#F1A2AB;">}</font>
>

$parent：值为一个reactive对象，是父组件的实例对象，可用.访问已暴露的数据。

它们两个一般都作为参数传入方法中，从而操作子/父组件的数据

## 四、slot
### 默认插槽
**【使用场景】**

多个组件整体结构相同，但要填充的内容不同（甚至不是同一种形式，如有的要图有的要视频）

**【使用方法】**

子组件内，内容不同的填充区域加上slot双标签。可以写一些默认内容，没有被填充时会展示。

父组件内，以双标签的形式写子组件。两个标签内部的内容会自动转移到slot之间。

### 具名插槽
**【使用方法】**

子组件内的slot标签通过name属性命名。

父组件内借助v-slot属性。这个属性只能用在template或组件标签上。

放在组件标签上跟默认插槽一个效果，所以一般会写一个template双标签包住要放的内容，再使用v-slot属性给它一个与子组件内相同的名字。此时`v-slot="s1"`可以简写为`<font style="color:#DF2A3F;background-color:#FBE4E7;">#s1</font>`。

### 作用域插槽
**理解：**子组件的数据与交互均由自身维护，但结构由父组件决定

<font style="color:#8A8F8D;">比如调用两次基本框架相同的子组件，对于同一个数组，第一个使用有序列表，第二个为无序列表。</font>

**【使用方法】**子组件slot标签内传参，父组件template标签内使用v-slot="a"接受到一个名为a的变量，各属性即为各参数。

子组件slot标签同时完成命名与传参时，父组件内：`<font style="color:#F1A2AB;"><template v-slot:插槽名="形参名"></font>`

## 五、自定义事件
常用于子传父。

#### 【自定义事件】
**原生事件：   **事件名是特定的，<font style="color:#8A8F8D;">如click、mosueenter</font>；

原生事件的事件对象 $event 是一个包含事件相关信息的对象，内部有pageX、target、keyCode等属性。

**自定义事件：**事件名是任意自拟名称，多个单词用 <font style="background-color:#FBE4E7;"> - </font> 连接（使用kebab-case命名规则）

自定义事件的事件对象 $event 是调用emit时所提供的数据（即emit方法的第二个参数），可为任意类型。

#### 【如何进行通信】
子组件内声明事件名并赋值给emit，父组件内给子组件标签绑定事件与函数。再于父组件内写函数，函数的参数为emit通过第二个参数传递过来，即可实现子传父。

eg .  子组件脚本内，`<font style="color:#F1A2AB;background-color:#FBE4E7;">let emit = defineEmits(['a'])</font>`声明一个叫作a的自定义事件。之后即可使用`<font style="color:#F1A2AB;background-color:#FBE4E7;">emit('a'，参数)</font>`传递参数并触发。父组件内<Child @a=''方法名 />

## 六、$attrs 
祖传孙。

$attrs是一个对象，包含所有父组件传入的、未被defineProps接受的标签属性，祖传孙的过程中需要中介。

**【用法】**

父组件中：<Child :a="a" v-bind="{x：100}" :updateA="updateA"/>

    其中 v-bind="{x：100}"对象写法就相当于：x="100"

子组件中：<font style="color:#F1A2AB;background-color:#FBE4E7;"><GrandChild v-bind="$attrs"/></font>

孙组件中：使用defineProps([ 'a'，'x'，'updateA' ])解析出传递的数据与方法即可直接使用。

本质仍为复制与借用，可以认为是props的升级版本。

## 七、provide 与 inject
祖孙<u>直接</u>通信。

祖先组件中通过provide，后代组件中通过inject配置声明接收数据。二者都要先引入。

子组件中不用编写任何与之相关的内容。

**【用法】**

父组件中，<font style="color:#F1A2AB;background-color:#FBE4E7;">provide( 'xxxContext' ，{ 数据与方法列表 } )</font> 只传递一个内容时不用写成对象格式、id直接写该内容名即可。

孙组件中，<font style="color:#F1A2AB;background-color:#FBE4E7;">let { 数据与方法列表 } = inject( 'xxxContext' , { a : 0 , updateMoney:( )=>{} })</font>的格式接收。接收时一般要写上默认值。

依旧是一种复制。

## 八、mitt
可实现任意组件间通信，与消息的订阅与发布（`pubsub`）类似。都放在工具文件夹utils或tools内。

Step01. 安装:npm i mitt

Step02. 新建文件`src\utils\emitter.ts`

```javascript
import mitt from 'mitt'
// 调用mitt得到emitter，emitter能绑定与触发事件。
const emitter = mitt()
export default emitter
```

:::danger
emitter常用方法有：

emitter.on（ ' 事件名 ' ，函数）绑定事件，事件触发时调用该函数。

emitter.emit（‘事件名’[ , 参数 ]）触发事件。

emitter.off（‘事件名’）解绑事件。

emitter.all（）获取全部绑定事件。

:::

无论接发数据都要先引入emitter。

Step03. 接收数据的组件中进行绑定与解绑。

```typescript
emitter.on('send-a',(value)=>{a.value=value})

onUnmounted(()=>{
  emitter.off('send-a')
})
```

Step04. 提供数据的组件中负责触发事件

```javascript
function sendA(){ emitter.emit('send-a',a.value)}
//再设计一个按钮写“发送数据”。
```

只教了传数据，没教函数。

## 九、pinia
参照之前pinia的笔记

# （六）其它 API
## 一、浅层响应
只对顶层属性进行响应式处理。用法跟ref和reactive一致。

**【shallowRef】**基础数据响应本身的变动，对象数据只响应整体的变化不响应属性的变化

**【shallowReactive】**只响应顶层数据的变化（也可以整体变动，实际上仍是顶层数据的变化），不再响应深层的变化

**【作用】**避免了对每一个属性做响应式所带来的性能成本，加快对属性的访问，提升性能。

## 二、只读
均要先<font style="background-color:#FBE4E7;"> 引入 </font>再使用。

需要一个对象类型的参数（普通对象、ref响应式变量、reactive响应式变量均可），返回对象的只读形式。

**【readonly】**readonly(original)，完全无法更改（还会在控制台中发出警告）。创建不可变的状态快照 or 保护全局状态或配置不被修改。

**【shallowReadonly】**shallowReadonly(original)  只有顶层属性不可更改，对象内部的嵌套属性可变。

## 三、去响应
也需要先引入再使用。

**【toRaw】**

接受一个响应式对象参数，返回它的原始形式，原始形式不再是响应式的、不会触发视图更新。

临时读取而不引起代理访问/跟踪开销。

在需要将响应式对象传递给外部时，让它们收到普通对象，不建议持久引用。

**【markRaw】**接收一个对象类型的参数，返回一个永远无法被响应式处理的对象。一般用于一些引入的外部对象，如mockjs

## 四、customRef：自定义ref
使用场景：不想让ref响应得那么“即时”

创建一个自定义ref后，可以对其依赖项跟踪和更新触发进行逻辑控制、实现防抖效果

一般写为hooks格式，参数为一个返回值含get和set函数的对象

```typescript
import { customRef } from "vue";

export default function(initValue:string,delay:number){
  let msg = customRef((track,trigger)=>{//track跟踪、trigger触发
    
    let timer:number//用于接收定时器返回的定时器编号，避免拥挤
    
    return {
      get(){//msg被读取时调用
        track() // 告诉Vue要对msg持续关注，发生变化时要更新
        return initValue
      },
      set(value){//修改时调用
        clearTimeout(timer)//清空之前的定时器，从而只在意最后一个
        timer = setTimeout(() => {
          initValue = value
          trigger() //通知Vue数据msg变化了
        }, delay);
      }
    }
  }) 
  return {msg}
}
```

```typescript
import useMsgRef from './useMsgRef'
//ts就是不用带后缀
let msg = useMsgRef('你好', 1000)
console.log(msg.value)
```

# （七）<font style="color:rgb(51, 51, 51);">Vue3新组件</font>
## 一、teleport
传送门teleport：将组件的html结构移动到指定位置。通常是弹窗的问题。弹窗要放到整个屏幕的居中，但当父组件写了某些样式时，子组件的对齐模标准就变成父组件了。避免这种情况就用teleport标签+to属性值为body包一下弹窗的内容，其他设置照常写即可。

```html
<teleport to='body' >
    <div class="modal" v-show="isShow">
      <h2>我是一个弹窗</h2>
      <p>我是弹窗中的一些内容</p>
      <button @click="isShow = false">关闭弹窗</button>
    </div>
</teleport>
<script setup lang="ts" name="Modal">
import { ref } from 'vue'
const isShow = ref(true)
</script>

<style scoped>
.modal {
  border-radius: 5px;
  background-color: pink;
  padding: 5px;
  box-shadow: 0 0 10px;
  width: 200px;
  height: 160px;
  margin: 10px;
  position: fixed;
  text-align: center;
  left: 50%;
  margin-left: -100px;
  top: 10%;
}
</style>
```

## 二、Suspense
等待异步组件时渲染一些额外内容，让应用有更好的用户体验 

使用：当一个组件内有异步内容，父组件使用它就要包一层<Suspense>。内部再用template包，因为要用到插槽。 `v-slot:fallback`表示异步任务未完成时的内容，`v-slot:default`表示异步任务结束时的内容。

```vue
<Suspense>
  
  <template v-slot:fallback>
    <h3>加载中.......</h3>
  </template>
  
  <template v-slot:default>
    <Child />
  </template>
  
</Suspense>
```

```vue
import axios from 'axios'
let { data } = await axios.get('https://v1.hitokoto.cn')
//setup函数内以及提前做好了对于async的处理，直接写awaut即可
```

## 三、全局API→应用对象的方法
app即createApp(App)的赋值对象

+ <font style="background-color:#FBE4E7;">component：全局组件。</font>

在main.ts中 import Hello from './component/Hello.vue' 后 <font style="color:#F1A2AB;">app.component('Hello',Hello)</font>。这样别的组件和页面内就可以不引用直接使用Hello组件。

+ <font style="background-color:#FBE4E7;">config：全局属性</font>

app.config.globalProperties.x=9，则值为9的变量x在任意组件和页面内可使用。想要去除报错还要从官方文档中复制扩展全局属性粘过来并修改，最内层改为x:number

+ <font style="background-color:#FBE4E7;">directive：全局指令</font>

<font style="color:#F1A2AB;">app.directive('指令名'，(element)=>{</font>

<font style="color:#F1A2AB;">element.style.color='pink'</font>

<font style="color:#F1A2AB;">})</font>

对于想要执行该指令的标签内加v-指令名

<font style="color:#F1A2AB;">前三个都在挂载之前写好</font>

+ <font style="background-color:#FBE4E7;">mount：挂载到页面</font> <font style="color:#F1A2AB;">app.mount('#app')</font>
+ <font style="background-color:#FBE4E7;">unmount：卸载</font>，去除挂载过的组件 <font style="color:#F1A2AB;">app.unmount()</font>
+ <font style="background-color:#FBE4E7;">use：安装插件</font>，如路由：<font style="color:#F1A2AB;">app.use(router)</font>

## 四、非兼容性改变
关注官方文档中vue3的非兼容性改变

+ 过渡类名 `v-enter` 修改为 `v-enter-from`、过渡类名 `v-leave` 修改为 `v-leave-from`。
+ `keyCode` 作为 `v-on` 修饰符的支持。
+ `v-model` 指令在组件上的使用已经被重新设计，替换掉了 `v-bind.sync。`
+ `v-if` 和 `v-for` 在同一个元素身上使用时的优先级发生了变化。
+ 移除了`$on`、`$off` 和 `$once` 实例方法。
+ 移除了过滤器 `filter`。
+ 移除了`$children` 实例 `propert`。

......

