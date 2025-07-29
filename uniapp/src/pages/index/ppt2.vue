<template>
	<view class="page-container">
		<view class="main-content">
			<!-- PPT图片列表 -->
			<view class="ppt-container">
				<view 
					class="ppt-item" 
					v-for="(item, index) in pptImages" 
					:key="index"
				>
					<image 
						class="ppt-image" 
						:src="item.image" 
						mode="widthFix"
						@click="previewImage(item.image, index)"
					></image>
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

// PPT图片数据
const pptImages = ref([
	{ image: 'https://pic1.imgdb.cn/item/685a940058cb8da5c86c17de.jpg' },
	{ image: 'https://pic1.imgdb.cn/item/685a940058cb8da5c86c17df.jpg' },
	{ image: 'https://pic1.imgdb.cn/item/685a940058cb8da5c86c17e1.jpg' },
	{ image: 'https://pic1.imgdb.cn/item/685a940058cb8da5c86c17dd.jpg' },
	{ image: 'https://pic1.imgdb.cn/item/685a940058cb8da5c86c17e0.jpg' },
	
	{ image: 'https://pic1.imgdb.cn/item/685a944c58cb8da5c86c1ae1.jpg' },
	{ image: 'https://pic1.imgdb.cn/item/685a944c58cb8da5c86c1ade.jpg' },
	{ image: 'https://pic1.imgdb.cn/item/685a944c58cb8da5c86c1adf.jpg' },
	{ image: 'https://pic1.imgdb.cn/item/685a944c58cb8da5c86c1ae2.jpg' },
	{ image: 'https://pic1.imgdb.cn/item/685a944c58cb8da5c86c1add.jpg' },

	{ image: 'https://pic1.imgdb.cn/item/685a94c858cb8da5c86c2077.jpg' },
	{ image: 'https://pic1.imgdb.cn/item/685a94c858cb8da5c86c2076.jpg' },
	{ image: 'https://pic1.imgdb.cn/item/685a94c858cb8da5c86c2074.jpg' },
	{ image: 'https://pic1.imgdb.cn/item/685a94c858cb8da5c86c2078.jpg' },
	{ image: 'https://pic1.imgdb.cn/item/685a94c858cb8da5c86c2079.jpg' },

	{ image: 'https://pic1.imgdb.cn/item/685a952358cb8da5c86c232c.jpg' },
	{ image: 'https://pic1.imgdb.cn/item/685a952358cb8da5c86c232b.jpg' },
	{ image: 'https://pic1.imgdb.cn/item/685a952358cb8da5c86c232a.jpg' },
	{ image: 'https://pic1.imgdb.cn/item/685a952358cb8da5c86c232e.jpg' },
	// 您可以继续添加更多PPT图片
	// { image: '您的PPT图片URL' },
]);

// 预览图片功能
const previewImage = (current, index) => {
	uni.previewImage({
		current: current,
		urls: pptImages.value.map(item => item.image)
	});
};

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
		card: {
			title: '高层管理者领导力提示',
			subtitle: '与发展研修项目',
			bgImage: '/static/page1/card-bg.png'
		}
	},
	{
		tag: '金昇贸易',
		title: '另一个热门的研修项目介绍',
		card: {
			title: '热门项目核心内容',
			subtitle: '学习与实践',
			bgImage: '/static/page1/card-bg-2.png' // 请确保您有这个图片
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
	
	.consult-section {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 30rpx;
		background-color: #ffffff;
		margin-top: 20rpx;
	}
	
	.logo-placeholder {
		width: 200rpx;
		height: 80rpx;
	}
	
	.consult-button {
		background-image: linear-gradient(to right, #3d6eb2, #4a87d3);
		color: white;
		padding: 20rpx 60rpx;
		border-radius: 40rpx;
		box-shadow: 0 4rpx 10rpx rgba(0, 0, 0, 0.1);
	}

	.consult-text {
		font-size: 32rpx;
		font-weight: bold;
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
		position: absolute;
		bottom: -20rpx;
		right: -20rpx;
		width: 150rpx;
		height: 100rpx;
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

	// PPT图片列表样式
	.ppt-container {
		padding: 20rpx;
	}

	.ppt-item {
		margin-bottom: 20rpx;
		background-color: #ffffff;
		border-radius: 12rpx;
		overflow: hidden;
		box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.1);
	}

	.ppt-image {
		width: 100%;
		height: auto;
		display: block;
	}

</style>
