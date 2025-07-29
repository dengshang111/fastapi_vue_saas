<template>
  <div class="space-y-4">
    <!-- 上传区域 -->
    <div
      @drop.prevent="handleDrop"
      @dragover.prevent="dragover = true"
      @dragleave.prevent="dragover = false"
      :class="[
        'border-2 border-dashed rounded-lg p-6 text-center transition-colors max-h-96 overflow-y-auto',
        dragover
          ? 'border-blue-400 bg-blue-50 dark:bg-blue-900/20'
          : 'border-gray-300 hover:border-gray-400 dark:border-gray-600 dark:hover:border-gray-500'
      ]"
    >
      <div v-if="selectedFiles.length === 0">
        <svg class="mx-auto h-12 w-12 text-gray-400 dark:text-gray-500" stroke="currentColor" fill="none" viewBox="0 0 48 48">
          <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
        <div class="mt-4">
          <label for="file-upload" class="cursor-pointer inline-flex items-center px-6 py-3 border-2 border-dashed border-gray-300 text-sm font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 hover:border-gray-400 transition-colors dark:border-gray-600 dark:text-gray-300 dark:bg-gray-800 dark:hover:bg-gray-700 dark:hover:border-gray-500">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
            </svg>
            选择图片文件
          </label>
          <input
            id="file-upload"
            ref="fileInput"
            type="file"
            accept="image/*"
            multiple
            class="sr-only"
            @change="handleFileSelect"
          />
          <p class="mt-2 text-xs text-gray-500 dark:text-gray-400">
            支持 JPG, PNG, GIF, WebP 格式，最大 10MB，可多选
          </p>
        </div>
      </div>
      <!-- 批量预览区域 -->
      <div v-if="selectedFiles.length > 0" class="space-y-4">
        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
          <div v-for="(file, idx) in selectedFiles" :key="file.id" class="relative group border rounded-lg p-2 bg-white dark:bg-gray-800 dark:border-gray-700">
            <img
              v-if="file.previewUrl"
              :src="file.previewUrl"
              :alt="file.file.name"
              class="mx-auto max-h-32 rounded object-cover"
            />
            <div class="mt-2 text-xs text-gray-700 dark:text-gray-300 truncate">{{ file.file.name }}</div>
            <div class="text-xs text-gray-400 dark:text-gray-500">{{ formatFileSize(file.file.size) }}</div>
            <button
              @click="removeFile(idx)"
              class="absolute top-2 right-2 bg-red-500 text-white rounded-full p-1 hover:bg-red-600 transition-colors"
              title="移除"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
            <!-- 单个文件上传进度 -->
            <div v-if="file.uploading" class="mt-2">
              <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                <div
                  class="bg-blue-600 h-2 rounded-full transition-all duration-300"
                  :style="{ width: file.progress + '%' }"
                ></div>
              </div>
              <div class="text-xs text-gray-500 dark:text-gray-400 mt-1">{{ file.progress }}%</div>
            </div>
            <div v-if="file.error" class="text-xs text-red-500 dark:text-red-400 mt-1">{{ file.error }}</div>
            <div v-if="file.success" class="text-xs text-green-600 dark:text-green-400 mt-1">上传成功</div>
          </div>
        </div>
        
      </div>
    </div>

    <!-- 错误信息 -->
    <div v-if="error" class="p-3 bg-red-50 border border-red-200 rounded-md dark:bg-red-900/20 dark:border-red-800">
      <p class="text-sm text-red-600 dark:text-red-400">{{ error }}</p>
    </div>

    <!-- 操作按钮区域 -->
    <div v-if="selectedFiles.length > 0 && !uploadingAll" class="flex justify-center space-x-4">
      <!-- 添加更多文件按钮 -->
      <label for="file-upload-more" class="cursor-pointer inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 dark:border-gray-600 dark:text-gray-300 dark:bg-gray-800 dark:hover:bg-gray-700">
        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
        </svg>
        添加更多文件
      </label>
      <input
        id="file-upload-more"
        ref="fileInputMore"
        type="file"
        accept="image/*"
        multiple
        class="sr-only"
        @change="handleFileSelect"
      />
      
      <!-- 批量上传按钮 -->
      <button
        @click="uploadAll"
        :disabled="selectedFiles.length === 0"
        class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed dark:bg-blue-500 dark:hover:bg-blue-600"
      >
        批量上传 ({{ selectedFiles.length }})
      </button>
    </div>
    <div v-if="uploadingAll" class="text-center text-sm text-gray-500 dark:text-gray-400">批量上传中...</div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  group: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue', 'upload-success'])

