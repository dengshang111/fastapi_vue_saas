<template>
	<view class="page-container">
		<view class="main-content">
			<!-- 顶部标题 -->
			<view class="header">
				<text class="header-title">供货价表</text>
				<text class="header-subtitle">产品价格信息</text>
			</view>

			<!-- 搜索栏 -->
			<view class="search-section">
				<view class="search-box">
					<text class="search-icon">🔍</text>
					<input 
						class="search-input" 
						placeholder="搜索产品系列或型号" 
						v-model="searchKeyword"
						@input="handleSearch"
					/>
				</view>
			</view>

			<!-- 分类标签 -->
			<view class="category-tabs">
				<scroll-view class="tabs-scroll" scroll-x="true">
					<view class="tabs-container">
						<view 
							class="tab-item" 
							:class="{ active: activeCategory === index }"
							v-for="(category, index) in categories" 
							:key="index"
							@click="switchCategory(index)"
						>
							<text class="tab-text">{{ category.name }}</text>
						</view>
					</view>
				</scroll-view>
			</view>

			<!-- 产品列表 -->
			<view class="product-section">
				<view class="product-grid">
					<view 
						class="product-item" 
						v-for="(product, index) in filteredProducts" 
						:key="index"
						@click="previewProduct(product)"
					>
						<view class="product-image-container">
							<image 
								class="product-image" 
								:src="product.mainImage" 
								mode="aspectFill"
								@error="handleImageError"
							></image>
							<view class="product-overlay">
								<text class="preview-text">点击预览</text>
							</view>
						</view>
						<view class="product-info">
							<text class="product-name">{{ product.name }}</text>
							<text class="product-price">{{ product.price }}</text>
						</view>
					</view>
				</view>
			</view>

			<!-- 空状态 -->
			<view class="empty-state" v-if="filteredProducts.length === 0">
				<text class="empty-text">暂无相关产品</text>
			</view>
		</view>

		<!-- 图片预览弹窗 -->
		<view class="preview-modal" v-if="showPreview" @click="closePreview">
			<view class="preview-content" @click.stop>
				<view class="preview-header">
					<text class="preview-title">{{ currentProduct.name }}</text>
					<text class="close-btn" @click="closePreview">×</text>
				</view>
				<swiper class="preview-swiper" :indicator-dots="true" indicator-color="rgba(255, 255, 255, 0.6)"
					indicator-active-color="#FFF">
					<swiper-item v-for="(image, index) in currentProduct.images" :key="index">
						<image class="preview-image" :src="image" mode="aspectFit"></image>
					</swiper-item>
				</swiper>
				<view class="preview-info">
					<text class="preview-price">{{ currentProduct.price }}</text>
					<text class="preview-description">{{ currentProduct.description }}</text>
				</view>
			</view>
		</view>

		<!-- 底部导航栏 -->
		<view class="tab-bar">
			<view 
				class="tab-item" 
				:class="{ active: activeTab === index }"
				v-for="(item, index) in tabItems" 
				:key="index"
				@click="switchTab(index)"
			>
				<image 
					class="tab-icon" 
					:src="activeTab === index ? item.activeIcon : item.icon"
				></image>
				<text class="tab-text">{{ item.text }}</text>
			</view>
		</view>
	</view>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';

// 搜索关键词
const searchKeyword = ref('');

// 当前选中的分类
const activeCategory = ref(0);

// 预览相关
const showPreview = ref(false);
const currentProduct = ref({});

// 底部导航
const activeTab = ref(1); // provider页面

// 分类数据
const categories = ref([
	{ name: '全部', key: 'all' },
	{ name: 'CY系列', key: 'CY' },
	{ name: 'CZYL系列', key: 'CZYL' },
	{ name: 'HH系列', key: 'HH' },
	{ name: 'HS系列', key: 'HS' },
	{ name: 'JT系列', key: 'JT' },
	{ name: 'RD868系列', key: 'RD868' },
	{ name: 'SXH系列', key: 'SXH' },
	{ name: 'XW系列', key: 'XW' },
	{ name: '润达工厂', key: '润达工厂' }
]);

