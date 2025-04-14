import { defineStore } from 'pinia'
import { ref } from 'vue'

// 数字计数器模块
export const useCountStore = defineStore('big-count', () => {
  const count = ref<number>(100) // 明确指定 ref 的类型为 number

  // 定义 add 函数，参数 n 的类型为 number
  const add = (n: number) => {
    count.value += n
  }

  return {
    count,
    add,
  }
})
