<template>
	<view 
		class="page-container" 
		@touchstart="handleTouchStart"
		@touchend="handleTouchEnd"
		@wheel.prevent="handleWheel"
		:style="{ '--theme-color': themeColor }"
	>
		<view class="content-wrapper" :style="{ transform: `translateY(-${currentSectionIndex * 100}vh)` }">
			<view
				v-for="(section, index) in sections"
				:key="index"
				class="section"
				:class="[section.type, { 'active': index === currentSectionIndex, 'is-leaving': index === leavingSectionIndex }]"
			>
				<view class="section-content">
					<view class="title" v-if="section.title">{{ section.title }}</view>
					<view class="subtitle" v-if="section.subtitle">{{ section.subtitle }}</view>
					
					<view v-if="section.type === 'origin'" class="origin-grid">
						<view v-for="(point, pIndex) in section.items" :key="pIndex" class="origin-point">
							<view class="point-title">{{ point.title }}</view>
							<view class="point-text">{{ point.text }}</view>
						</view>
					</view>

					<view v-if="section.type === 'mission'" class="mission-grid">
						<view v-for="(item, mIndex) in section.items" :key="mIndex" class="mission-item">
							<view class="item-title">{{ item.title }}</view>
							<view class="item-text">{{ item.text }}</view>
						</view>
					</view>

					<view v-if="section.type === 'timeline'" class="timeline">
						<view v-for="(item, tIndex) in section.items" :key="tIndex" class="timeline-item">
							<view class="timeline-dot"></view>
							<view class="timeline-content">
								<view class="item-title">{{ item.title }}</view>
								<view class="item-text">{{ item.text }}</view>
							</view>
						</view>
					</view>
				</view>
			</view>
		</view>

		<!-- Pagination Dots -->
		<view class="pagination">
			<view
				v-for="(section, index) in sections"
				:key="index"
				class="dot"
				:class="{ 'active': index === currentSectionIndex }"
				@click="goToSection(index)"
			></view>
		</view>

		<!-- Custom Tab Bar -->
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
					:src="activeTab === index ? item.activeIcon : item.icon"
				></image>
				<text>{{ item.text }}</text>
			</view>
		</view>
	</view>
</template>

<script setup>
import { ref } from 'vue';

const themeColor = ref('#E54D42'); // A brighter theme color for light mode

