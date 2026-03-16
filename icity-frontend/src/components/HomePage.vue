<template>
  <div class="home-container">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-bg" :style="{ backgroundImage: `url(${heroBg})` }"></div>
      <div class="hero-overlay"></div>
      <div class="hero-content">
        <h1 class="main-title">
          <span class="text-gradient">城市更新</span>与<span class="text-gradient">创新涌现</span>
        </h1>
        <p class="sub-title">探索武汉城市空间重构与活力再造的数字化图景</p>
        <div class="hero-actions">
          <el-button type="primary" size="large" class="cta-btn" @click="$emit('start-explore')">
            开始探索 <el-icon class="el-icon--right"><ArrowRight /></el-icon>
          </el-button>
          <el-button size="large" class="secondary-btn" @click="scrollToFeatures">
            了解更多
          </el-button>
        </div>
      </div>
      
      <!-- Scroll Indicator -->
      <div class="scroll-indicator" @click="scrollToFeatures">
        <div class="mouse">
          <div class="wheel"></div>
        </div>
        <span class="scroll-text">向下滚动</span>
      </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="features-section">
      <div class="section-header scroll-reveal">
        <h2>核心功能</h2>
        <div class="divider"></div>
        <p>多维度解析城市更新过程中的空间与社会经济变革</p>
      </div>
      
      <div class="features-grid">
        <div 
          class="feature-card scroll-reveal" 
          v-for="(feature, index) in features" 
          :key="index"
          :style="{ transitionDelay: `${index * 100}ms` }"
        >
          <div class="icon-wrapper" :style="{ background: feature.bg }">
            <el-icon :size="32" :color="feature.color">
              <component :is="feature.icon" />
            </el-icon>
          </div>
          <h3>{{ feature.title }}</h3>
          <p>{{ feature.desc }}</p>
        </div>
      </div>
    </section>

    <!-- Stats Section -->
    <section class="stats-section">
      <div class="stats-grid">
        <div class="stat-item scroll-reveal" v-for="(stat, index) in stats" :key="index">
          <div class="stat-number">{{ stat.value }}</div>
          <div class="stat-label">{{ stat.label }}</div>
        </div>
      </div>
    </section>

    <!-- Team Section -->
    <section class="team-section">
      <div class="section-header scroll-reveal">
        <h2>团队介绍</h2>
        <div class="divider"></div>
        <p>汇聚多学科力量，共绘城市未来蓝图</p>
      </div>
      <div class="team-grid">
        <div class="team-card scroll-reveal" v-for="(member, index) in teamMembers" :key="index">
          <div class="avatar-wrapper">
            <img :src="member.avatar" :alt="member.name" class="avatar-img" />
          </div>
          <div class="member-info">
            <h3>{{ member.name }}</h3>
            <span class="member-role">{{ member.role }}</span>
            <p class="member-desc">{{ member.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="home-footer">
      <p>&copy; 2026 城市更新与创新涌现研究课题组. All Rights Reserved.</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { ArrowRight, MapLocation, DataAnalysis, TrendCharts, Reading, UserFilled } from '@element-plus/icons-vue';
import heroBg from '../assets/hero.png'; // Import local image

defineEmits(['start-explore']);

// 滚动监测逻辑
const observeScroll = () => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.scroll-reveal').forEach(el => observer.observe(el));
};

onMounted(() => {
  observeScroll();
});

const teamMembers = [
  { name: '张三', role: '项目负责人', desc: '全面统筹项目规划与实施', avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&w=200&q=80' },
  { name: '李四', role: '技术总监', desc: '负责GIS平台架构与开发', avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=200&q=80' },
  { name: '王五', role: '设计总监', desc: 'UI/UX设计与视觉呈现', avatar: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?auto=format&fit=crop&w=200&q=80' },
  { name: '赵六', role: '数据分析', desc: '城市数据挖掘与模型构建', avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=200&q=80' }
];

const features = [
  {
    icon: MapLocation,
    title: '空间可视化',
    desc: '基于 GIS 技术的城市更新单元高精度地图展示，直观呈现空间分布与边界。',
    color: '#3b82f6',
    bg: '#eff6ff'
  },
  {
    icon: DataAnalysis,
    title: '多维数据档案',
    desc: '整合产业、投资、规划愿景等多源数据，为每个更新单元建立详细的数字档案。',
    color: '#10b981',
    bg: '#ecfdf5'
  },
  {
    icon: TrendCharts,
    title: '创新涌现分析',
    desc: '追踪城市更新过程中的创新要素集聚与活力迸发，揭示空间演变的内在逻辑。',
    color: '#f59e0b',
    bg: '#fffbeb'
  },
  {
    icon: Reading,
    title: '政策与规划',
    desc: '深度解读相关政策文件与规划导则，为城市更新实践提供理论支撑与方向指引。',
    color: '#8b5cf6',
    bg: '#f5f3ff'
  }
];

const stats = [
  { value: '50+', label: '重点更新单元' },
  { value: '100B+', label: '预估总投资额' },
  { value: '10+', label: '行政区域覆盖' },
  { value: '2026', label: '数据持续更新' }
];

const scrollToFeatures = () => {
  document.getElementById('features').scrollIntoView({ behavior: 'smooth' });
};
</script>

<style scoped>
.home-container {
  width: 100%;
  height: 100vh; /* Fill full screen height */
  overflow-y: auto;
  background-color: #fff;
}

/* Hero Section */
.hero-section {
  position: relative;
  height: 100vh; /* Use full viewport height */
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  color: #fff;
}

.hero-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  /* background-image: url('https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?ixlib=rb-1.2.1&auto=format&fit=crop&w=1920&q=80'); */
  background-size: cover;
  background-position: center;
  animation: scaleBackground 20s infinite alternate;
  z-index: 0;
}

@keyframes scaleBackground {
  0% { transform: scale(1); }
  100% { transform: scale(1.1); }
}

.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to bottom, rgba(15, 23, 42, 0.6), rgba(15, 23, 42, 0.8));
  z-index: 1;
}

.hero-content {
  position: relative;
  z-index: 2;
  text-align: center;
  max-width: 800px;
  padding: 0 20px;
  animation: fadeInUp 1s ease-out;
}

.main-title {
  font-size: 3.5rem; /* 字体小一点 */
  font-weight: 800;
  margin-bottom: 1.5rem;
  line-height: 1.2;
  letter-spacing: -0.02em;
  font-family: "SimSun", "Songti SC", serif; /* 宋体 */
}

.text-gradient {
  background: linear-gradient(135deg, #60a5fa 0%, #c084fc 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.sub-title {
  font-size: 1.25rem; /* 字体小一点 */
  color: #cbd5e1;
  margin-bottom: 3rem;
  font-weight: 300;
  letter-spacing: 0.05em;
  font-family: "SimSun", "Songti SC", serif; /* 宋体 */
}

.hero-actions {
  display: flex;
  gap: 20px;
  justify-content: center;
}

.cta-btn {
  font-weight: 600;
  padding: 24px 48px;
  font-size: 1.1rem;
  border-radius: 50px;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  border: none;
  transition: transform 0.3s, box-shadow 0.3s;
}

.cta-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.5);
}

.secondary-btn {
  font-weight: 600;
  padding: 24px 48px;
  font-size: 1.1rem;
  border-radius: 50px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #fff;
  backdrop-filter: blur(10px);
}

.secondary-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  color: #fff;
}

