<template>
  <div class="show-container">
    <el-radio-group v-model="selectedDataset">
      <el-text class="mx-1" size="large">数据集：</el-text>
      <div>
        <el-radio value="shoes" size="large" border @change="handleRadioChange()">Shoes</el-radio>
        <el-radio value="fashioniq" size="large" border @change="handleRadioChange()">fashionIQ</el-radio>
      </div>
    </el-radio-group>
    <div v-if="selectedDataset === 'shoes'">
      <!-- 遍历 JSON 数据 -->
    <div v-for="(item, index) in showData1" :key="index" class="show-item">
      <!-- 展示 ImageName 图片 -->
      <div class="image-container">
        <el-image :src="getImageUrlshoes(item.ImageName)" :alt="item.ImageName" class="image" />
        <el-text class="caption">{{ item.ImageName }}</el-text>
      </div>

      <!-- 展示 ReferenceImageName 图片 -->
      <div class="image-container">
        <el-image :src="getImageUrlshoes(item.ReferenceImageName)" :alt="item.ReferenceImageName" class="image" />
        <el-text class="caption">{{ item.ReferenceImageName }}</el-text>
      </div>

      <!-- 展示 RelativeCaption 描述 -->
      <div class="caption-container">
        <el-text class="caption">{{ item.RelativeCaption }}</el-text>
      </div>

    </div>
    </div>
    <div v-else>
      <div v-for="(item, index) in showData2" :key="index" class="show-item">
      <!-- 展示 ImageName 图片 -->
      <div class="image-container">
        <el-image :src="getImageUrlfashioniq(item.ImageName)" :alt="item.ImageName" class="image" />
        <el-text class="caption">{{ item.ImageName }}</el-text>
      </div>

      <!-- 展示 ReferenceImageName 图片 -->
      <div class="image-container">
        <el-image :src="getImageUrlfashioniq(item.ReferenceImageName)" :alt="item.ReferenceImageName" class="image" />
        <el-text class="caption">{{ item.ReferenceImageName }}</el-text>
      </div>

      <!-- 展示 RelativeCaption 描述 -->
      <div class="caption-container">
        <el-text class="caption">{{ item.RelativeCaption }}</el-text>
      </div>

    </div>
    </div>
    



  </div>
</template>

<script setup lang="ts">
import showData1 from '@/assets/shoes/data.ts' // 导入 data.ts 文件
import showData2 from '@/assets/fashiniq/data.ts' // 导入 data.ts 文件
import { ref } from 'vue'

// 定义数据集选择
const selectedDataset = ref('shoes')




// 处理数据集选择变化
const handleRadioChange = () => {
  console.log('当前选择的数据集:', selectedDataset.value)
}

// 获取图片的完整 URL
const getImageUrlshoes = (imageName: string): string => {
  return new URL(`/src/assets/shoes/${imageName}`, import.meta.url).href
}
const getImageUrlfashioniq = (imageName: string): string => {
  return new URL(`/src/assets/fashiniq/${imageName}`, import.meta.url).href
}
</script>

<style scoped>
.show-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 20px;
}

.show-item {
  display: flex;
  align-items: center;
  gap: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  background-color: #f9f9f9;
}

.image-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.image {
  width: 200px;
  height: 200px;
  border-radius: 8px;
  object-fit: cover;
}

.caption-container {
  flex: 1;
  text-align: center;
}

.caption {
  font-size: 16px;
  color: #333;
}

.type-selector {
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
}
</style>