const sections = ref([
	{
		type: 'title-card',
		title: '金昇贸易进出口公司的辉煌发展史',
		subtitle: '探索一家领先跨境电商企业的崛起之路',
	},
	{
		type: 'section_header',
		title: '公司简介',
		subtitle: '了解公司的起源、愿景和使命',
	},
	{
		type: 'origin',
		title: '公司起源',
		subtitle: '探索公司的创立背景',
		items: [
			{ title: '成立时间与地点', text: '公司于2019年在中国广东成立，最初专注于本地电子产品贸易。' },
			{ title: '创立动机', text: '创始人受到全球化趋势的启发，创立了专注于鞋类的跨境电商平台。' },
			{ title: '早期挑战', text: '面对激烈的市场竞争和资源限制，公司不断寻求创新以脱颖而出。' },
			{ title: '初始团队', text: '创始团队由一群经验丰富的行业专家组成，具备多元化的背景。' },
			{ title: '初期合作伙伴', text: '公司与多家国际供应商建立合作关系，为后续发展奠定基础。' },
			{ title: '早期产品线', text: '专注于鞋类，通过精选优质产品打开市场。' },
			{ title: '市场定位', text: '定位为提供高品质、高性价比的鞋类，满足国内外市场需求。' },
			{ title: '公司文化', text: '在创业初期，公司注重团队合作，逐渐形成独特的企业文化。' },
		],
	},
	{
		type: 'mission',
		title: '使命与愿景',
		subtitle: '公司的核心使命和长期愿景',
		items: [
			{ title: '使命宣言', text: '通过创新的电商平台，让全球消费者轻松获取高品质商品。' },
			{ title: '长期愿景', text: '成为全球领先的跨境电商企业，推动全球贸易自由化。' },
			{ title: '价值观', text: '坚持诚信、创新、合作、共赢的核心价值观。' },
			{ title: '社会责任', text: '积极参与公益事业，推动可持续发展，回馈社会。' },
			{ title: '客户导向', text: '始终以客户需求为中心，提供卓越的用户体验。' },
			{ title: '创新驱动', text: '持续投入研发，推动技术创新，提升竞争力。' },
            { title: '全球视野', text: '拥有全球化的视野,积极参与国际市场竞争与合作。' },
		],
	},
	{
		type: 'origin',
		title: '初始市场策略',
		subtitle: '公司的市场进入和定位策略',
		items: [
			{ title: '市场调研', text: '深入分析全球市场趋势，确定目标市场。' },
			{ title: '产品定位', text: '以高性价比和优质客户服务为核心竞争力。' },
			{ title: '品牌建设', text: '打造独特品牌形象，提升市场认知度。' },
			{ title: '竞争分析', text: '研究竞争对手策略，制定差异化竞争方案。' },
			{ title: '客户反馈', text: '收集客户反馈，持续优化产品和服务。' },
			{ title: '市场细分', text: '根据客户需求进行市场细分，提供定制化解决方案。' },
			{ title: '渠道选择', text: '选择适合目标市场的销售渠道，提高市场渗透率。' },
			{ title: '营销策略', text: '制定综合营销策略，提升品牌知名度和市场占有率。' },
		],
	},
    
	{
		type: 'section_header',
		title: '市场扩展',
		subtitle: '探讨公司如何逐步扩大市场份额',
	},
    {
		type: 'origin',
		title: '海外市场开拓',
		subtitle: '公司进军海外市场的策略和成果',
		items: [
			{ title: '目标市场选择', text: '选择具有潜力的新兴市场作为切入点,逐步扩展至全球。' },
			{ title: '本地化策略', text: '针对不同市场进行产品和服务的本地化调整,提高适应性。' },
			{ title: '合作伙伴关系', text: '与国际品牌和当地企业建立合作,提升市场渗透率。' },
			{ title: '文化适应', text: '尊重和理解当地文化差异,调整营销策略以适应当地需求。' },
			{ title: '市场反馈', text: '通过市场反馈不断优化产品和服务,提高客户满意度。' },
			{ title: '品牌知名度', text: '通过广告和公关活动提升品牌在目标市场的知名度。' },
			{ title: '法律合规', text: '确保在目标市场的运营符合当地法律法规,规避风险。' },
			
		],
	},
    {
		type: 'mission',
		title: '产品线扩展',
		subtitle: '公司产品线的多元化发展',
		items: [
			{ title: '新品引入', text: '持续引入各类新品,满足市场多元化需求。' },
			{ title: '自有品牌', text: '发展自有品牌,提升市场竞争力和品牌影响力。' },
			{ title: '供应链管理', text: '优化供应链管理,确保产品质量和交付效率。' },
			{ title: '市场调研', text: '定期进行市场调研,以把握消费者需求变化。' },
			{ title: '产品创新', text: '不断进行产品创新,引领市场潮流。' },
			{ title: '环保产品', text: '推出环保产品,响应全球绿色消费趋势。' },
            { title: '客户定制', text: '提供客户定制化服务,满足个性化需求。' },
            { title: '产品生命周期管理', text: '实施有效的产品生命周期管理,提高产品利润率。' },
		],
	},

	{
		type: 'section_header',
		title: '未来展望',
		subtitle: '展望公司的未来发展方向和战略',
	},
    {
		type: 'timeline',
		title: '全球化布局',
		subtitle: '公司全球化战略的深化与拓展',
		items: [
			{ title: '新兴市场进入', text: '积极开拓东南亚、南美等新兴市场，寻找新的增长机会。' },
			{ title: '本地化服务', text: '提供本地化的产品和服务，满足当地消费者的特定需求。' },
			{ title: '合作伙伴网络', text: '构建全球合作伙伴网络，加强资源共享和市场拓展。' },
            { title: '政策研究', text: '深入研究各国政策法规,确保合规运营并规避风险。' },
			{ title: '区域中心建设', text: '在关键市场建立区域中心，提升运营效率和市场响应速度。' },
            { title: '国际人才引进', text: '吸引全球优秀人才,增强公司的国际化视野和竞争力。' },
            { title: '文化融合', text: '推动不同文化间的融合,促进跨国团队的协作与创新。' },
		],
	},
	{
		type: 'mission',
		title: '可持续发展',
		subtitle: '公司的社会责任和可持续发展目标',
		items: [
			{ title: '环保措施', text: '推行绿色物流和包装，减少对环境的影响。' },
			{ title: '员工发展', text: '提供多元化培训和发展机会，提升员工技能。' },
			{ title: '供应链透明', text: '提高供应链透明度，确保供应商的社会责任。' },
			{ title: '循环经济', text: '推动循环经济模式，减少资源浪费和环境污染。' },
			{ title: '社会公益', text: '积极参与公益事业,推动社会发展和进步。' },
			{ title: '长期规划', text: '制定长期可持续发展规划,确保企业健康发展。' },
			{ title: '可再生能源', text: '使用可再生能源,推动低碳运营。' },
			{ title: '社区参与', text: '加强社区互动和参与,促进企业与社区的和谐发展。' },
		],
	},
	{
		type: 'final-card',
		title: '金昇贸易',
		subtitle: '与您共创未来',
	}
]);

