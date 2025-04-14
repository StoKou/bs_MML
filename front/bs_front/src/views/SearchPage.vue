<template>
  <el-main>
    <div class="container">
      <!-- 左半边：输入部分 -->
      <div class="left-side">
        <div>
          <el-radio-group v-model="selectedDataset">
            <el-text class="mx-1" size="large">数据集：</el-text>
            <div>
              <el-radio value="shoes" size="large" border @change="handleRadioChange()"
              >Shoes</el-radio
            >
            <el-radio value="fashioniq" size="large" border @change="handleRadioChange()"
              >fashionIQ</el-radio
            >
            </div>
            
          </el-radio-group>
        </div>
        <div v-if="selectedDataset === 'shoes'" class="model-radio-group">
          <div class="flex flex-wrap gap-4 items-center">
            <!-- <el-text class="mx-1" size="large">模型：</el-text> -->
            <el-select
              v-model="selectedModel"
              placeholder="模型"
              size="large"
              style="width: 240px"
            >
              <el-option
                v-for="item in options_shoes"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </div>
        </div>
        <div v-else class="model-radio-group">
          <div class="flex flex-wrap gap-4 items-center">
            <!-- <el-text class="mx-1" size="large">模型：</el-text> -->
            <el-select
              v-model="selectedModel"
              placeholder="模型"
              size="large"
              style="width: 240px"
            >
              <el-option
                v-for="item in options_fashiniq"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </div>
        </div>
        
        <div>
          <!-- 图片上传组件 -->
          <el-upload
            v-model:file-list="fileList"
            class="upload-demo"
            action="http://127.0.0.1:5000/upload"
            :multiple="false"
            :limit="1"
            :on-success="handleSuccess"
            :on-remove="handleRemove"
            :before-remove="beforeRemove"
            :on-exceed="handleExceed"
            :on-preview="handlePreview"
          >
            <el-button type="primary">点击上传图片</el-button>
            <template #tip>
              <div class="el-upload__tip">jpg/png 文件，大小不超过 500KB</div>
            </template>
          </el-upload>
        </div>

        <div>
          <!-- 文本输入 -->
          <el-input v-model="inputText" style="width: 240px" placeholder="请输入描述文字" />
        </div>

        <div>
          <!-- 提交按钮 -->
          <el-button type="primary" @click="submit">提交</el-button>
        </div>
        <div>
          <el-progress
            v-if="showProgress"
            :percentage="progressPercentage"
            stroke-width="6"
          ></el-progress>
        </div>
      </div>

      <!-- 右半边：输出部分 -->
      <div class="right-side">
        <div class="demo-image">
          <div v-for="fit in fits" :key="fit" class="block">
            <span class="demonstration">{{ fit }}</span>
            <el-image style="width: 200px; height: 200px" :src="url" :fit="fit" />
          </div>
        </div>
      </div>
    </div>
  </el-main>
  <el-footer>
    <el-text class="mx-1" type="info">历史记录</el-text>
    <el-table :data="histories" style="width: 100%" max-height="250">
      <el-table-column fixed prop="request_time" label="Date" width="150" />
      <el-table-column prop="username" label="Name" width="120" />
      <el-table-column prop="model" label="Model" width="120" />
      <el-table-column prop="image_name" label="UploadImage" width="120" />
      <el-table-column prop="description" label="Description" width="600" />
      <!-- <el-table-column prop="zip" label="Zip" width="120" /> -->
      <el-table-column fixed="right" label="Operations" min-width="120">
        <template #default="scope">
          <el-button link type="primary" size="small" @click.prevent="deleteRow(scope.$index)">
            Remove
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-footer>
</template>

<script setup lang="ts">
import { ElMessage, ElMessageBox } from 'element-plus'
import type { UploadProps, UploadUserFile } from 'element-plus'
import { computed, ref } from 'vue'

import type { ImageProps } from 'element-plus'
import { useImageStore } from '@/stores/modules/useImageStore'
import axios from 'axios'
import { useUserStore } from '@/stores'
import { updateHistoryService } from '@/api/user'
// 处理图片和文字
const fileList = ref<UploadUserFile[]>([])

const handleRemove: UploadProps['onRemove'] = (file, uploadFiles) => {
  console.log(file, uploadFiles)
}

const handlePreview: UploadProps['onPreview'] = (uploadFile) => {
  console.log(uploadFile)
}

const handleExceed: UploadProps['onExceed'] = (files, uploadFiles) => {
  ElMessage.warning(
    `The limit is 3, you selected ${files.length} files this time, add up to ${
      files.length + uploadFiles.length
    } totally`,
  )
}

