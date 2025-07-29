<template>
	<view class="page-container">
		<view class="main-content">
			<!-- 1. Swiper -->
			<swiper class="swiper" circular :indicator-dots="true" indicator-color="rgba(255, 255, 255, 0.6)"
				indicator-active-color="#FFF" :autoplay="true" :interval="3000" :duration="500">
				<swiper-item v-for="(item, index) in swiperList" :key="index">
					<view class="swiper-item">
						<image :src="item.image" class="banner-image" mode="aspectFill"></image>
						<view class="swiper-text-overlay">
							<text class="new-course-text">{{ item.title }}</text>
						</view>
					</view>
				</swiper-item>
			</swiper>

			<!-- 2. Nav Menu -->
			<view class="nav-grid">
				<view class="nav-item" v-for="(item, index) in navItems" :key="index" @click="handleNavClick(item, index)">
					<!-- 请替换为您的图标 -->
					<image class="nav-icon" :src="item.icon"></image>
					<text class="nav-text">{{ item.text }}</text>
				</view>
			</view>

			<!-- 3. Contact Section -->
			<view class="contact-section">
				<view class="contact-header">
					<text class="contact-title">联系我们</text>
					<text class="contact-subtitle">随时为您提供专业服务</text>
				</view>
				<view class="contact-cards">
					<view class="contact-card phone-card" @click="makePhoneCall">
						<view class="card-icon">
							<text class="icon-text">📞</text>
						</view>
						<view class="card-content">
							<text class="card-label">联系电话</text>
							
							<text class="card-value">132-1754-8970</text>
						</view>
					</view>
					<button class="contact-card wechat-card" open-type="contact">
						<view class="card-icon">
							<text class="icon-text">💬</text>
						</view>
						<view class="card-content">
							<text class="card-label">微信咨询</text>
							<text class="card-value">点击联系客服</text>
						</view>
					</button>
				</view>
			</view>

			<!-- 4. Content Section -->
			<view class="content-section">
				<text class="content-main-title">企业近期内容</text>
				<view class="course-item" v-for="(course, index) in courseList" :key="index" @click="handleCourseClick(course, index)">
					<view class="course-tag-wrapper">
						<text class="course-tag">{{ course.tag }}</text>
						<text class="course-title">{{ course.title }}</text>
					</view>
					<view class="course-card">
						<text class="card-title">{{ course.card.title }}</text>
						<text class="card-subtitle">{{ course.card.subtitle }}</text>
						<image class="card-bg-shape" :src="course.card.bgImage" mode="widthFix"></image>
					</view>
				</view>
			</view>
		</view>

		<!-- 5. Custom Tab Bar -->
		<view class="tab-bar">
			<view 
				class="tab-item" 
				:class="{ active: activeTab === index }"
				v-for="(item, index) in tabItems" 
				:key="index"
				@click="handleTabClick(index)"
			>
				<image 
					class="tab-icon-placeholder" 
					:class="{ 'home-icon': index === 0 }"
					:src="activeTab === index ? item.activeIcon : item.icon"
				></image>
				<text>{{ item.text }}</text>
			</view>
		</view>
	</view>
</template>

<script setup>
import { ref } from 'vue';


const swiperList = ref([
	{ title: '', image: 'https://pic1.imgdb.cn/item/68596a1e58cb8da5c8688dbc.jpg' },
	{ title: '', image: 'https://pic1.imgdb.cn/item/68596c4a58cb8da5c8689428.jpg' },
  { title: '', image: 'https://pic1.imgdb.cn/item/68596c8158cb8da5c868947b.jpg' },
	{ title: '', image: 'https://pic1.imgdb.cn/item/68596cc558cb8da5c8689545.jpg' },
  { title: '', image: 'https://pic1.imgdb.cn/item/68596cef58cb8da5c8689616.jpg' },

]);

