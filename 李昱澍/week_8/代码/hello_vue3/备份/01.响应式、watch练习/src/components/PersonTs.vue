<script setup lang="ts" name="PersonTs">
import { type PersonInter, type Persons } from '@/types'
//@等价于src,整个vue工程内都可以这样简写
let person: PersonInter = {
  id: '001',
  name: '张三',
  age: 1,
}
//此处Persons相当于Array<PersonInter>
let personList: Persons = [
  { id: '001', name: '张三', age: 1 },
  { id: '002', name: '李四', age: 2 },
  { id: '003', name: '王五', age: 3 },
]
</script>
