import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
// 应该可以注释掉，暂时不知道有什么用
export const useCounterStore = defineStore('counter', () => {
  const count = ref(0)
  const doubleCount = computed(() => count.value * 2)
  function increment() {
    count.value++
  }

  return { count, doubleCount, increment }
})