const courseList = ref([
	{
		tag: '金昇贸易',
		title: '高层管理者领导力提升与发展研修项目',
		pagePath: '/pages/index/ppt1',
		card: {
			title: '高层管理者领导力提示',
			subtitle: '与发展研修项目',
			bgImage: 'https://pic1.imgdb.cn/item/685a91ba58cb8da5c86c1023.jpg'
		}
	},
	{
		tag: '金昇贸易',
		title: '另一个热门的研修项目介绍',
		pagePath: '/pages/index/ppt2',
		card: {
			title: '热门项目核心内容',
			subtitle: '学习与实践',
			bgImage: 'https://pic1.imgdb.cn/item/685a940058cb8da5c86c17de.jpg' // 请确保您有这个图片
		}
	}
]);

const navItems = ref([
	{ icon: 'https://pic1.imgdb.cn/item/153625/provider.png', text: '产品信息' },
	{ icon: 'https://pic1.imgdb.cn/item/153625/about.png', text: '关于我们' }
]);

const tabItems = ref([
	{ icon: 'https://pic1.imgdb.cn/item/153625/home.png', activeIcon: 'https://pic1.imgdb.cn/item/153625/home-active.png', text: '首页' },
	{ icon: 'https://pic1.imgdb.cn/item/153625/provider.png', activeIcon: 'https://pic1.imgdb.cn/item/153625/provider-active.png', text: '产品信息' },
	{ icon: 'https://pic1.imgdb.cn/item/153625/about.png', activeIcon: 'https://pic1.imgdb.cn/item/153625/about-active.png', text: '关于我们' }
]);

const activeTab = ref(0);

const handleNavClick = (item, index) => {
	// 处理导航菜单点击事件
	if (item.text === '产品信息') {
		// 跳转到供货价表页面
		uni.navigateTo({
			url: '/pages/index/provider'
		});
	} else if (item.text === '关于我们') {
		// 跳转到关于我们页面
		uni.navigateTo({
			url: '/pages/index/aboutus'
		});
	}
};

const handleTabClick = (index) => {
	// 处理底部标签栏点击事件
	const tabItem = tabItems.value[index];
	
	if (tabItem.text === '产品信息') {
		// 跳转到供货价表页面
		uni.navigateTo({
			url: '/pages/index/provider'
		});
	} else if (tabItem.text === '关于我们') {
		// 跳转到关于我们页面
		uni.navigateTo({
			url: '/pages/index/aboutus'
		});
	} else if (tabItem.text === '首页') {
		// 首页已经在当前页面，不需要跳转
		activeTab.value = index;
	}
};

const handleCourseClick = (course, index) => {
	// 处理课程卡片点击事件
	if (course.pagePath) {
		uni.navigateTo({
			url: course.pagePath
		});
	}
};

const makePhoneCall = () => {
	// 拨打电话
	uni.makePhoneCall({
		phoneNumber: '138-8888-8888',
		success: () => {
			console.log('拨打电话成功');
		},
		fail: (err) => {
			console.log('拨打电话失败', err);
		}
	});
};
</script>

