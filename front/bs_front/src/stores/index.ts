import { createPinia, type Pinia } from 'pinia'
import persist from 'pinia-plugin-persistedstate'

const pinia: Pinia = createPinia()
pinia.use(persist)

export default pinia
export * from './modules/user'
export * from './modules/counter'
export * from './modules/useImageStore'

// 如果需要单独导出 store，可以取消注释以下代码
// import { useUserStore } from './modules/user'
// export { useUserStore }
// import { useCountStore } from './modules/counter'
// export { useCountStore }
