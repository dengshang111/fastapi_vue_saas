<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-900">
    <!-- 顶部导航栏 -->
    <nav class="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <h1 class="text-xl font-semibold text-gray-900 dark:text-white">仓库管理</h1>
          </div>
          <div class="flex items-center space-x-4">
            <router-link
              to="/dashboard"
              class="inline-flex items-center px-3 py-2 border border-gray-300 dark:border-gray-600 text-sm leading-4 font-medium rounded-md text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
            >
              返回主控面板
            </router-link>
            <button
              @click="handleLogout"
              class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-red-600 hover:bg-red-700"
            >
              退出登录
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- 主要内容 -->
    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <!-- 分类管理 -->
        <div class="mb-8">
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-2xl font-bold text-gray-900 dark:text-white">分类管理</h2>
            <button
              @click="showCategoryModal = true"
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
              </svg>
              添加分类
            </button>
          </div>
          
          <div class="bg-white dark:bg-gray-800 shadow overflow-hidden sm:rounded-lg">
            <div class="divide-y divide-gray-200 dark:divide-gray-700">
              <div v-for="category in categories" :key="category.key" class="px-6 py-4 flex justify-between items-center">
                <div>
                  <h3 class="text-lg font-medium text-gray-900 dark:text-white">{{ category.name }}</h3>
                  <p class="text-sm text-gray-500 dark:text-gray-400">分类代码: {{ category.key }}</p>
                </div>
                <div class="flex space-x-2" v-if="category.key !== 'all'">
                  <button
                    @click="editCategory(category)"
                    class="inline-flex items-center px-3 py-1 border border-gray-300 dark:border-gray-600 text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
                  >
                    编辑
                  </button>
                  <button
                    @click="deleteCategory(category)"
                    class="inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md text-red-700 dark:text-red-400 bg-red-100 dark:bg-red-900 hover:bg-red-200 dark:hover:bg-red-800"
                  >
                    删除
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 产品列表 -->
        <div>
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-2xl font-bold text-gray-900 dark:text-white">产品管理</h2>
            <button
              @click="showProductModal = true"
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
              </svg>
              添加产品
            </button>
          </div>

          <!-- 分类筛选 -->
          <div class="mb-4">
            <div class="flex flex-wrap gap-2">
              <button
                v-for="category in categories"
                :key="category.key"
                @click="currentCategory = category.key"
                :class="[
                  'px-4 py-2 rounded-full text-sm font-medium',
                  currentCategory === category.key
                    ? 'bg-blue-600 text-white'
                    : 'bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-600'
                ]"
              >
                {{ category.name }}
              </button>
            </div>
          </div>

          <!-- 产品列表 -->
          <div class="bg-white dark:bg-gray-800 shadow overflow-hidden sm:rounded-lg">
            <div v-if="filteredProducts.length === 0" class="text-center py-12">
              <svg class="mx-auto h-12 w-12 text-gray-400 dark:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"></path>
              </svg>
              <h3 class="mt-2 text-sm font-medium text-gray-900 dark:text-white">暂无产品</h3>
              <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">开始添加您的第一个产品吧</p>
            </div>

            <div v-else class="divide-y divide-gray-200 dark:divide-gray-700">
              <div v-for="product in filteredProducts" :key="product.id" class="p-6">
                <div class="flex items-center justify-between">
                  <div class="flex items-center space-x-4">
                    <!-- 产品主图 -->
                    <div class="flex-shrink-0">
                      <img
                        :src="getPreviewUrl(product.mainImage)"
                        :alt="product.name"
                        class="h-24 w-24 object-cover rounded-lg"
                      />
                    </div>
                    
                    <!-- 产品信息 -->
                    <div class="flex-1 min-w-0">
                      <p class="text-lg font-medium text-gray-900 dark:text-white">
                        {{ product.name }}
                      </p>
                      <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
                        {{ product.description }}
                      </p>
                      <div class="mt-2 flex items-center space-x-4">
                        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200">
                          {{ getCategoryName(product.category) }}
                        </span>
                        <span class="text-sm text-gray-500 dark:text-gray-400">
                          {{ product.images.length }} 个配色
                        </span>
                      </div>
                    </div>
                  </div>
                  
                  <!-- 操作按钮 -->
                  <div class="flex items-center space-x-2">
                    <button
                      @click="editProduct(product)"
                      class="inline-flex items-center px-3 py-2 border border-gray-300 dark:border-gray-600 text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
                    >
                      编辑
                    </button>
                    <button
                      @click="deleteProduct(product)"
                      class="inline-flex items-center px-3 py-2 border border-transparent text-sm font-medium rounded-md text-red-700 dark:text-red-400 bg-red-100 dark:bg-red-900 hover:bg-red-200 dark:hover:bg-red-800"
                    >
                      删除
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 分类编辑模态框 -->
    <div v-if="showCategoryModal" class="fixed inset-0 bg-transparent overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white dark:bg-gray-800 dark:border-gray-600">
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">
            {{ editingCategory ? '编辑分类' : '添加分类' }}
          </h3>
          
          <form @submit.prevent="saveCategoryForm" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">分类名称</label>
              <input
                v-model="categoryForm.name"
                type="text"
                required
                class="mt-1 block w-full border border-gray-300 dark:border-gray-600 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400"
                placeholder="请输入分类名称"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">分类代码</label>
              <input
                v-model="categoryForm.key"
                type="text"
                required
                :disabled="editingCategory"
                class="mt-1 block w-full border border-gray-300 dark:border-gray-600 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100 dark:disabled:bg-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400"
                placeholder="请输入分类代码"
              />
            </div>
            
            <div class="flex justify-end space-x-3 pt-4">
              <button
                type="button"
                @click="closeCategoryModal"
                class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
              >
                取消
              </button>
              <button
                type="submit"
                :disabled="submitting"
                class="px-4 py-2 border border-transparent rounded-md text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50"
              >
                {{ submitting ? '保存中...' : '保存' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- 产品编辑模态框 -->
    <div v-if="showProductModal" class="fixed inset-0 bg-transparent overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-[800px] shadow-lg rounded-md bg-white dark:bg-gray-800 dark:border-gray-600">
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">
            {{ editingProduct ? '编辑产品' : '添加产品' }}
          </h3>
          
          <form @submit.prevent="saveProductForm" class="space-y-4">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">产品名称</label>
                <input
                  v-model="productForm.name"
                  type="text"
                  required
                  class="mt-1 block w-full border border-gray-300 dark:border-gray-600 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400"
                  placeholder="请输入产品名称"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">产品分类</label>
                <select
                  v-model="productForm.category"
                  required
                  class="mt-1 block w-full border border-gray-300 dark:border-gray-600 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                >
                  <option v-for="category in categories.filter(c => c.key !== 'all')" 
                          :key="category.key" 
                          :value="category.key">
                    {{ category.name }}
                  </option>
                </select>
              </div>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">产品描述</label>
              <textarea
                v-model="productForm.description"
                rows="3"
                class="mt-1 block w-full border border-gray-300 dark:border-gray-600 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400"
                placeholder="请输入产品描述"
              ></textarea>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">产品主图</label>
              <ImageSelector v-model="productForm.mainImage" />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">其他配色图片</label>
              <div class="mt-1">
                <ImageSelector 
                  v-model="productForm.images"
                  multiple
                />
              </div>
            </div>
            
            <div class="flex justify-end space-x-3 pt-4">
              <button
                type="button"
                @click="closeProductModal"
                class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
              >
                取消
              </button>
              <button
                type="submit"
                :disabled="submitting"
                class="px-4 py-2 border border-transparent rounded-md text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50"
              >
                {{ submitting ? '保存中...' : '保存' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- 确认删除对话框 -->
    <ConfirmDialog
      v-model:show="showDeleteConfirm"
      :title="deleteDialogConfig.title"
      :message="deleteDialogConfig.message"
      type="danger"
      confirmText="删除"
      cancelText="取消"
      @confirm="confirmDelete"
      @cancel="cancelDelete"
    />

    <!-- 消息提示对话框 -->
    <ConfirmDialog
      v-model:show="showMessageDialog"
      :title="messageDialogConfig.title"
      :message="messageDialogConfig.message"
      :type="messageDialogConfig.type"
      confirmText="确定"
      :showCancel="false"
      @confirm="closeMessageDialog"
      @cancel="closeMessageDialog"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import ImageSelector from '../components/ImageSelector.vue'
import ConfirmDialog from '../components/ConfirmDialog.vue'
import { getImageUrlWithToken } from '../config/env'

const router = useRouter()
const authStore = useAuthStore()

// 响应式数据
const categories = ref([

])
const products = ref([])
const currentCategory = ref('all')
const loading = ref(false)
const submitting = ref(false)

// 模态框状态
const showCategoryModal = ref(false)
const showProductModal = ref(false)
const editingCategory = ref(null)
const editingProduct = ref(null)

// 表单数据
const categoryForm = ref({
  name: '',
  key: ''
})

const   productForm = ref({
  name: '',
  category: '',
  description: '',
  mainImage: '',
  images: []
})

// 对话框配置
const showDeleteConfirm = ref(false)
const deleteDialogConfig = ref({
  title: '',
  message: '',
  type: 'danger',
  callback: null
})

const showMessageDialog = ref(false)
const messageDialogConfig = ref({
  title: '',
  message: '',
  type: 'info'
})

// 计算属性
const filteredProducts = computed(() => {
  if (currentCategory.value === 'all') {
    return products.value
  }
  return products.value.filter(product => product.category === currentCategory.value)
})

// 获取分类名称
const getCategoryName = (key) => {
  const category = categories.value.find(c => c.key === key)
  return category ? category.name : key
}

// 获取预览URL
const getPreviewUrl = (imageUrl) => {
  return getImageUrlWithToken(imageUrl)
}

// 加载数据
const loadData = async () => {
  loading.value = true
  try {
    // 加载分类
    const categoryResponse = await authStore.authenticatedFetch('/api/product/categories')
    if (categoryResponse.ok) {
      const data = await categoryResponse.json()
      categories.value = [{ name: '全部', key: 'all' }, ...data.categories]
    }

    // 加载产品
    const productResponse = await authStore.authenticatedFetch('/api/product/list')
    if (productResponse.ok) {
      const data = await productResponse.json()
      products.value = data.products
    }
  } catch (error) {
    console.error('加载数据失败:', error)
    showMessage('错误', '加载数据失败', 'danger')
  } finally {
    loading.value = false
  }
}

// 分类相关方法
const editCategory = (category) => {
  editingCategory.value = category
  categoryForm.value = { ...category }
  showCategoryModal.value = true
}

const deleteCategory = (category) => {
  deleteDialogConfig.value = {
    title: '删除分类',
    message: `确定要删除分类"${category.name}"吗？删除后无法恢复。`,
    callback: async () => {
      try {
        const response = await authStore.authenticatedFetch(`/api/product/categories/${category.key}`, {
          method: 'DELETE'
        })
        
        if (response.ok) {
          const index = categories.value.findIndex(c => c.key === category.key)
          if (index > -1) {
            categories.value.splice(index, 1)
          }
          showMessage('成功', '分类删除成功', 'info')
        } else {
          const error = await response.json()
          showMessage('错误', error.detail || '删除失败', 'danger')
        }
      } catch (error) {
        console.error('删除分类失败:', error)
        showMessage('错误', '删除失败', 'danger')
      }
    }
  }
  showDeleteConfirm.value = true
}

const saveCategoryForm = async () => {
  if (!categoryForm.value.name || !categoryForm.value.key) {
    showMessage('提示', '请填写完整的分类信息', 'warning')
    return
  }

  submitting.value = true
  try {
    const method = editingCategory.value ? 'PUT' : 'POST'
    const url = editingCategory.value 
      ? `/api/product/categories/${editingCategory.value.key}`
      : '/api/product/categories'
    
    const response = await authStore.authenticatedFetch(url, {
      method,
      body: JSON.stringify(categoryForm.value)
    })
    
    if (response.ok) {
      if (editingCategory.value) {
        const index = categories.value.findIndex(c => c.key === editingCategory.value.key)
        if (index > -1) {
          categories.value[index] = { ...categoryForm.value }
        }
      } else {
        categories.value.push({ ...categoryForm.value })
      }
      
      closeCategoryModal()
      showMessage('成功', `分类${editingCategory.value ? '更新' : '创建'}成功`, 'info')
    } else {
      const error = await response.json()
      showMessage('错误', error.detail || '保存失败', 'danger')
    }
  } catch (error) {
    console.error('保存分类失败:', error)
    showMessage('错误', '保存失败', 'danger')
  } finally {
    submitting.value = false
  }
}

const closeCategoryModal = () => {
  showCategoryModal.value = false
  editingCategory.value = null
  categoryForm.value = {
    name: '',
    key: ''
  }
}

// 产品相关方法
const editProduct = (product) => {
  editingProduct.value = product
  productForm.value = { ...product }
  showProductModal.value = true
}

const deleteProduct = (product) => {
  deleteDialogConfig.value = {
    title: '删除产品',
    message: `确定要删除产品"${product.name}"吗？删除后无法恢复。`,
    callback: async () => {
      try {
        const response = await authStore.authenticatedFetch(`/api/product/${product.id}`, {
          method: 'DELETE'
        })
        
        if (response.ok) {
          const index = products.value.findIndex(p => p.id === product.id)
          if (index > -1) {
            products.value.splice(index, 1)
          }
          showMessage('成功', '产品删除成功', 'info')
        } else {
          const error = await response.json()
          showMessage('错误', error.detail || '删除失败', 'danger')
        }
      } catch (error) {
        console.error('删除产品失败:', error)
        showMessage('错误', '删除失败', 'danger')
      }
    }
  }
  showDeleteConfirm.value = true
}

const saveProductForm = async () => {
  if (!productForm.value.name || !productForm.value.category || !productForm.value.mainImage) {
    showMessage('提示', '请填写必要的产品信息', 'warning')
    return
  }

  submitting.value = true
  try {
    const method = editingProduct.value ? 'PUT' : 'POST'
    const url = editingProduct.value 
      ? `/api/product/${editingProduct.value.id}`
      : '/api/product/new'
    
    console.log('保存产品:', {
      method,
      url,
      token: localStorage.getItem('token'),
      productForm: productForm.value
    })
    
    const response = await authStore.authenticatedFetch(url, {
      method,
      body: JSON.stringify(productForm.value)
    })
    
    if (response.ok) {
      const savedProduct = await response.json()
      
      if (editingProduct.value) {
        const index = products.value.findIndex(p => p.id === editingProduct.value.id)
        if (index > -1) {
          products.value[index] = savedProduct
        }
      } else {
        products.value.push(savedProduct)
      }
      
      closeProductModal()
      showMessage('成功', `产品${editingProduct.value ? '更新' : '创建'}成功`, 'info')
    } else {
      const error = await response.json()
      showMessage('错误', error.detail || '保存失败', 'danger')
    }
  } catch (error) {
    console.error('保存产品失败:', error)
    showMessage('错误', '保存失败', 'danger')
  } finally {
    submitting.value = false
  }
}

const closeProductModal = () => {
  showProductModal.value = false
  editingProduct.value = null
  productForm.value = {
    name: '',
    category: '',
    description: '',
    mainImage: '',
    images: []
  }
}



// 对话框相关方法
const confirmDelete = () => {
  if (deleteDialogConfig.value.callback) {
    deleteDialogConfig.value.callback()
  }
  showDeleteConfirm.value = false
}

const cancelDelete = () => {
  showDeleteConfirm.value = false
  deleteDialogConfig.value.callback = null
}

const showMessage = (title, message, type = 'info') => {
  messageDialogConfig.value = {
    title,
    message,
    type
  }
  showMessageDialog.value = true
}

const closeMessageDialog = () => {
  showMessageDialog.value = false
}

// 退出登录
const handleLogout = async () => {
  try {
    await authStore.logout()
    router.push('/login')
  } catch (error) {
    console.error('退出登录失败:', error)
  }
}

// 组件挂载时加载数据
onMounted(() => {
  loadData()
})
</script> 