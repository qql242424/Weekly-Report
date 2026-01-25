<template>
  <div class="father">
    <h3>父组件</h3>
    <hr />

    <h3>1.props</h3>
    <div>
      <b>a：</b>{{ a }}
      <button @click="add">a+1</button>
      <Child1 :a="a" :add="add" />
      <hr />
    </div>

    <h3>2.v-model</h3>
    <div>
      <!-- v-model本质 -->
      <h4>【v-model的本质】</h4>
      <input type="text" v-model="b1" /> 输入的内容为：{{ b1 }}
      <br />
      <input type="text" :value="b2" @input="b2 = (<HTMLInputElement>$event.target).value" />
      输入的内容为：{{ b2 }}
      <!-- 组件通信 -->
      <h4>【使用v-model进行通信】</h4>
      <b>b：</b>{{ b }} <Child2 :modelValue="b" @update:modelValue="b = $event" />
      <!-- 实际上父组件内可以直接写v-model -->
      <Child2 v-model="b" />
      <hr />
    </div>

    <h3>3.$refs和$parent</h3>
    <div>
      <b>c：</b>{{ c }}
      <br />
      <button @click="changeJie">更改姐姐的c1为666</button>
      <button @click="changeMei">更改妹妹的c1为888</button>
      <button @click="changeBoth($refs)">两个子组件的c1同时+1</button>
      <Child3 ref="jie" />
      <Child3 ref="mei" />
      <hr />
    </div>

    <h3>4.slot</h3>
    <div class="slot">
      <Child4 title="1号"> 哈哈 </Child4>
      <Child4 title="2号"> <template #s1>嘿嘿</template></Child4>
      <Child4 title="3号">
        <template v-slot:s2="ds">
          <ul>
            <li v-for="i in ds.d" :key="i.id">{{ i.content }}</li>
          </ul>
        </template>
      </Child4>
    </div>
    <hr />

    <h3>5.自定义事件</h3>
    <div>
      <b>e：</b>{{ e }}
      <Child5 @sendE="saveE" @addE="addE" />
    </div>
  </div>
</template>

<script setup lang="ts" name="Father">
import Child1 from './Child1.vue'
import Child2 from './Child2.vue'
import Child3 from './Child3.vue'
import Child4 from './Child4.vue'
import Child5 from './Child5.vue'
import { ref } from 'vue'
// 组件1

let a = ref(1)
function add() {
  a.value++
}

// 组件2
let b = ref(1)
let b1 = ref('')
let b2 = ref('')

//组件3
let c = ref(1)
let jie = ref()
let mei = ref()
defineExpose({ c })
function changeJie() {
  jie.value.c1 = 666
}
function changeMei() {
  mei.value.c1 = 888
}
function changeBoth(refs: any) {
  for (let key in refs) {
    refs[key].c1 += 1
  }
}

//组件4

//组件5
let e = ref(1)
function saveE(val: number) {
  e.value = val
}
function addE() {
  e.value++
}
</script>

<style scoped>
.father {
  background: pink;
  border-radius: 15px;
  margin: 10px;
  padding: 10px;
}
button {
  margin: 5px;
}
.slot {
  display: flex;
  justify-content: space-evenly;
}
</style>
