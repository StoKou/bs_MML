<template>
  <page-container title="基本资料">
    <!-- 表单部分 -->
    <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
      <el-form-item label="登录名称">
        <el-input v-model="form.username" disabled></el-input>
      </el-form-item>
      <el-form-item label="用户昵称" prop="nickname">
        <el-input v-model="form.nickname"></el-input>
      </el-form-item>
      <el-form-item label="用户邮箱" prop="email">
        <el-input v-model="form.email"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitForm">提交修改</el-button>
      </el-form-item>
    </el-form>
  </page-container>
</template>
<script setup lang="ts">
import PageContainer from '@/components/PageContainer.vue'
import { ref } from 'vue'
import { useUserStore } from '@/stores/index'
import { userUpdateInfoService } from '@/api/user'
import { ElMessage } from 'element-plus' // 引入 ElMessage 用于提示
import type { FormInstance, FormRules } from 'element-plus' // 引入 Element Plus 表单相关类型

// 表单引用，使用 ref 并指定类型为 FormInstance
const formRef = ref<FormInstance>()

// 使用用户 store 中的数据
const userStore = useUserStore()
const {
  user: { 
    id,
  username,
  nickname,
  email,},
  getUser,
} = userStore

// 表单数据，使用 ref 并指定类型
const form = ref({
  id,
  username,
  nickname,
  email,
})

// 表单校验规则，使用 ref 并指定类型为 FormRules
const rules = ref<FormRules>({
  nickname: [
    { required: true, message: '请输入用户昵称', trigger: 'blur' },
    {
      pattern: /^\S{2,10}/,
      message: '昵称长度在2-10个非空字符',
      trigger: 'blur',
    },
  ],
  email: [
    { required: true, message: '请输入用户邮箱', trigger: 'blur' },
    {
      type: 'email',
      message: '请输入正确的邮箱格式',
      trigger: ['blur', 'change'],
    },
  ],
})

// 提交表单
const submitForm = async () => {
  try {
    console.log(form.value)
    // 等待校验结果
    await formRef.value?.validate()
    // 提交修改
    await userUpdateInfoService(form.value)
    console.log(form.value)
    // 通知 user 模块，进行数据的更新
    await getUser()
    // 提示用户
    ElMessage.success('修改成功')
  } catch (error) {
    console.error('修改失败:', error)
    ElMessage.error('修改失败')
  }
}
</script>