// 产品数据
const products = ref([
	// CY系列
	{
		id: 'CY25-1',
		name: 'CY25-1',
		price: '供货价',
		category: 'CY',
		description: 'CY25-1系列产品',
		mainImage: 'https://pic1.imgdb.cn/item/153625/CY25-1供货价.jpg',
		images: ['https://pic1.imgdb.cn/item/153625/CY25-1供货价.jpg']
	},
	{
		id: 'CY25-3',
		name: 'CY25-3',
		price: '供货价27',
		category: 'CY',
		description: 'CY25-3系列产品',
		mainImage: 'https://pic1.imgdb.cn/item/153625/CY25-3供货价27.jpg',
		images: ['https://pic1.imgdb.cn/item/153625/CY25-3供货价27.jpg']
	},
	{
		id: 'CY25-6',
		name: 'CY25-6',
		price: '供货价29',
		category: 'CY',
		description: 'CY25-6系列产品',
		mainImage: 'https://pic1.imgdb.cn/item/153625/CY25-6供货价29.jpg',
		images: ['https://pic1.imgdb.cn/item/153625/CY25-6供货价29.jpg']
	},
	{
		id: 'CY25-7',
		name: 'CY25-7',
		price: '供货价27',
		category: 'CY',
		description: 'CY25-7系列产品',
		mainImage: 'https://pic1.imgdb.cn/item/153625/CY25-7供货价27.jpg',
		images: ['https://pic1.imgdb.cn/item/153625/CY25-7供货价27.jpg']
	},
	{
		id: 'CY25-8',
		name: 'CY25-8',
		price: '供货价28',
		category: 'CY',
		description: 'CY25-8系列产品',
		mainImage: 'https://pic1.imgdb.cn/item/153625/CY25-8供货价28.jpg',
		images: [
			'https://pic1.imgdb.cn/item/153625/CY25-8供货价28.jpg',
			'https://pic1.imgdb.cn/item/153625/IMGM8379.jpg',
			'https://pic1.imgdb.cn/item/153625/IMGM8390.jpg',
			'https://pic1.imgdb.cn/item/153625/IMGM8395.jpg'
		]
	},
	{
		id: 'CY25-9',
		name: 'CY25-9',
		price: '供货价27',
		category: 'CY',
		description: 'CY25-9系列产品',
		mainImage: 'https://pic1.imgdb.cn/item/153625/CY25-9供货价27.jpg',
		images: [
			'https://pic1.imgdb.cn/item/153625/CY25-9供货价27.jpg',
			'https://pic1.imgdb.cn/item/153625/IMGM8359.jpg',
			'https://pic1.imgdb.cn/item/153625/IMGM8363.jpg',
			'https://pic1.imgdb.cn/item/153625/IMGM8365.jpg'
		]
	},
	// CZYL系列
	// {
	// 	id: 'CZYL888-2',
	// 	name: 'CZYL888-2黑色',
	// 	price: '供货价18',
	// 	category: 'CZYL',
	// 	description: 'CZYL888-2黑色系列产品',
	// 	mainImage: 'https://pic1.imgdb.cn/item/153625/DSC05875+.jpg',
	// 	images: ['https://pic1.imgdb.cn/item/153625/DSC05875+.jpg']
	// },
	// {
	// 	id: 'CZYL888-3',
	// 	name: 'CZYL888-3白色',
	// 	price: '供货价19',
	// 	category: 'CZYL',
	// 	description: 'CZYL888-3白色系列产品',
	// 	mainImage: 'https://pic1.imgdb.cn/item/153625/DSC05885+.jpg',
	// 	images: ['https://pic1.imgdb.cn/item/153625/DSC05885+.jpg']
	// },
	// {
	// 	id: 'CZYL888-4',
	// 	name: 'CZYL888-4棕色',
	// 	price: '已上架',
	// 	category: 'CZYL',
	// 	description: 'CZYL888-4棕色系列产品',
	// 	mainImage: 'https://pic1.imgdb.cn/item/153625/DSC05890+.jpg',
	// 	images: ['https://pic1.imgdb.cn/item/153625/DSC05890+.jpg']
	// },
	// HH系列
	{
		id: 'HH023-49',
		name: '023-49',
		price: '供货价35',
		category: 'HH',
		description: 'HH系列023-49产品',
		mainImage: 'https://pic1.imgdb.cn/item/153625/IMGM9406.jpg',
		images: ['https://pic1.imgdb.cn/item/153625/IMGM9406.jpg']
	},
	{
		id: 'HH023-51',
		name: '023-51',
		price: '供货价36',
		category: 'HH',
		description: 'HH系列023-51产品',
		mainImage: 'https://pic1.imgdb.cn/item/153625/IMGM9342.jpg',
		images: ['https://pic1.imgdb.cn/item/153625/IMGM9342.jpg']
	},
	// HS系列
	{
		id: 'HS567-1',
		name: 'HS567-1',
		price: '供货价33',
		category: 'HS',
		description: 'HS567-1系列产品',
		mainImage: 'https://pic1.imgdb.cn/item/153625/IMGM3611.jpg',
		images: ['https://pic1.imgdb.cn/item/153625/IMGM3611.jpg']
	},
	{
		id: 'HS567-2',
		name: 'HS567-2',
		price: '供货价33',
		category: 'HS',
		description: 'HS567-2系列产品',
		mainImage: 'https://pic1.imgdb.cn/item/153625/IMGM3635.jpg',
		images: ['https://pic1.imgdb.cn/item/153625/IMGM3635.jpg']
	},
	// JT系列
	// {
	// 	id: 'JT19114-1',
	// 	name: '19114-1金.银',
	// 	price: '供货价38',
	// 	category: 'JT',
	// 	description: 'JT系列19114-1金.银产品',
	// 	mainImage: 'https://pic1.imgdb.cn/item/153625/IMGM8417.jpg',
	// 	images: ['https://pic1.imgdb.cn/item/153625/IMGM8417.jpg']
	// },
	// {
	// 	id: 'JT19114-2',
	// 	name: '19114-2金色',
	// 	price: '供货价40',
	// 	category: 'JT',
	// 	description: 'JT系列19114-2金色产品',
	// 	mainImage: 'https://pic1.imgdb.cn/item/153625/IMGM8432.jpg',
	// 	images: ['https://pic1.imgdb.cn/item/153625/IMGM8432.jpg']
	// },
	// // RD868系列
	// {
	// 	id: 'RD868-1',
	// 	name: 'RD868-1金色',
	// 	price: '供货价36',
	// 	category: 'RD868',
	// 	description: 'RD868-1金色系列产品',
	// 	mainImage: 'https://pic1.imgdb.cn/item/153625/DSC09218+.JPG',
	// 	images: ['https://pic1.imgdb.cn/item/153625/DSC09218+.JPG']
	// },
	// {
	// 	id: 'RD868-4',
	// 	name: 'RD868-4银色',
	// 	price: '供货价36',
	// 	category: 'RD868',
	// 	description: 'RD868-4银色系列产品',
	// 	mainImage: 'https://pic1.imgdb.cn/item/153625/DSC09163+.JPG',
	// 	images: ['https://pic1.imgdb.cn/item/153625/DSC09163+.JPG']
	// },
	// // SXH系列
	// {
	// 	id: 'SXH9136-1',
	// 	name: 'SXH9136-1黑色',
	// 	price: '供货价13',
	// 	category: 'SXH',
	// 	description: 'SXH9136-1黑色系列产品',
	// 	mainImage: 'https://pic1.imgdb.cn/item/153625/',
	// 	images: []
	// },
	// {
	// 	id: 'SXH9136-2',
	// 	name: 'SXH9136-2黑色',
	// 	price: '供货价39',
	// 	category: 'SXH',
	// 	description: 'SXH9136-2黑色系列产品',
	// 	mainImage: 'https://pic1.imgdb.cn/item/153625/DSC05908+.jpg',
	// 	images: ['https://pic1.imgdb.cn/item/153625/DSC05908+.jpg']
	// },
	// XW系列
	{
		id: 'XW206-11',
		name: '206-11白色',
		price: '供货价36',
		category: 'XW',
		description: 'XW系列206-11白色产品',
		mainImage: 'https://pic1.imgdb.cn/item/153625/IMGM7788.jpg',
		images: ['https://pic1.imgdb.cn/item/153625/IMGM7788.jpg']
	},
	{
		id: 'XW8888-1',
		name: '8888-1黑色',
		price: '供货价26',
		category: 'XW',
		description: 'XW系列8888-1黑色产品',
		mainImage: 'https://pic1.imgdb.cn/item/153625/IMGM4653.jpg',
		images: ['https://pic1.imgdb.cn/item/153625/IMGM4653.jpg']
	},
	// 润达工厂
	// {
	// 	id: '润达RD868-1',
	// 	name: 'RD868-1金色',
	// 	price: '供货价36',
	// 	category: '润达工厂',
	// 	description: '润达工厂RD868-1金色产品',
	// 	mainImage: 'https://pic1.imgdb.cn/item/153625/DSC09200+.JPG',
	// 	images: ['https://pic1.imgdb.cn/item/153625/DSC09200+.JPG']
	// }
]);

