<template>
  <div>
    <page-container title="更换头像">
      <el-upload
        ref="uploadRef"
        :auto-upload="false"
        class="avatar-uploader"
        :show-file-list="false"
        :on-change="onSelectFile"
      >
        <img v-if="imgUrl" :src="imgUrl" class="avatar" />
        <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
      </el-upload>

      <br />

      <el-button
        @click="uploadRef.$el.querySelector('input').click()"
        type="primary"
        :icon="Plus"
        size="large"
        >选择图片</el-button
      >
      <el-button @click="onUpdateAvatar" type="success" :icon="Upload" size="large"
        >上传头像</el-button
      >
    </page-container>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Plus, Upload } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/index'
import { userUpdateAvatarService } from '@/api/user'
import { ElMessage } from 'element-plus' // 引入 ElMessage 用于提示
import type { UploadFile } from 'element-plus' // 引入 UploadFile 类型

// 获取用户 store
const userStore = useUserStore()

// 图片地址，使用 ref 并指定类型为 string
// const imgUrl = ref<string>(userStore.user.user_pic || '')
const imgUrl = ref<string>('')
// 上传组件实例，使用 ref 并指定类型为 any（因为 Element Plus 的 Upload 组件类型较复杂）
const uploadRef = ref<any>()

// 选择文件时的回调函数
const onSelectFile = (uploadFile: UploadFile) => {
  // 基于 FileReader 读取图片做预览
  const reader = new FileReader()
  if (uploadFile.raw) {
    reader.readAsDataURL(uploadFile.raw)
    reader.onload = () => {
      if (reader.result) {
        imgUrl.value = reader.result as string
      }
    }
  }
}

// 更新头像的函数
const onUpdateAvatar = async () => {
  try {
    // 发送请求更新头像
    console.log(imgUrl)
    await userUpdateAvatarService(imgUrl.value)
    // 重新获取用户信息
    await userStore.getUser()
    // 提示用户
    ElMessage.success('头像更新成功')
  } catch (error) {
    console.error('头像更新失败:', error)
    ElMessage.error('头像更新失败')
  }
}
</script>

<style lang="scss" scoped>
.avatar-uploader {
  :deep() {
    .avatar {
      width: 278px;
      height: 278px;
      display: block;
    }
    .el-upload {
      border: 1px dashed var(--el-border-color);
      border-radius: 6px;
      cursor: pointer;
      position: relative;
      overflow: hidden;
      transition: var(--el-transition-duration-fast);
    }
    .el-upload:hover {
      border-color: var(--el-color-primary);
    }
    .el-icon.avatar-uploader-icon {
      font-size: 28px;
      color: #8c939d;
      width: 278px;
      height: 278px;
      text-align: center;
    }
  }
}
</style>