const authStore = useAuthStore()

// 响应式数据
const fileInput = ref(null)
const selectedFiles = ref([]) // [{ id, file, previewUrl, uploading, progress, error, success }]
const error = ref('')
const dragover = ref(false)
const uploadingAll = ref(false)

// 处理文件选择
const handleFileSelect = (event) => {
  const files = Array.from(event.target.files)
  addFiles(files)
}

// 处理拖拽
const handleDrop = (event) => {
  dragover.value = false
  const files = Array.from(event.dataTransfer.files)
  addFiles(files)
}

// 添加文件到列表
function addFiles(files) {
  for (const file of files) {
    if (!file.type.startsWith('image/')) {
      error.value = '请选择图片文件'
      continue
    }
    if (file.size > 10 * 1024 * 1024) {
      error.value = '文件大小不能超过10MB'
      continue
    }
    const id = `${file.name}_${file.size}_${file.lastModified}_${Math.random()}`
    const reader = new FileReader()
    reader.onload = (e) => {
      selectedFiles.value.push({
        id,
        file,
        previewUrl: e.target.result,
        uploading: false,
        progress: 0,
        error: '',
        success: false
      })
    }
    reader.readAsDataURL(file)
  }
}

// 移除文件
function removeFile(idx) {
  selectedFiles.value.splice(idx, 1)
  error.value = ''
  // 清空所有input
  if (fileInput.value) fileInput.value.value = ''
  
}

// 格式化文件大小
function formatFileSize(bytes) {
  if (!bytes) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// 批量上传
async function uploadAll() {
  uploadingAll.value = true
  error.value = ''
  
  // 设置所有文件为上传中状态
  selectedFiles.value.forEach(fileObj => {
    fileObj.uploading = true
    fileObj.progress = 0
    fileObj.error = ''
    fileObj.success = false
  })
  
  try {
    const formData = new FormData()
    
    // 添加所有文件到FormData
    selectedFiles.value.forEach(fileObj => {
      formData.append('files', fileObj.file)
    })
    
    // 添加分组信息
    if (props.group) {
      formData.append('group', props.group)
    }
    
    // 模拟整体进度
    const totalFiles = selectedFiles.value.length
    let completedFiles = 0
    const progressInterval = setInterval(() => {
      selectedFiles.value.forEach(fileObj => {
        if (fileObj.progress < 90) {
          fileObj.progress += 10
        }
      })
    }, 100)
    
    const response = await authStore.authenticatedFetch('/api/upload/batch-upload', {
      method: 'POST',
      body: formData
    })
    
    clearInterval(progressInterval)
    
    if (response.ok) {
      const result = await response.json()
      
      // 处理上传结果
      result.results.forEach((uploadResult, index) => {
        if (selectedFiles.value[index]) {
          selectedFiles.value[index].progress = 100
          selectedFiles.value[index].success = true
          emit('upload-success', uploadResult)
        }
      })
      
      // 处理错误结果
      result.errors.forEach(errorInfo => {
        const fileIndex = selectedFiles.value.findIndex(fileObj => 
          fileObj.file.name === errorInfo.filename
        )
        if (fileIndex !== -1) {
          selectedFiles.value[fileIndex].error = errorInfo.error
        }
      })
      
      console.log(`批量上传完成: ${result.message}`)
    } else {
      const errorData = await response.json()
      selectedFiles.value.forEach(fileObj => {
        fileObj.error = errorData.detail || '上传失败'
      })
    }
  } catch (err) {
    selectedFiles.value.forEach(fileObj => {
      fileObj.error = err.message || '上传失败'
    })
  }
  
  // 设置所有文件为非上传状态
  selectedFiles.value.forEach(fileObj => {
    fileObj.uploading = false
  })
  
  uploadingAll.value = false
  
  // 上传完成后自动清空
  setTimeout(() => {
    selectedFiles.value = []
    if (fileInput.value) fileInput.value.value = ''
   
  }, 2000)
}
</script> 