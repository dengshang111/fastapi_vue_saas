<template>
  <div class="image-selector">
    <!-- 当前选中的图片 -->
    <div v-if="selectedImage && (!Array.isArray(selectedImage) || selectedImage.length > 0)" class="mb-4">
      <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">当前选中的图片</label>
      <div v-if="!multiple" class="flex items-center space-x-3 p-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800">
        <img
          :src="getPreviewUrl(selectedImage, true)"
          :alt="selectedTitle"
          class="h-16 w-24 object-cover rounded-lg"
        />
        <div class="flex-1">
          <p class="text-sm font-medium text-gray-900 dark:text-gray-100">{{ selectedTitle || '' }}</p>
          <p class="text-sm text-gray-500 dark:text-gray-400">{{ selectedImage }}</p>
        </div>
        <button
          @click="clearSelection"
          class="text-red-600 hover:text-red-800 dark:text-red-400 dark:hover:text-red-300"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
      </div>
      <div v-else class="space-y-2 overflow-y-auto max-h-50">
        <div v-for="(image, index) in selectedImage" :key="index" class="flex items-center space-x-3 p-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800">
          <img
            :src="getPreviewUrl(image, true)"
            :alt="selectedTitle[index]"
            class="h-16 w-24 object-cover rounded-lg"
          />
          <div class="flex-1">
            <p class="text-sm font-medium text-gray-900 dark:text-gray-100">{{ selectedTitle[index] || '' }}</p>
            <p class="text-sm text-gray-500 dark:text-gray-400">{{ image }}</p>
          </div>
          <button
            @click="selectImage({url: image, filename: selectedTitle[index]})"
            class="text-red-600 hover:text-red-800 dark:text-red-400 dark:hover:text-red-300"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- 分组选择 -->
    <div class="mb-4">
      <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">选择分组</label>
      <select
        v-model="selectedGroup"
        @change="loadImages"
        class="block w-full border border-gray-300 dark:border-gray-600 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
      >
        <option value="">默认分组</option>
        <option v-for="group in groups" :key="group.name" :value="group.name">
          {{ group.name }} ({{ group.file_count }}张图片)
        </option>
      </select>
    </div>

    <!-- 图片网格 -->
    <div v-if="loading" class="text-center py-8">
      <div class="inline-flex items-center">
        <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-blue-600 dark:text-blue-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <span class="text-gray-900 dark:text-gray-100">加载中...</span>
      </div>
    </div>

    <div v-else-if="images.length === 0" class="text-center py-8">
      <svg class="mx-auto h-12 w-12 text-gray-400 dark:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
      </svg>
      <h3 class="mt-2 text-sm font-medium text-gray-900 dark:text-gray-100">暂无图片</h3>
      <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">该分组下没有上传的图片。</p>
    </div>

    <div v-else class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 overflow-y-auto max-h-40">
      <div
        v-for="image in images"
        :key="image.filename"
        :class="['relative border rounded-lg overflow-hidden cursor-pointer hover:shadow-md transition-all',
                isImageSelected(image.url) ? 'border-blue-500 ring-2 ring-blue-500 dark:border-blue-400 dark:ring-blue-400' : 'border-gray-300 dark:border-gray-600']"
        @click="selectImage(image)"
      >
        <div ref="imageRefs" class="w-full h-32">
          <img
            v-if="imageVisibility[image.filename]"
            :src="getPreviewUrl(image.url, true)"
            :alt="image.filename"
            class="w-full h-full object-cover"
            loading="lazy"
          />
          <div v-else class="w-full h-full bg-gray-100 dark:bg-gray-700 flex items-center justify-center">
            <svg class="w-8 h-8 text-gray-300 dark:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
            </svg>
          </div>
        </div>
        <div class="p-2 bg-white dark:bg-gray-800">
          <p class="text-xs text-gray-600 dark:text-gray-300 truncate">{{ image.filename }}</p>
          <p class="text-xs text-gray-400 dark:text-gray-500">{{ formatFileSize(image.size) }}</p>
        </div>
        <!-- 选中标记 -->
        <div v-if="isImageSelected(image.url)" class="absolute top-2 right-2 bg-blue-500 dark:bg-blue-400 rounded-full p-1">
          <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
          </svg>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import { useAuthStore } from '../stores/auth'
