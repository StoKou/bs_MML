// src/stores/useUserStore.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { userGetInfoService, userHistoryService } from '../../api/user'
export interface HistoryItem {
  request_time: string
  username: string
  dataset: string
  model: string
  image_name: string
  description: string
  // 其他可能的字段...
}
// 定义用户信息的类型
interface UserInfo {
  id: number
  username: string
  nickname: string
  email: string
  user_pic: string
  history: HistoryItem[]
}

// 用户模块：token、setToken、removeToken
export const useUserStore = defineStore(
  'big-user',
  () => {
    // 定义 token 状态
    const token = ref<string>('')

    // 设置 token
    const setToken = (newToken: string): void => {
      token.value = newToken
    }

    // 移除 token
    const removeToken = (): void => {
      token.value = ''
    }

    // 定义用户信息状态
    const user = ref<UserInfo | null>(null)

    // 获取用户信息
    const getUser = async (): Promise<void> => {
      try {
        const res = await userGetInfoService() // 请求获取数据
        console.log(res)
        user.value = res.data.data as UserInfo
      } catch (error) {
        console.error('Failed to fetch user info:', error)
      }
    }
    //获取用户历史记录
    const getUserHistory = async (): Promise<void> => {
      try {
        const response = await userHistoryService()
        console.log(response)
        if (user.value) {
          user.value.history = response.data.data.history as HistoryItem[]
        } else {
          // 处理 user.value 为 null 的情况
          console.error('User data is not initialized')
        }
      } catch (error) {
        console.error('Failed to fetch histories:', error)
      }
    }
    // 设置用户信息
    const setUser = (obj: UserInfo): void => {
      user.value = obj
    }
    // 修改用户历史记录（history）
    const setUserHistory = (newHistory: HistoryItem[]): void => {
      if (user.value) {
        user.value.history = newHistory
      } else {
        console.warn('User is not set. Cannot update history.')
      }
    }
    return {
      token,
      setToken,
      removeToken,
      user,
      getUser,
      setUser,
      setUserHistory,
      getUserHistory,
    }
  },
  {
    persist: true,
  },
)