/* Scroll Indicator */
.scroll-indicator {
  position: absolute;
  bottom: 40px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  opacity: 0.8;
  transition: opacity 0.3s;
  animation: bounce 2s infinite;
}

.scroll-indicator:hover {
  opacity: 1;
}

.mouse {
  width: 26px;
  height: 42px;
  border: 2px solid #fff;
  border-radius: 20px;
  position: relative;
}

.wheel {
  width: 4px;
  height: 8px;
  background: #fff;
  border-radius: 2px;
  position: absolute;
  top: 8px;
  left: 50%;
  transform: translateX(-50%);
  animation: scrollWheel 1.5s infinite;
}

.scroll-text {
  font-size: 12px;
  letter-spacing: 2px;
  text-transform: uppercase;
}

/* Features Section */
.features-section {
  padding: 100px 20px;
  background-color: #f8fafc;
}

.section-header {
  text-align: center;
  margin-bottom: 60px;
}

.section-header h2 {
  font-size: 2.2rem; /* 字体小一点 */
  color: #0f172a;
  margin-bottom: 20px;
  font-weight: 700;
  font-family: "SimSun", "Songti SC", serif; /* 二级标题宋体 */
}

.divider {
  width: 60px;
  height: 4px;
  background: #3b82f6;
  margin: 0 auto 20px;
  border-radius: 2px;
}

