<template>
  <!-- 悬浮式详情卡片 -->
  <transition name="slide-fade">
    <div v-if="modelValue" class="floating-panel">
      <!-- 顶部控制栏 -->
      <div class="panel-header">
        <span class="panel-title">城市更新单元档案</span>
        <div class="panel-controls">
          <el-button-group size="small">
            <el-button :icon="ArrowLeft" @click="$emit('prev-unit')" title="上一个区域" />
            <el-button :icon="ArrowRight" @click="$emit('next-unit')" title="下一个区域" />
          </el-button-group>
          <el-button link class="close-btn" @click="$emit('update:modelValue', false)">
            <el-icon :size="20"><Close /></el-icon>
          </el-button>
        </div>
      </div>

      <div class="panel-content">
        <div v-if="loading" class="loading-state">
          <el-skeleton animated>
            <template #template>
              <el-skeleton-item variant="image" style="width: 100%; height: 180px" />
              <div style="padding: 14px;">
                <el-skeleton-item variant="h3" style="width: 50%" />
                <el-skeleton-item variant="text" style="width: 100%; margin-top: 16px;" />
                <el-skeleton-item variant="text" style="width: 80%; margin-top: 8px;" />
              </div>
            </template>
          </el-skeleton>
        </div>
        
        <div v-else-if="unit" class="unit-details">
          <!-- 动态图片展示区 -->
          <div class="hero-image">
            <el-image 
              :src="getImageUrl(unit.unitName)" 
              fit="cover"
              class="cover-img"
            >
              <template #error>
                <div class="image-placeholder">
                  <el-icon :size="40"><Picture /></el-icon>
                  <span>{{ unit.unitName }}</span>
                </div>
              </template>
            </el-image>
            <div class="hero-overlay">
              <el-tag :type="getTagType(unit.category)" effect="dark" round class="hero-tag">
                {{ unit.category }}
              </el-tag>
            </div>
          </div>

          <div class="content-body">
            <h2 class="unit-title">{{ unit.unitName }}</h2>
            
            <div class="stats-cards">
              <div class="stat-card">
                <div class="stat-icon">
                  <el-icon><DataLine /></el-icon>
                </div>
                <div class="stat-info">
                  <span class="stat-label">主导产业</span>
                  <span class="stat-value">{{ unit.mainIndustry }}</span>
                </div>
              </div>
              <div class="stat-card highlight">
                <div class="stat-icon">
                  <el-icon><Money /></el-icon>
                </div>
                <div class="stat-info">
                  <span class="stat-label">预估投资额</span>
                  <span class="stat-value">￥{{ unit.investmentEst }} 亿</span>
                </div>
              </div>
            </div>

            <el-divider border-style="dashed" />

            <div class="desc-section">
              <h4 class="section-title">
                <el-icon><LocationInformation /></el-icon> 规划愿景与定位
              </h4>
              <p class="desc-text">{{ unit.description }}</p>
            </div>

            <!-- 扩展信息：虚拟数据用于展示 -->
            <div class="desc-section mt-4">
              <h4 class="section-title">
                <el-icon><OfficeBuilding /></el-icon> 建设指标评估
              </h4>
              <el-progress :percentage="85" :stroke-width="10" color="#e74c3c" />
              <div class="progress-labels">
                <span>规划完成度</span>
                <span>优秀</span>
              </div>
              
              <el-row :gutter="10" class="mini-stats mt-3">
                <el-col :span="8">
                  <div class="mini-stat-item">
                    <div class="num">12+</div>
                    <div class="lbl">重点项目</div>
                  </div>
                </el-col>
                <el-col :span="8">
                  <div class="mini-stat-item">
                    <div class="num">500+</div>
                    <div class="lbl">预计就业</div>
                  </div>
                </el-col>
                <el-col :span="8">
                  <div class="mini-stat-item">
                    <div class="num">15m</div>
                    <div class="lbl">生活圈</div>
                  </div>
                </el-col>
              </el-row>
            </div>
          </div>
        </div>
        
        <div v-else class="empty-state">
          <el-empty description="请在地图上点击选择一个城市更新单元" />
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, watch } from 'vue';
import axios from 'axios';
import { 
  Picture, DataLine, Money, LocationInformation, OfficeBuilding,
  ArrowLeft, ArrowRight, Close 
} from '@element-plus/icons-vue';
import { getImageUrl } from '../utils/image.js';