// 底部导航
const tabItems = ref([
	{ icon: 'https://pic1.imgdb.cn/item/153625/home.png', activeIcon: 'https://pic1.imgdb.cn/item/153625/home-active.png', text: '首页' },
	{ icon: 'https://pic1.imgdb.cn/item/153625/provider.png', activeIcon: 'https://pic1.imgdb.cn/item/153625/provider-active.png', text: '产品信息' },
	{ icon: 'https://pic1.imgdb.cn/item/153625/about.png', activeIcon: 'https://pic1.imgdb.cn/item/153625/about-active.png', text: '关于我们' }
]);

// 计算属性：过滤后的产品列表
const filteredProducts = computed(() => {
	let filtered = products.value;
	
	// 按分类过滤
	if (activeCategory.value > 0) {
		const categoryKey = categories.value[activeCategory.value].key;
		filtered = filtered.filter(product => product.category === categoryKey);
	}
	
	// 按搜索关键词过滤
	if (searchKeyword.value.trim()) {
		const keyword = searchKeyword.value.toLowerCase();
		filtered = filtered.filter(product => 
			product.name.toLowerCase().includes(keyword) ||
			product.description.toLowerCase().includes(keyword) ||
			product.price.toLowerCase().includes(keyword)
		);
	}
	
	return filtered;
});

