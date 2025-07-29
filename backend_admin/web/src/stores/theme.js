import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  // 当前主题模式
  const currentTheme = ref('light')

  // 主题配置
  const themeConfig = {
    light: {
      name: '浅色主题',
      description: '明亮清晰的界面，适合白天使用',
      icon: 'sun',
      dataTheme: 'light'
    },
    dark: {
      name: '深色主题',
      description: '护眼舒适的界面，适合夜间使用',
      icon: 'moon',
      dataTheme: 'dark'
    }
  }

  // 设置主题
  const setTheme = (theme) => {
    if (themeConfig[theme]) {
      currentTheme.value = theme
      applyThemeToDOM(theme)
    }
  }

  // 获取当前主题
  const getCurrentTheme = () => {
    return currentTheme.value
  }

  // 获取主题配置
  const getThemeConfig = (theme = null) => {
    const targetTheme = theme || currentTheme.value
    return themeConfig[targetTheme]
  }

  // 应用主题到DOM
  const applyThemeToDOM = (theme = null) => {
    const targetTheme = theme || currentTheme.value
    const config = themeConfig[targetTheme]
    
    if (config) {
      // 设置 data-theme 属性到 html 元素
      document.documentElement.setAttribute('data-theme', config.dataTheme)
    }
  }

  // 加载保存的主题设置
  const loadThemeSettings = () => {
    try {
      const savedTheme = localStorage.getItem('currentTheme')
      if (savedTheme && themeConfig[savedTheme]) {
        currentTheme.value = savedTheme
        applyThemeToDOM(savedTheme)
      }
    } catch (error) {
      console.error('加载主题设置失败:', error)
    }
  }

  // 保存主题设置
  const saveThemeSettings = () => {
    try {
      localStorage.setItem('currentTheme', currentTheme.value)
      return true
    } catch (error) {
      console.error('保存主题设置失败:', error)
      return false
    }
  }

  // 切换主题
  const toggleTheme = () => {
    const newTheme = currentTheme.value === 'light' ? 'dark' : 'light'
    setTheme(newTheme)
  }

  // 获取所有可用主题
  const getAvailableThemes = () => {
    return Object.keys(themeConfig).map(key => ({
      key,
      ...themeConfig[key]
    }))
  }

  return {
    currentTheme,
    themeConfig,
    setTheme,
    getCurrentTheme,
    getThemeConfig,
    applyThemeToDOM,
    loadThemeSettings,
    saveThemeSettings,
    toggleTheme,
    getAvailableThemes
  }
}) 