const props = defineProps(['modelValue', 'unitId']); // Changed visible to modelValue for v-model
const emit = defineEmits(['update:modelValue', 'next-unit', 'prev-unit']); // Renamed visible to modelValue

const loading = ref(false);
const unit = ref(null);

const getTagType = (category) => {
    switch (category) {
        case '强功能单元': return 'danger';
        case '补短板单元': return 'primary';
        case '显特色单元': return 'success';
        default: return 'info';
    }
};

const fetchDetail = async (id) => {
  if (!id) return;
  loading.value = true;
  try {
    const res = await axios.get(`http://localhost:8080/api/unit/detail/${id}`);
    unit.value = res.data;
  } catch (error) {
    console.error("获取详情失败", error);
  } finally {
    loading.value = false;
  }
};

watch(() => props.unitId, (newId) => {
  if (newId) {
    fetchDetail(newId);
  }
});
</script>

<style scoped>
/* 悬浮面板样式 */
.floating-panel {
  position: fixed;
  top: 80px; /* 避开顶部导航栏 */
  right: 20px;
  width: 380px;
  max-height: calc(100vh - 100px);
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
  z-index: 2000;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border: 1px solid #f3f4f6;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #f3f4f6;
  background-color: #ffffff;
}

.panel-title {
  font-size: 16px;
  font-weight: 700;
  color: #1f2937;
}

.panel-controls {
  display: flex;
  align-items: center;
  gap: 12px;
}

.close-btn {
  color: #9ca3af;
  margin-left: 8px;
}

.close-btn:hover {
  color: #ef4444;
}

.panel-content {
  flex: 1;
  overflow-y: auto;
  /* 美化滚动条 */
  scrollbar-width: thin;
  scrollbar-color: #e5e7eb transparent;
}

.panel-content::-webkit-scrollbar {
  width: 6px;
}

.panel-content::-webkit-scrollbar-thumb {
  background-color: #e5e7eb;
  border-radius: 3px;
}

/* 动画效果 */
.slide-fade-enter-active {
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.slide-fade-leave-active {
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateX(20px);
  opacity: 0;
}

/* 复用之前的样式，略作调整 */
.loading-state {
  padding: 20px;
}

.empty-state {
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-image {
  position: relative;
  height: 180px;
  width: 100%;
}

.cover-img {
  width: 100%;
  height: 100%;
}

.image-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #e0e7ff 0%, #d1d5db 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #6b7280;
}

.hero-overlay {
  position: absolute;
  bottom: 12px;
  right: 12px;
  z-index: 10;
}

.content-body {
  padding: 20px;
}

.unit-title {
  margin: 0 0 16px 0;
  font-size: 20px;
  color: #111827;
  font-weight: 800;
  line-height: 1.3;
}

.stats-cards {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.stat-card {
  flex: 1;
  background-color: #f9fafb;
  border-radius: 10px;
  padding: 10px;
  display: flex;
  align-items: center;
  gap: 10px;
  border: 1px solid #f3f4f6;
}

.stat-card.highlight {
  background-color: #fff1f2;
  border-color: #ffe4e6;
}

.stat-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background-color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  color: #4b5563;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}

.highlight .stat-icon {
  color: #e11d48;
}

.stat-info {
  display: flex;
  flex-direction: column;
  min-width: 0; /* 防止文本溢出 */
}

.stat-label {
  font-size: 11px;
  color: #6b7280;
  margin-bottom: 2px;
}

.stat-value {
  font-size: 13px;
  font-weight: 700;
  color: #1f2937;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.highlight .stat-value {
  color: #be123c;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 15px;
  color: #374151;
  margin: 0 0 10px 0;
  font-weight: 600;
}

.desc-text {
  color: #4b5563;
  line-height: 1.6;
  font-size: 13px;
  background-color: #f8fafc;
  padding: 14px;
  border-radius: 8px;
  border-left: 3px solid #3b82f6;
  margin: 0;
}

.mt-4 {
  margin-top: 24px;
}

.mt-3 {
  margin-top: 12px;
}

.progress-labels {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #6b7280;
  margin-top: 6px;
}

.mini-stats {
  background-color: #f9fafb;
  border-radius: 8px;
  padding: 12px 0;
  border: 1px solid #f3f4f6;
}

.mini-stat-item {
  text-align: center;
}

.mini-stat-item .num {
  font-size: 16px;
  font-weight: 800;
  color: #111827;
}

.mini-stat-item .lbl {
  font-size: 11px;
  color: #6b7280;
  margin-top: 2px;
}
</style>
