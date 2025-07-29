<script>
import { login, getToken } from './utils/api.js'

export default {
  onLaunch: function () {
    console.log('App Launch')
    this.autoLogin()
  },
  onShow: function () {
    console.log('App Show')
  },
  onHide: function () {
    console.log('App Hide')
  },
  methods: {
    // 自动登录
    async autoLogin() {
      try {
        // 每次都执行登录，获取新的token
        const accessKey = '29855e4c-ae10-4582-a473-ad544fce8b19'
        const result = await login(accessKey)
        console.log('登录成功:', result)
        
        uni.showToast({
          title: '登录成功',
          icon: 'success'
        })
      } catch (error) {
        console.error('登录失败:', error)
        uni.showToast({
          title: '登录失败',
          icon: 'error'
        })
      }
    }
  }
}
</script>

<style>
/*每个页面公共css */
</style>