const tabItems = ref([
	{ icon: 'https://pic1.imgdb.cn/item/153625/home.png', activeIcon: 'https://pic1.imgdb.cn/item/153625/home-active.png', text: '首页' },
	{ icon: 'https://pic1.imgdb.cn/item/153625/provider.png', activeIcon: 'https://pic1.imgdb.cn/item/153625/provider-active.png', text: '产品信息' },
	{ icon: 'https://pic1.imgdb.cn/item/153625/about.png', activeIcon: 'https://pic1.imgdb.cn/item/153625/about-active.png', text: '关于我们' }
]);

const activeTab = ref(2);

const handleTabClick = (index) => {
	const tabItem = tabItems.value[index];
	if (index === activeTab.value) return;
	
	if (tabItem.text === '产品信息') {
		uni.redirectTo({ url: '/pages/index/provider' });
	} else if (tabItem.text === '首页') {
		uni.redirectTo({ url: '/pages/index/index' });
	}
};

// --- Full Page Scroll Logic ---
const currentSectionIndex = ref(0);
const leavingSectionIndex = ref(-1); // Track leaving section for exit animations
const isAnimating = ref(false);
const touchStartY = ref(0);

const goToSection = (index) => {
	if (isAnimating.value || index === currentSectionIndex.value) return;
	if (index >= 0 && index < sections.value.length) {
		leavingSectionIndex.value = currentSectionIndex.value; // Set current section as the one that is leaving
		currentSectionIndex.value = index;
		isAnimating.value = true;
		setTimeout(() => {
			isAnimating.value = false;
			leavingSectionIndex.value = -1; // Reset leaving section after transition
		}, 1000); // Match this with CSS transition time
	}
};

const handleTouchStart = (e) => {
	if (isAnimating.value) return;
	touchStartY.value = e.touches[0].clientY;
};

const handleTouchEnd = (e) => {
	if (isAnimating.value) return;
	const touchEndY = e.changedTouches[0].clientY;
	const deltaY = touchEndY - touchStartY.value;

	if (Math.abs(deltaY) < 50) return;

	let newIndex = currentSectionIndex.value;
	if (deltaY < 0) {
		if (currentSectionIndex.value < sections.value.length - 1) newIndex++;
	} else {
		if (currentSectionIndex.value > 0) newIndex--;
	}
	goToSection(newIndex);
};

const handleWheel = (e) => {
	if (isAnimating.value) return;
	let newIndex = currentSectionIndex.value;
	if (e.deltaY > 0) {
		if (currentSectionIndex.value < sections.value.length - 1) newIndex++;
	} else {
		if (currentSectionIndex.value > 0) newIndex--;
	}
	goToSection(newIndex);
};
</script>