import { getImageUrlWithToken } from '../config/env'
import { useIntersectionObserver } from '@vueuse/core'

// API基础URL
const API_BASE_URL = '/backend'
const props = defineProps({
  modelValue: {
    type: [String, Array],
    default: ''
  },
  title: {
    type: [String, Array],
    default: ''
  },
  multiple: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'update:title'])

const authStore = useAuthStore()
const loading = ref(false)
const images = ref([])
const groups = ref([])
const selectedGroup = ref('')
const imageRefs = ref([])
const imageVisibility = ref({})

// 选中的图片和标题
const selectedImage = ref(props.modelValue)
const selectedTitle = ref(props.title)

// 监听 props 变化
watch(() => props.modelValue, (newValue) => {
  selectedImage.value = newValue
})

watch(() => props.title, (newValue) => {
  selectedTitle.value = newValue
})

// 监听选中图片变化
watch(selectedImage, (newValue) => {
  emit('update:modelValue', newValue)
})

watch(selectedTitle, (newValue) => {
  emit('update:title', newValue)
})

// 选择图片
const selectImage = (image) => {
  if (props.multiple) {
    // 多选模式
    if (!Array.isArray(selectedImage.value)) {
      selectedImage.value = []
      selectedTitle.value = []
    }
    
    const imageIndex = selectedImage.value.indexOf(image.url)
    if (imageIndex === -1) {
      // 添加新选择的图片
      selectedImage.value.push(image.url)
      selectedTitle.value.push(image.filename)
    } else {
      // 取消选择已选中的图片
      selectedImage.value.splice(imageIndex, 1)
      selectedTitle.value.splice(imageIndex, 1)
    }
  } else {
    // 单选模式
    selectedImage.value = image.url
    selectedTitle.value = image.filename
  }
}

// 清除选择
const clearSelection = () => {
  selectedImage.value = props.multiple ? [] : ''
  selectedTitle.value = props.multiple ? [] : ''
}

// 检查图片是否被选中
const isImageSelected = (imageUrl) => {
  if (props.multiple) {
    return Array.isArray(selectedImage.value) && selectedImage.value.includes(imageUrl)
  }
  return selectedImage.value === imageUrl
}

// 获取分组列表
const loadGroups = async () => {
  try {
    const response = await authStore.authenticatedFetch('/api/upload/groups')
    if (response.ok) {
      groups.value = await response.json()
    }
  } catch (error) {
    console.error('获取分组列表失败:', error)
  }
}

// 获取图片列表
const loadImages = async () => {
  loading.value = true
  try {
    const url = selectedGroup.value 
      ? `/api/upload/files?group=${encodeURIComponent(selectedGroup.value)}`
      : '/api/upload/files'
    
    const response = await authStore.authenticatedFetch(url)
    if (response.ok) {
      images.value = await response.json()
      // 初始化所有图片的可见性为 false
      imageVisibility.value = images.value.reduce((acc, img) => {
        acc[img.filename] = false
        return acc
      }, {})
    }
  } catch (error) {
    console.error('获取图片列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 格式化文件大小
const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// 获取预览URL（添加token和thumbnail参数）
const getPreviewUrl = (imageUrl, useThumbnail = false) => {
  const baseUrl = getImageUrlWithToken(imageUrl)
  return useThumbnail ? `${baseUrl}&thumbnail=300x300` : baseUrl
}

// 设置图片懒加载
const setupIntersectionObserver = () => {
  if (imageRefs.value.length === 0) return

  imageRefs.value.forEach((el, index) => {
    const image = images.value[index]
    if (!image) return

    useIntersectionObserver(el, ([{ isIntersecting }]) => {
      if (isIntersecting) {
        imageVisibility.value[image.filename] = true
      }
    }, {
      threshold: 0.1
    })
  })
}

// 监听图片列表变化，重新设置懒加载
watch(images, () => {
  nextTick(() => {
    setupIntersectionObserver()
  })
})

// 组件挂载时加载数据
onMounted(() => {
  loadGroups()
  loadImages()
})
</script>

<style scoped>
.image-selector {
  width: 100%;
}
</style> 