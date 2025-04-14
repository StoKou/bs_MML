import type { HistoryItem } from '@/stores'
import request from '@/utils/request'

// 注册接口
export const userRegisterService = ({
  username,
  password,
  repassword,
}: {
  username: string
  password: string
  repassword: string
}) => request.post('/api/reg', { username, password, repassword })
//历史记录接口
export const userHistoryService = () => request.get('my/history')
// 登录接口
export const userLoginService = ({ username, password }: { username: string; password: string }) =>
  request.post('/api/login', { username, password })

// 获取用户基本信息
export const userGetInfoService = () => request.get('/my/userinfo')

// 更新用户基本信息
export const userUpdateInfoService = ({
  id,
  username,
  nickname,
  email,
}: {
  id: number
  username: string
  nickname: string
  email: string
}) => request.patch('/my/updateUserinfo', { id, username, nickname, email})
// 更新用户历史记录
export const updateHistoryService = (history: HistoryItem[]) =>
  request.patch('/my/updateHistory', { history })
// 更新用户头像
export const userUpdateAvatarService = (avatar: string) =>
  request.patch('/my/update/avatar', { avatar })

// 更新用户密码
export const userUpdatePasswordService = ({
  old_pwd,
  new_pwd,
  re_pwd,
}: {
  old_pwd: string
  new_pwd: string
  re_pwd: string
}) => request.patch('/my/updatepwd', { old_pwd, new_pwd, re_pwd })
