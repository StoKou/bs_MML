// src/stores/useImageStore.js
import { defineStore } from 'pinia'

export const useImageStore = defineStore('image', {
  state: () => ({
    imageUrl: null, // 存储图片的 URL
    text: '', // 存储文字
    targetImage: null, // 目标图片的 URL 或 Base64 数据
  }),
  actions: {
    // 设置图片
    setImageUrl(url) {
      this.imageUrl = url
    },
    // 设置文字
    setText(text) {
      this.text = text
    },
    setTargetImage(url) {
      this.targetImage = url
    },
    // 清空数据
    clearData() {
      this.imageUrl = null
      this.text = ''
      this.targetImage = null
    },
  },
  getters: {
    // 返回图片和文字
    getImageAndText(state) {
      return {
        imageUrl: state.imageUrl,
        text: state.text,
      }
    },
    getResults(state) {
      return {
        imageUrl: state.imageUrl,
        text: state.text,
        targetImage: state.targetImage,
      }
    },
  },
})
