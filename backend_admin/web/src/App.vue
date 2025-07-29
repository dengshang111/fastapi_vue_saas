<script setup>
import { RouterView } from 'vue-router'
import { onMounted } from 'vue'
import { useThemeStore } from './stores/theme'

const themeStore = useThemeStore()

onMounted(() => {
  // 初始化主题设置
  themeStore.loadThemeSettings()
})
</script>

<template>
  <div id="app">
    <RouterView />
  </div>
</template>