const beforeRemove: UploadProps['beforeRemove'] = (uploadFile) => {
  return ElMessageBox.confirm(`Cancel the transfer of ${uploadFile.name} ?`).then(
    () => true,
    () => false,
  )
}
const userStore = useUserStore()
const imageStore = useImageStore()
const inputText = ref('')
// 处理文件上传
const handleSuccess = () => {
  const file = fileList.value[0]
  console.log('文件上传成功:', file)
  console.log('file.raw:', file.raw)

  if (file.raw instanceof File) {
    const fileURL = URL.createObjectURL(file.raw) // 生成临时 URL
    imageStore.setImageUrl({
      url: fileURL,
    })
    console.log(fileURL)
  } else {
    console.error('file.raw 不是有效的 File 对象:', file.raw)
  }
}
//返回图片
const fits = ['fill'] as ImageProps['fit'][]
const url = ref('')
//返回图片设置
const setShowTarGetImage = (newUrl: string | null) => {
  if (newUrl !== null) {
    url.value = newUrl // 只有在 newUrl 不是 null 时才赋值
  }
}
const showProgress = ref(false)
const progressPercentage = ref(0)
//历史记录
const histories = computed(() => userStore.user?.history || [])

const deleteRow = async (index: number) => {
  // console.log(histories)
  histories.value?.splice(index, 1)
  if (histories.value) {
    userStore.setUserHistory(histories.value)
    await updateHistoryService(histories.value)
  } else {
    console.warn('Histories is null, cannot update user history.')
  }
}

// 提交数据
const submit = async () => {
  showProgress.value = true // 显示进度条
  progressPercentage.value = 0 // 初始化进度
  //先将文本存入pinia
  imageStore.setText(inputText.value)
  //处理上传的数据
  if (fileList.value.length === 0 || !inputText.value) {
    alert('请选择图片并输入描述文字')
    return
  }

  const file = fileList.value[0]

  // 确保 file.raw 是 File 对象
  if (!(file.raw instanceof File)) {
    alert('文件无效，请重新选择')
    return
  }

  const result = ref<{
    inputImage: string
    description: string
    outputImage: string
  } | null>(null)
  const formData = new FormData()
  formData.append('image', file.raw) // 添加图片文件
  formData.append('description', inputText.value) // 添加描述文字
  formData.append('dataset', selectedDataset.value)
  formData.append('model', selectedModel.value)
  formData.append('token', userStore.token)
  // 这里还需要添加模型选项，数据集选项
  try {
    const response = await axios.post('http://localhost:5000/predict', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        const { loaded, total } = progressEvent
        if (total !== undefined) {
          progressPercentage.value = Math.round((loaded / total) * 100)
        } else {
          progressPercentage.value = 0 // 如果 total 未定义，则设置进度为 0
        }
      },
    })

    // 处理返回的三元组
    result.value = {
      inputImage: URL.createObjectURL(file.raw), // 输入图片的临时 URL
      description: response.data.description, // 描述文字
      outputImage: `data:image/jpeg;base64,${response.data.outputImage}`, // 输出图片的 Base64
    }
    userStore.getUserHistory()
  } catch (error) {
    console.error('提交失败:', error)
    alert('提交失败，请重试')
  } finally {
    showProgress.value = false // 隐藏进度条
    console.log(result)
  }
  //保存到pinia
  imageStore.setTargetImage(result.value?.outputImage)

  //重新展示图片
  setShowTarGetImage(imageStore.getResults.targetImage)
}
// 定义数据集选择
const selectedDataset = ref('shoes')
// 用于绑定模型选择
const selectedModel = ref('')
const options_fashiniq = [
  {
    value:'dress',
    label:'dress',
  },
  {
    value:'shirt',
    label:'shirt',
  },
  {
    value:'toptee',
    label:'toptee',
  }
]
const options_shoes = [
  {
    value: 'model1',
    label: 'model1',
  },
  {
    value: 'model2',
    label: 'model2',
  },
  {
    value: 'model3',
    label: 'model3',
  },
]
// 处理数据集选择变化
const handleRadioChange = () => {
  console.log('当前选择的数据集:', selectedDataset.value)
}
</script>

<style scoped>
.container {
  display: flex;
  gap: 20px; /* 左右两部分之间的间距 */
}

.left-side {
  flex: 1; /* 左半边占 1 份 */
  max-width: 250px; /* 限制左半边的最大宽度 */
}

.right-side {
  flex: 1; /* 右半边占 1 份 */
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
}

.demo-image .block {
  padding: 30px 0;
  text-align: center;
  border-right: solid 1px var(--el-border-color);
  display: inline-block;
  width: 20%;
  box-sizing: border-box;
  vertical-align: top;
}
.demo-image .block:last-child {
  border-right: none;
}
.demo-image .demonstration {
  display: block;
  color: var(--el-text-color-secondary);
  font-size: 14px;
  margin-bottom: 20px;
}
</style>