// 切换分类
const switchCategory = (index) => {
	activeCategory.value = index;
};

// 搜索处理
const handleSearch = () => {
	// 搜索逻辑已在计算属性中处理
};

// 预览产品
const previewProduct = (product) => {
	currentProduct.value = product;
	showPreview.value = true;
};

// 关闭预览
const closePreview = () => {
	showPreview.value = false;
	currentProduct.value = {};
};

// 切换底部导航
const switchTab = (index) => {
	activeTab.value = index;
	
	// 根据点击的标签进行页面跳转
	const tabItem = tabItems.value[index];
	
	if (tabItem.text === '首页') {
		// 跳转到首页
		uni.navigateTo({
			url: '/pages/index/index'
		});
	} else if (tabItem.text === '关于我们') {
		// 跳转到关于我们页面
		uni.navigateTo({
			url: '/pages/index/aboutus'
		});
	}
	// 供货价表已经在当前页面，不需要跳转
};

// 图片加载错误处理
const handleImageError = (e) => {
	console.log('图片加载失败:', e);
};

onMounted(() => {
	// 页面加载完成后的初始化逻辑
});
</script>

<style lang="scss" scoped>
.page-container {
	display: flex;
	flex-direction: column;
	height: 100vh;
	background-color: #f5f5f5;
}

.main-content {
	flex: 1;
	overflow-y: auto;
	padding-bottom: 120rpx;
}

.header {
	padding: 40rpx 30rpx 20rpx;
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	color: white;
}