.section-header p {
  color: #64748b;
  font-size: 1rem; /* 字体小一点 */
  font-family: "SimSun", "Songti SC", serif; /* 宋体 */
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 30px;
  max-width: 1200px;
  margin: 0 auto;
}

.feature-card {
  background: #fff;
  padding: 40px 30px;
  border-radius: 20px;
  text-align: center;
  transition: all 0.5s ease;
  border: 1px solid #e2e8f0;
  opacity: 0;
  transform: translateY(30px);
}

.feature-card.visible {
  opacity: 1;
  transform: translateY(0);
}

.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.1);
  border-color: #3b82f6;
}

.icon-wrapper {
  width: 70px;
  height: 70px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 25px;
  transition: transform 0.3s;
}

.feature-card:hover .icon-wrapper {
  transform: rotate(10deg);
}

.feature-card h3 {
  font-size: 1.2rem; /* 字体小一点 */
  color: #1e293b;
  margin-bottom: 15px;
  font-weight: 600;
  font-family: "SimSun", "Songti SC", serif; /* 宋体 */
}

.feature-card p {
  color: #64748b;
  line-height: 1.6;
  font-size: 0.95rem; /* 字体小一点 */
}

/* Scroll Reveal Base Style */
.scroll-reveal {
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.8s cubic-bezier(0.5, 0, 0, 1);
}

.scroll-reveal.visible {
  opacity: 1;
  transform: translateY(0);
}

/* Stats Section */
.stats-section {
  padding: 80px 20px;
  background: #1e293b;
  color: #fff;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 40px;
  max-width: 1200px;
  margin: 0 auto;
  text-align: center;
}

.stat-item {
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.6s ease;
}

.stat-item.visible {
  opacity: 1;
  transform: translateY(0);
}

.stat-number {
  font-size: 2.5rem; /* 字体小一点 */
  font-weight: 800;
  margin-bottom: 10px;
  background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.stat-label {
  font-size: 1rem; /* 字体小一点 */
  color: #94a3b8;
  font-family: "SimSun", "Songti SC", serif; /* 宋体 */
}

/* Team Section */
.team-section {
  padding: 100px 20px;
  background-color: #fff;
}

.team-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 40px;
  max-width: 1200px;
  margin: 0 auto;
}

.team-card {
  text-align: center;
  transition: transform 0.3s;
}

.team-card:hover {
  transform: translateY(-5px);
}

.avatar-wrapper {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  overflow: hidden;
  margin: 0 auto 20px;
  border: 4px solid #f8fafc;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.member-info h3 {
  font-size: 1.2rem;
  color: #1e293b;
  margin: 0 0 5px;
  font-family: "SimSun", "Songti SC", serif;
}

.member-role {
  display: inline-block;
  padding: 4px 12px;
  background: #eff6ff;
  color: #3b82f6;
  border-radius: 20px;
  font-size: 0.8rem;
  margin-bottom: 10px;
  font-family: "SimSun", "Songti SC", serif;
}

.member-desc {
  color: #64748b;
  font-size: 0.9rem;
  line-height: 1.5;
}

/* Footer */
.home-footer {
  padding: 40px 20px;
  background: #0f172a;
  color: #475569;
  text-align: center;
  font-size: 0.9rem;
}

/* Animations */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% { transform: translate(-50%, 0); }
  40% { transform: translate(-50%, -10px); }
  60% { transform: translate(-50%, -5px); }
}

@keyframes scrollWheel {
  0% { transform: translate(-50%, 0); opacity: 1; }
  100% { transform: translate(-50%, 15px); opacity: 0; }
}

/* Responsive */
@media (max-width: 768px) {
  .main-title {
    font-size: 2.5rem;
  }
  
  .sub-title {
    font-size: 1.1rem;
  }
  
  .hero-actions {
    flex-direction: column;
  }
  
  .cta-btn, .secondary-btn {
    width: 100%;
  }
}
</style>