<style lang="scss" scoped>
	// Keyframes for animations
	@keyframes text-focus-in {
		0% { filter: blur(12px); opacity: 0; }
		100% { filter: blur(0px); opacity: 1; }
	}

	@keyframes slide-in-bottom {
		0% { transform: translateY(100px); opacity: 0; }
		100% { transform: translateY(0); opacity: 1; }
	}

	@keyframes scale-up-item {
		0% { transform: scale(0.5); opacity: 0; }
		100% { transform: scale(1); opacity: 1; }
	}
	
	@keyframes draw-line {
		from { transform: scaleY(0); }
		to { transform: scaleY(1); }
	}
	
	@keyframes fade-in-left {
		from { transform: translateX(-50px); opacity: 0; }
		to { transform: translateX(0); opacity: 1; }
	}

	// --- Keyframes for Exit Animations ---
	@keyframes text-blur-out {
		0% { filter: blur(0.01); opacity: 1; }
		100% { filter: blur(12px); opacity: 0; }
	}

	@keyframes slide-out-bottom {
		0% { transform: translateY(0); opacity: 1; }
		100% { transform: translateY(50px); opacity: 0; }
	}

	@keyframes scale-down-item {
		0% { transform: scale(1); opacity: 1; }
		100% { transform: scale(0.5); opacity: 0; }
	}

	@keyframes undraw-line {
		from { transform: scaleY(1); }
		to { transform: scaleY(0); }
	}
		
	@keyframes fade-out-right {
		from { transform: translateX(0); opacity: 1; }
		to { transform: translateX(50px); opacity: 0; }
	}

	.page-container {
		--theme-color: #E54D42;
		height: 100vh;
		overflow: hidden;
		background-color: #f8f8f8;
		color: #333;
	}
	
	.content-wrapper {
		height: 100%;
		transition: transform 0.8s cubic-bezier(0.77, 0, 0.175, 1);
	}

	.section {
		height: 100vh;
		width: 100vw;
		display: flex;
		justify-content: center;
		align-items: center;
		padding: 80rpx 50rpx;
		box-sizing: border-box;
		text-align: center;
	}
	
	.section-content {
		width: 100%;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 20rpx;
	}

	.title {
		font-size: 56rpx;
		font-weight: bold;
		color: var(--theme-color);
	}

	.subtitle {
		font-size: 32rpx;
		color: #888;
		margin-bottom: 40rpx;
	}
	
	// --- Content Specific Animations (triggered by .active for IN, .is-leaving for OUT) ---

	.title-card.active {
		.title {
			animation: text-focus-in 1s cubic-bezier(0.550, 0.085, 0.680, 0.530) both;
		}
		.subtitle {
			opacity: 0;
			animation: slide-in-bottom 0.8s cubic-bezier(0.250, 0.460, 0.450, 0.940) 0.5s both;
		}
	}
	
	.final-card.active {
		.title, .subtitle {
			opacity: 0;
			animation: slide-in-bottom 1s cubic-bezier(0.250, 0.460, 0.450, 0.940) both;
		}
	}
	
	// --- Exit Animation Styles ---
	.section.is-leaving {
		// These animations should be faster than the page transition
		&.title-card .title {
			animation: text-blur-out 0.6s cubic-bezier(0.550, 0.085, 0.680, 0.530) forwards;
		}
		&.title-card .subtitle {
			animation: slide-out-bottom 0.6s cubic-bezier(0.250, 0.460, 0.450, 0.940) forwards;
		}
		
		&.final-card .title,
		&.final-card .subtitle {
			animation: slide-out-bottom 0.6s cubic-bezier(0.250, 0.460, 0.450, 0.940) forwards;
		}

		.origin-point,
		.mission-item {
			animation: scale-down-item 0.4s cubic-bezier(0.600, -0.280, 0.735, 0.045) forwards;
		}

		.timeline {
			&::before {
				animation: undraw-line 0.5s cubic-bezier(0.25, 1, 0.5, 1) forwards;
			}
			.timeline-item {
				animation: fade-out-right 0.4s ease-out forwards;
			}
		}
	}

	.origin-point, .mission-item {
		opacity: 0; // Hide all items initially
	}
	
	.section.active {
		.origin-point, .mission-item {
			animation: scale-up-item 0.5s cubic-bezier(0.390, 0.575, 0.565, 1.000) forwards;
		}

		@for $i from 1 through 10 {
			.origin-point:nth-child(#{$i}),
			.mission-item:nth-child(#{$i}) {
				animation-delay: #{0.2 + $i * 0.1}s;
			}
		}
		
		.timeline {
			&::before {
				animation: draw-line 1s cubic-bezier(0.25, 1, 0.5, 1) forwards;
			}
			.timeline-item {
				opacity: 0;
				animation: fade-in-left 0.6s ease-out forwards;
				
				@for $i from 1 through 10 {
					&:nth-child(#{$i}) {
						animation-delay: #{0.5 + $i * 0.2}s;
					}
				}
			}
		}
	}

	.title-card .title { font-size: 64rpx; }
	.title-card .subtitle { font-size: 36rpx; }
	.final-card .title { font-size: 64rpx; }
	.section_header .title { font-size: 60rpx; color: #333; }
	.section_header .subtitle { color: #999; }

	.origin-grid, .mission-grid {
		display: grid;
		gap: 30rpx;
		width: 100%;
	}
	.origin-grid { grid-template-columns: 1fr 1fr; }
	.mission-grid { grid-template-columns: repeat(auto-fit, minmax(280rpx, 1fr)); }

	.origin-point {
		background-color: #fff;
		padding: 30rpx;
		border-radius: 16rpx;
		border: 1px solid #f0f0f0;
		transition: transform 0.3s ease, box-shadow 0.3s ease;
		&:hover {
			transform: translateY(-10rpx);
			box-shadow: 0 10px 20px rgba(0,0,0,0.1);
		}
	}
	
	.mission-item {
		background-color: rgba(229, 77, 66, 0.08);
		padding: 30rpx;
		border-radius: 16rpx;
		border: 1px solid rgba(229, 77, 66, 0.5);
	}

	.point-title, .mission-item .item-title {
		font-size: 30rpx;
		font-weight: bold;
		color: var(--theme-color);
		margin-bottom: 10rpx;
	}
	.point-text { color: #666; font-size: 24rpx; }
	.mission-item .item-text { color: #555; font-size: 24rpx; }
	
	.timeline {
		width: 100%;
		position: relative;
		padding-left: 40rpx;
		&::before {
			content: '';
			position: absolute; left: 0; top: 10rpx; bottom: 10rpx;
			width: 4rpx;
			background-color: var(--theme-color);
			transform-origin: top;
			transform: scaleY(0);
		}
	}
	
	.timeline-item { position: relative; margin-bottom: 40rpx; text-align: left; }
	.timeline-dot {
		position: absolute; left: -48rpx; top: 8rpx;
		width: 20rpx; height: 20rpx;
		border-radius: 50%;
		background-color: #f8f8f8;
		border: 4rpx solid var(--theme-color);
	}
	.timeline-content .item-title { font-size: 30rpx; font-weight: bold; color: #333; }
	.timeline-content .item-text { font-size: 24rpx; color: #666; }

	// --- Pagination ---
	.pagination {
		position: fixed;
		right: 30rpx;
		top: 50%;
		transform: translateY(-50%);
		display: flex;
		flex-direction: column;
		gap: 20rpx;
		z-index: 10;
	}
	.dot {
		width: 16rpx;
		height: 16rpx;
		background-color: #ccc;
		border-radius: 50%;
		transition: background-color 0.3s, transform 0.3s;
		cursor: pointer;
	}
	.dot.active {
		background-color: var(--theme-color);
		transform: scale(1.5);
	}

	// --- Tab Bar ---
	.tab-bar {
		position: fixed;
		bottom: 0; left: 0; right: 0;
		height: 120rpx;
		background: #fff;
		display: flex;
		justify-content: space-around;
		align-items: center;
		border-top: 1rpx solid #e0e0e0;
		padding-bottom: env(safe-area-inset-bottom);
		z-index: 10;
	}
	.tab-item {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		font-size: 24rpx;
		color: #666;
		&.active { color: var(--theme-color); }
	}
	.tab-icon-placeholder {
		width: 50rpx;
		height: 50rpx;
		margin-bottom: 8rpx;
	}
</style>