<style lang="scss" scoped>
	.page-container {
		display: flex;
		flex-direction: column;
		height: 100vh;
		background-color: #f7f7f7;
	}

	.main-content {
		flex: 1;
		overflow-y: auto;
		padding-bottom: 120rpx; // for tab bar
	}

	.swiper {
		width: 100%;
		height: 400rpx;
	}

	.swiper-item {
		position: relative;
		width: 100%;
		height: 100%;
		background-color: #3375b3; // Placeholder color
	}

	.banner-image {
		width: 100%;
		height: 100%;
	}
	
	.swiper-text-overlay {
		position: absolute;
		top: 40rpx;
		left: 40rpx;
		color: white;
	}
	
	.new-course-text {
		font-size: 48rpx;
		font-weight: bold;
	}

	.nav-grid {
		display: flex;
		justify-content: space-around;
		padding: 30rpx 20rpx;
		background-color: #ffffff;
	}

	.nav-item {
		display: flex;
		flex-direction: column;
		align-items: center;
		font-size: 28rpx;
		color: #333;
	}
	
	.nav-icon {
		width: 90rpx;
		height: 90rpx;
		border-radius: 16rpx;
		margin-bottom: 15rpx;
	}

	.nav-text {
		font-size: 26rpx;
	}
	
	.contact-section {
		padding: 40rpx 30rpx;
		background-color: #ffffff;
		margin-top: 20rpx;
	}
	
	.contact-header {
		text-align: center;
		margin-bottom: 40rpx;
	}
	
	.contact-title {
		font-size: 36rpx;
		font-weight: bold;
		color: #333;
		display: block;
		margin-bottom: 10rpx;
	}
	
	.contact-subtitle {
		font-size: 28rpx;
		color: #666;
		display: block;
	}
	
	.contact-cards {
		display: flex;
		gap: 20rpx;
	}
	
	.contact-card {
		flex: 1;
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
		border-radius: 20rpx;
		padding: 30rpx;
		position: relative;
		overflow: hidden;
		box-shadow: 0 8rpx 25rpx rgba(102, 126, 234, 0.15);
		border: none;
		text-align: left;
		line-height: normal;
		
		&::after {
			border: none;
		}
	}
	
	.wechat-card {
		background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
		box-shadow: 0 8rpx 25rpx rgba(240, 147, 251, 0.15);
	}
	
	.card-icon {
		width: 80rpx;
		height: 80rpx;
		background: rgba(255, 255, 255, 0.2);
		border-radius: 50%;
		display: flex;
		align-items: center;
		justify-content: center;
		margin-bottom: 20rpx;
	}
	
	.icon-text {
		font-size: 40rpx;
	}
	
	.card-content {
		margin-bottom: 15rpx;
	}
	
	.card-label {
		font-size: 24rpx;
		color: rgba(255, 255, 255, 0.8);
		display: block;
		margin-bottom: 8rpx;
	}
	
	.card-value {
		font-size: 32rpx;
		font-weight: bold;
		color: white;
		display: block;
	}
	
	.qr-code {
		width: 80rpx;
		height: 80rpx;
		border-radius: 12rpx;
		border: 3rpx solid rgba(255, 255, 255, 0.3);
		position: absolute;
		top: 30rpx;
		right: 30rpx;
	}

	.content-section {
		margin-top: 20rpx;
		padding: 30rpx;
		background-color: #ffffff;
	}
	
	.content-main-title {
		font-size: 34rpx;
		font-weight: bold;
		color: #333;
		margin-bottom: 20rpx;
	}
	
	.course-item {
		margin-top: 20rpx;
		cursor: pointer;
		transition: transform 0.2s ease;
		
		&:hover {
			transform: translateY(-2rpx);
		}
	}
	
	.course-tag-wrapper {
		display: flex;
		align-items: center;
		margin-bottom: 20rpx;
	}
	
	.course-tag {
		background-color: #e54d42;
		color: white;
		padding: 8rpx 16rpx;
		border-radius: 8rpx;
		font-size: 24rpx;
		margin-right: 16rpx;
	}
	
	.course-title {
		font-size: 28rpx;
		color: #666;
	}
	
	.course-card {
		background-color: #003366;
		color: white;
		padding: 40rpx;
		border-radius: 16rpx;
		position: relative;
		overflow: hidden;
		cursor: pointer;
	}
	
	.card-title {
		font-size: 40rpx;
		font-weight: bold;
	}
	
	.card-subtitle {
		font-size: 32rpx;
		margin-top: 10rpx;
	}

	.card-bg-shape {
		width: 100%;
		margin-top: 20rpx;
		border-radius: 8rpx;
	}

	.tab-bar {
		position: fixed;
		bottom: 0;
		left: 0;
		right: 0;
		height: 120rpx;
		background: #ffffff;
		display: flex;
		justify-content: space-around;
		align-items: center;
		border-top: 1rpx solid #e0e0e0;
		padding-bottom: env(safe-area-inset-bottom);
	}

	.tab-item {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		font-size: 24rpx;
		color: #666;
		
		&.active {
			color: #e54d42;
		}
	}
	
	.tab-icon-placeholder {
		width: 50rpx;
		height: 50rpx;
		margin-bottom: 8rpx;
	}

	.contact-button {
		background-color: rgba(255, 255, 255, 0.2);
		color: white;
		border: 2rpx solid rgba(255, 255, 255, 0.3);
		border-radius: 12rpx;
		padding: 16rpx 32rpx;
		font-size: 26rpx;
		font-weight: bold;
		position: absolute;
		top: 30rpx;
		right: 30rpx;
		width: auto;
		height: auto;
		line-height: 1.2;
		text-align: center;
	}

</style>
