<template>
  <div class="image-search">
    <h1>图像检索</h1>
    <p>基于多模态和大模型</p>
    <button @click="startSearch">点击开始</button>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
const route = useRouter()

const startSearch = () => {
  route.push('/search')
}
</script>

<style scoped>
.image-search {
  text-align: center;
  padding: 50px;
  background-color: #ffffff; /* 浅紫色背景 */
}

.image-search h1 {
  font-size: 3em;
  font-weight: bold;
  color: #333333;
  margin: 0;
}

.image-search p {
  font-size: 1.2em;
  color: #666666;
  margin: 10px 0 30px;
}

.image-search button {
  padding: 10px 30px;
  font-size: 1.2em;
  background-color: #007bff;
  color: #ffffff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.image-search button:hover {
  background-color: #0056b3;
}
.el-header {
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
  padding: 20px; /* 添加一些内边距 */
  height: auto; /* 根据内容自动调整高度 */
  width: 1200px;
}

.text-container {
  display: flex;
  flex-direction: column;
  align-items: center; /* 水平居中 */
  justify-content: center; /* 垂直居中 */
  padding: 20px; /* 添加一些内边距 */
  gap: 20px; /* 设置网格项之间的间距 */
}

.text-large {
  font-size: 40px;
  text-align: center; /* 设置文本居中 */
  white-space: pre-wrap; /* 允许文本换行 */
  word-wrap: break-word; /* 允许长单词换行 */
}

.el-footer {
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
  padding: 20px; /* 添加一些内边距 */
}
</style>
