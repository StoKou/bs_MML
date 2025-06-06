<script setup lang="ts">
import { ref } from 'vue'
import { userUpdatePasswordService } from '@/api/user'
import { useUserStore } from '@/stores'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus' // 引入 ElMessage 用于提示
import type { FormInstance, FormRules } from 'element-plus' // 引入 Element Plus 表单相关类型

// 表单引用，使用 ref 并指定类型为 FormInstance
const formRef = ref<FormInstance>()

// 表单数据，使用 ref 并指定类型
const pwdForm = ref({
  old_pwd: '',
  new_pwd: '',
  re_pwd: '',
})

// 校验规则：新密码不能与原密码一样
const checkDifferent = (rule: any, value: string, callback: (error?: Error) => void) => {
  if (value === pwdForm.value.old_pwd) {
    callback(new Error('新密码不能与原密码一样'))
  } else {
    callback()
  }
}

// 校验规则：确认密码必须和新密码一样
const checkSameAsNewPwd = (rule: any, value: string, callback: (error?: Error) => void) => {
  if (value !== pwdForm.value.new_pwd) {
    callback(new Error('确认密码必须和新密码一样'))
  } else {
    callback()
  }
}

// 表单校验规则，使用 ref 并指定类型为 FormRules
const rules = ref<FormRules>({
  old_pwd: [
    { required: true, message: '请输入原密码', trigger: 'blur' },
    { min: 6, max: 15, message: '原密码长度在6-15位之间', trigger: 'blur' },
  ],
  new_pwd: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, max: 15, message: '新密码长度在6-15位之间', trigger: 'blur' },
    { validator: checkDifferent, trigger: 'blur' },
  ],
  re_pwd: [
    { required: true, message: '请再次输入新密码', trigger: 'blur' },
    { min: 6, max: 15, message: '确认密码长度在6-15位之间', trigger: 'blur' },
    { validator: checkSameAsNewPwd, trigger: 'blur' },
  ],
})

// 获取用户 store 和路由实例
const userStore = useUserStore()
const router = useRouter()

// 提交表单
const submitForm = async () => {
  try {
    // 校验表单
    await formRef.value?.validate()
    // 发送请求更新密码
    await userUpdatePasswordService(pwdForm.value)
    // 提示用户
    ElMessage.success('密码修改成功')

    // 密码修改成功后，退出重新登录
    // 清空本地存储的 token 和 个人信息
    userStore.setToken('')
    userStore.setUser({})

    // 跳转到登录页
    router.push('/login')
  } catch (error) {
    console.error('密码修改失败:', error)
    ElMessage.error('密码修改失败')
  }
}

// 重置表单
const resetForm = () => {
  formRef.value?.resetFields()
}
</script>

<template>
  <page-container title="修改密码">
    <el-row>
      <el-col :span="12">
        <el-form ref="formRef" :model="pwdForm" :rules="rules" label-width="100px">
          <el-form-item label="原密码" prop="old_pwd">
            <el-input v-model="pwdForm.old_pwd" show-password></el-input>
          </el-form-item>
          <el-form-item label="新密码" prop="new_pwd">
            <el-input v-model="pwdForm.new_pwd" show-password></el-input>
          </el-form-item>
          <el-form-item label="确认密码" prop="re_pwd">
            <el-input v-model="pwdForm.re_pwd" show-password></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitForm">修改密码</el-button>
            <el-button @click="resetForm">清空</el-button>
          </el-form-item>
        </el-form></el-col
      >
    </el-row>
  </page-container>
</template>