.header-title {
	font-size: 48rpx;
	font-weight: bold;
	display: block;
	margin-bottom: 10rpx;
}

.header-subtitle {
	font-size: 28rpx;
	opacity: 0.9;
}

.search-section {
	padding: 20rpx 30rpx;
	background-color: white;
}

.search-box {
	display: flex;
	align-items: center;
	background-color: #f8f9fa;
	border-radius: 50rpx;
	padding: 20rpx 30rpx;
}

.search-icon {
	font-size: 32rpx;
	margin-right: 20rpx;
	color: #999;
}

.search-input {
	flex: 1;
	font-size: 28rpx;
	color: #333;
}

.category-tabs {
	background-color: white;
	padding: 20rpx 0;
	border-bottom: 1rpx solid #eee;
}

.tabs-scroll {
	white-space: nowrap;
}

.tabs-container {
	display: flex;
	padding: 0 30rpx;
}

.tab-item {
	padding: 16rpx 32rpx;
	margin-right: 20rpx;
	border-radius: 50rpx;
	
	transition: all 0.3s ease;
	
	// &.active {
	// 	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	// 	color: white;
	// }
}

.tab-text {
	font-size: 26rpx;
	white-space: nowrap;
}

.product-section {
	padding: 20rpx;
}

.product-grid {
	display: grid;
	grid-template-columns: repeat(2, 1fr);
	gap: 20rpx;
}

.product-item {
	background-color: white;
	border-radius: 16rpx;
	overflow: hidden;
	box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
	transition: transform 0.3s ease;
	
	&:active {
		transform: scale(0.98);
	}
}

.product-image-container {
	position: relative;
	height: 300rpx;
	overflow: hidden;
}

.product-image {
	width: 100%;
	height: 100%;
}

.product-overlay {
	position: absolute;
	top: 0;
	left: 0;
	right: 0;
	bottom: 0;
	background: rgba(0, 0, 0, 0.5);
	display: flex;
	align-items: center;
	justify-content: center;
	opacity: 0;
	transition: opacity 0.3s ease;
}

.product-item:active .product-overlay {
	opacity: 1;
}

.preview-text {
	color: white;
	font-size: 28rpx;
	font-weight: bold;
}

.product-info {
	padding: 20rpx;
}

.product-name {
	font-size: 28rpx;
	font-weight: bold;
	color: #333;
	margin-bottom: 8rpx;
	display: block;
}

.product-price {
	font-size: 24rpx;
	color: #e54d42;
	font-weight: bold;
}

.empty-state {
	display: flex;
	align-items: center;
	justify-content: center;
	padding: 100rpx 30rpx;
}

.empty-text {
	font-size: 28rpx;
	color: #999;
}

.preview-modal {
	position: fixed;
	top: 0;
	left: 0;
	right: 0;
	bottom: 0;
	background: rgba(0, 0, 0, 0.8);
	z-index: 1000;
	display: flex;
	align-items: center;
	justify-content: center;
}

.preview-content {
	width: 90%;
	height: 80%;
	background: white;
	border-radius: 16rpx;
	overflow: hidden;
	display: flex;
	flex-direction: column;
}

.preview-header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding: 30rpx;
	border-bottom: 1rpx solid #eee;
}

.preview-title {
	font-size: 32rpx;
	font-weight: bold;
	color: #333;
}

.close-btn {
	font-size: 48rpx;
	color: #999;
	padding: 10rpx;
}

.preview-swiper {
	flex: 1;
}

.preview-image {
	width: 100%;
	height: 100%;
}

.preview-info {
	padding: 30rpx;
	border-top: 1rpx solid #eee;
}

.preview-price {
	font-size: 36rpx;
	font-weight: bold;
	color: #e54d42;
	margin-bottom: 10rpx;
	display: block;
}

.preview-description {
	font-size: 28rpx;
	color: #666;
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

.tab-icon {
	width: 50rpx;
	height: 50rpx;
	margin-bottom: 8rpx;
}

.tab-text {
	font-size: 24rpx;
}
</style>
