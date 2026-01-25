export interface PersonInter {
  name: string //首字母不可大写
  id: string
  age: number
}
export type Persons = Array<PersonInter> //“泛型”，用尖括号表示可写的数据类型
// 等同于export type Persons = PersonInter[]
