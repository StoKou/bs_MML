<script setup lang="ts">
import {
  Management,
  Promotion,
  UserFilled,
  User,
  Crop,
  EditPen,
  SwitchButton,
  CaretBottom,
} from '@element-plus/icons-vue'
import avatar from '@/assets/default.png'
import { useUserStore } from '@/stores'
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessageBox } from 'element-plus' // 引入 ElMessageBox 用于确认对话框

// 获取用户 store 和路由实例
const userStore = useUserStore()
const router = useRouter()

// 组件挂载时获取用户信息
onMounted(() => {
  userStore.getUser()
})

// 处理命令的函数
const handleCommand = async (key: string) => {
  if (key === 'logout') {
    // 退出操作
    try {
      await ElMessageBox.confirm('你确认要进行退出么', '温馨提示', {
        type: 'warning',
        confirmButtonText: '确认',
        cancelButtonText: '取消',
      })

      // 清除本地的数据 (token + user信息)
      userStore.removeToken()
      userStore.setUser({})
      router.push('/login')
    } catch (error) {
      console.error('退出操作取消:', error)
    }
  } else {
    // 跳转操作
    router.push(`/user/${key}`)
  }
}
</script>

<template>
  <el-container class="layout-container">
    <el-aside width="200px">
      <div class="el-aside__logo"></div>
      <el-menu
        active-text-color="#ffd04b"
        background-color="#5bc5f2"
        :default-active="$route.path"
        text-color="#fff"
        router
      >
        <el-menu-item index="/home">
          <el-icon><Management /></el-icon>
          <span>主页</span>
        </el-menu-item>
        <el-menu-item index="/search">
          <el-icon><Promotion /></el-icon>
          <span>查询</span>
        </el-menu-item>
        <el-menu-item index="/show">
          <el-icon><Management /></el-icon>
          <span>展示</span>
        </el-menu-item>

        <el-sub-menu index="/user">
          <!-- 多级菜单的标题 - 具名插槽 title -->
          <template #title>
            <el-icon><UserFilled /></el-icon>
            <span>个人中心</span>
          </template>

          <!-- 展开的内容 - 默认插槽 -->
          <el-menu-item index="/user/profile">
            <el-icon><User /></el-icon>
            <span>基本资料</span>
          </el-menu-item>
          <el-menu-item index="/user/avatar">
            <el-icon><Crop /></el-icon>
            <span>更换头像</span>
          </el-menu-item>
          <el-menu-item index="/user/password">
            <el-icon><EditPen /></el-icon>
            <span>重置密码</span>
          </el-menu-item>
        </el-sub-menu>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header>
        <div>
          用户名：<strong>{{ userStore.user?.nickname || userStore.user?.username }}</strong>
        </div>
        <el-dropdown placement="bottom-end" @command="handleCommand">
          <!-- 展示给用户，默认看到的 -->
          <span class="el-dropdown__box">
            <el-avatar :src="userStore.user?.user_pic || avatar" />
            <el-icon><CaretBottom /></el-icon>
          </span>

          <!-- 折叠的下拉部分 -->
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="profile" :icon="User">基本资料</el-dropdown-item>
              <el-dropdown-item command="avatar" :icon="Crop">更换头像</el-dropdown-item>
              <el-dropdown-item command="password" :icon="EditPen">重置密码</el-dropdown-item>
              <el-dropdown-item command="logout" :icon="SwitchButton">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </el-header>
      <el-main>
        <router-view></router-view>
      </el-main>
      <el-footer>基于多模态大模型的图像检索系统 ©2025 Created by shikou</el-footer>
    </el-container>
  </el-container>
</template>

<style lang="scss" scoped>
.layout-container {
  height: 100vh;
  .el-aside {
    background-color: #5bc5f2;
    &__logo {
      height: 120px;
      background: url('@/assets/mylogo2.jpg') no-repeat center / 120px auto;
    }
    .el-menu {
      border-right: none;
    }
  }
  .el-header {
    background-color: #fff;
    display: flex;
    align-items: center;
    justify-content: space-between;
    .el-dropdown__box {
      display: flex;
      align-items: center;
      .el-icon {
        color: #999;
        margin-left: 10px;
      }

      &:active,
      &:focus {
        outline: none;
      }
    }
  }
  .el-footer {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    color: #666;
  }
}
</style>
