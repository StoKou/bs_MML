import axios from 'axios'
import { useUserStore } from '@/stores'
import { ElMessage } from 'element-plus'
import router from '@/router'

// 基础 URL
const baseURL = 'http://127.0.0.1:5000'

const instance = axios.create({
  baseURL,
  timeout: 10000, // 设置超时时间为 10 秒
})

// 请求拦截器
instance.interceptors.request.use(
  (config) => {
    const userStore = useUserStore() // 获取用户状态
    // console.log(userStore.token)
    if (userStore.token) {
      config.headers.Authorization = userStore.token // 携带 Token
      config.headers.username = userStore.user?.username
    }
    // console.log(config)
    return config
  },
  (err) => Promise.reject(err),
)

// 响应拦截器
instance.interceptors.response.use(
  (res) => {
    // console.log(res)
    if (res.data?.code === 0) {
      return res // 如果响应成功，直接返回响应数据
    }
    // 如果业务失败，提示错误信息并抛出错误
    // ElMessage.error(res.data.message)
    return Promise.reject(res.data)
  },
  (err) => {
    // 处理 401 错误（权限不足或 Token 过期）
    if (err.response?.status === 401) {
      ElMessage.error('登录状态失效，请重新登录')
      router.push('/login') // 跳转到登录页面
    }
    // // 其他错误，提示错误信息
    ElMessage.error(err.response?.data.message)
    return Promise.reject(err)
  },
)

export default instance
export { baseURL }
