<template>
  <div class="app-container">
    <!-- 顶部导航栏 -->
    <header class="app-header" :class="{ 'header-light': currentView !== 'home' }">
      <div class="header-left" @click="switchView('home')" style="cursor: pointer">
        <h1 class="main-title">城市更新与创新涌现</h1>
      </div>
      <div class="header-nav">
        <div 
          class="nav-item" 
          :class="{ active: currentView === 'home' }"
          @click="switchView('home')"
        >
          首页
        </div>
        <div 
          class="nav-item" 
          :class="{ active: currentView === 'overview' }"
          @click="switchView('overview')"
        >
          区域概况
        </div>
        <div 
          class="nav-item" 
          :class="{ active: currentView === 'projects' }"
          @click="switchView('projects')"
        >
          更新项目
        </div>
        <div 
          class="nav-item" 
          :class="{ active: currentView === 'emergence' }"
          @click="switchView('emergence')"
        >
          涌现过程
        </div>
      </div>
    </header>

    <!-- 主内容区 -->
    <main class="main-content">
      <HomePage 
        v-if="currentView === 'home'"
        @start-explore="switchView('overview')"
      />

      <Map 
        v-show="currentView === 'overview'"
        :units="units"
        :is-visible="currentView === 'overview'"
        @unit-selected="handleUnitSelect" 
        :selected-unit-id="selectedUnitId"
      />
      
      <ProjectList 
        v-if="currentView === 'projects'"
        :units="units"
        :loading="loading"
        @select-unit="handleProjectSelect"
      />

      <EmergenceProcess
        v-if="currentView === 'emergence'"
        :units="units"
      />
    </main>

    <!-- 悬浮式详情卡片 -->
    <UnitDetail
      v-model="drawerVisible"
      :unit-id="selectedUnitId"
      @next-unit="handleNextUnit"
      @prev-unit="handlePrevUnit"
    />
  </div>
</template>

<script setup>
import { ref, provide, onMounted } from 'vue';
import axios from 'axios';
import Map from './components/Map.vue';
import UnitDetail from './components/UnitDetail.vue';
import ProjectList from './components/ProjectList.vue';
import HomePage from './components/HomePage.vue';
import EmergenceProcess from './components/EmergenceProcess.vue';

const drawerVisible = ref(false);
const selectedUnitId = ref(null);
const allUnitIds = ref([]); // Store all IDs for navigation
const currentView = ref('home'); // Default to home
const units = ref([]);
const loading = ref(false);

// Provide a method for Map to register unit IDs
const registerUnits = (ids) => {
  allUnitIds.value = ids;
};
provide('registerUnits', registerUnits);

// Fetch data once at root level
onMounted(async () => {
  loading.value = true;
  try {
    const res = await axios.get('http://localhost:8080/api/unit/list');
    units.value = res.data;
    // Pre-register units for navigation
    registerUnits(units.value.map(u => u.id));
  } catch (e) {
    console.error("Failed to load units:", e);
  } finally {
    loading.value = false;
  }
});

const switchView = (view) => {
  currentView.value = view;
  if (view === 'projects' || view === 'home' || view === 'emergence') {
    drawerVisible.value = false;
  }
};

const handleUnitSelect = (id) => {
  selectedUnitId.value = id;
  drawerVisible.value = true;
};

const handleProjectSelect = (id) => {
  selectedUnitId.value = id;
  currentView.value = 'overview';
  // Small delay to allow map to be visible before flying
  setTimeout(() => {
    drawerVisible.value = true;
  }, 100);
};

const handleNextUnit = () => {
  if (!selectedUnitId.value || allUnitIds.value.length === 0) return;
  const currentIndex = allUnitIds.value.indexOf(selectedUnitId.value);
  const nextIndex = (currentIndex + 1) % allUnitIds.value.length;
  selectedUnitId.value = allUnitIds.value[nextIndex];
};

const handlePrevUnit = () => {
  if (!selectedUnitId.value || allUnitIds.value.length === 0) return;
  const currentIndex = allUnitIds.value.indexOf(selectedUnitId.value);
  const prevIndex = (currentIndex - 1 + allUnitIds.value.length) % allUnitIds.value.length;
  selectedUnitId.value = allUnitIds.value[prevIndex];
};
</script>

<style>
/* 重置全局样式以消除所有边距和黑边 */
html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  font-family: 'Helvetica Neue', Helvetica, Arial, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
  overflow: hidden; /* 防止出现滚动条导致黑边 */
}

/* 根容器设置 */
#app {
  width: 100vw;
  height: 100vh;
  margin: 0;
  padding: 0;
  max-width: none;
}

.app-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
}

/* 顶部导航栏样式 */
.app-header {
  height: 60px;
  background-color: transparent; /* 改为透明 */
  position: absolute; /* 绝对定位使其浮在内容上方 */
  top: 0;
  left: 0;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 40px; /* 两端增加间距 */
  z-index: 1000;
  flex-shrink: 0;
  font-family: "SimSun", "Songti SC", serif; /* 改为宋体 */
  box-sizing: border-box; /* 确保 padding 不会撑大 width */
}

.header-left {
  display: flex;
  align-items: center;
}

.header-nav {
  display: flex;
  gap: 30px;
  height: 100%;
}

.main-title {
  margin: 0;
  font-size: 20px;
  font-weight: 700;
  color: #fff; /* 默认白色以适应首页深色背景 */
  letter-spacing: 1px;
  text-shadow: 0 2px 4px rgba(0,0,0,0.3); /* 增加文字阴影提高可读性 */
}

/* 针对非首页视图，需要适配浅色背景 */
.header-light .main-title {
  color: #1f2937;
  text-shadow: none;
}

.header-light {
  background-color: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  position: relative; /* 恢复相对定位 */
}

.nav-item {
  height: 100%;
  display: flex;
  align-items: center;
  font-size: 15px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.9); /* 默认浅色文字 */
  cursor: pointer;
  position: relative;
  transition: all 0.3s;
  padding: 0 10px;
}

.header-light .nav-item {
  color: #4b5563;
}

.nav-item:hover {
  color: #fff;
  text-shadow: 0 0 8px rgba(255,255,255,0.6);
}

.header-light .nav-item:hover {
  color: #2563eb;
  text-shadow: none;
}

.nav-item.active {
  color: #fff;
  font-weight: 700;
}

.header-light .nav-item.active {
  color: #2563eb;
}

.nav-item.active::after {
  content: '';
  position: absolute;
  bottom: 12px;
  left: 10px;
  right: 10px;
  height: 2px;
  background-color: #fff;
  border-radius: 2px;
}

.header-light .nav-item.active::after {
  background-color: #2563eb;
  bottom: 0;
  left: 0;
  right: 0;
}

/* 主内容区（地图）样式 */
.main-content {
  flex: 1;
  width: 100%;
  position: relative;
  overflow: hidden;
}
</style>
