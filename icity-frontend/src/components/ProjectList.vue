<template>
  <div class="project-list-container">
    <div class="project-header">
      <h2>城市更新项目概览</h2>
      <p class="subtitle">探索武汉市内的重点更新单元与创新空间</p>
    </div>

    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="3" animated />
    </div>

    <div v-else class="project-grid">
      <div 
        v-for="(unit, index) in units" 
        :key="unit.id" 
        class="project-card"
        :style="{ animationDelay: `${index * 0.1}s` }"
        @click="selectUnit(unit)"
      >
        <div class="card-image-wrapper">
          <el-image 
            :src="getImageUrl(unit.unitName)" 
            fit="cover" 
            class="card-image"
            lazy
          >
            <template #placeholder>
              <div class="image-placeholder">Loading...</div>
            </template>
          </el-image>
          <div class="card-overlay">
            <el-tag :type="getTagType(unit.category)" effect="dark" size="small" class="category-tag">
              {{ unit.category }}
            </el-tag>
          </div>
        </div>
        
        <div class="card-content">
          <h3 class="card-title">{{ unit.unitName }}</h3>
          
          <div class="card-stats">
            <div class="stat-item">
              <el-icon><DataLine /></el-icon>
              <span>{{ unit.mainIndustry }}</span>
            </div>
            <div class="stat-item">
              <el-icon><Money /></el-icon>
              <span>{{ unit.investmentEst }} 亿</span>
            </div>
          </div>
          
          <p class="card-desc">{{ truncateText(unit.description, 60) }}</p>
          
          <div class="card-footer">
            <el-button type="primary" plain size="small" round>查看详情</el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { DataLine, Money } from '@element-plus/icons-vue';
import { getImageUrl } from '../utils/image.js';

const props = defineProps({
  units: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['select-unit']);

const selectUnit = (unit) => {
  emit('select-unit', unit.id);
};

const getTagType = (category) => {
    switch (category) {
        case '强功能单元': return 'danger';
        case '补短板单元': return 'primary';
        case '显特色单元': return 'success';
        default: return 'info';
    }
};

const truncateText = (text, length) => {
  if (!text) return '';
  return text.length > length ? text.substring(0, length) + '...' : text;
};
</script>

<style scoped>
.project-list-container {
  width: 100%;
  height: calc(100vh - 60px);
  padding: 40px;
  background-color: #f8fafc;
  overflow-y: auto;
  box-sizing: border-box;
}

.project-header {
  text-align: center;
  margin-bottom: 40px;
  animation: fadeInDown 0.8s ease-out;
}

.project-header h2 {
  font-size: 32px;
  color: #1e293b;
  margin: 0 0 10px 0;
  font-weight: 800;
}

.subtitle {
  font-size: 16px;
  color: #64748b;
  margin: 0;
}

.project-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 30px;
  max-width: 1400px;
  margin: 0 auto;
}

.project-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  border: 1px solid #f1f5f9;
  animation: fadeInUp 0.6s ease-out backwards;
}

.project-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.card-image-wrapper {
  position: relative;
  height: 180px;
  overflow: hidden;
}

.card-image {
  width: 100%;
  height: 100%;
  transition: transform 0.5s ease;
}

.project-card:hover .card-image {
  transform: scale(1.05);
}

.card-overlay {
  position: absolute;
  top: 12px;
  right: 12px;
}

.card-content {
  padding: 20px;
}

.card-title {
  font-size: 18px;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 12px 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.card-stats {
  display: flex;
  gap: 16px;
  margin-bottom: 12px;
  font-size: 13px;
  color: #64748b;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.card-desc {
  font-size: 14px;
  color: #475569;
  line-height: 1.5;
  margin: 0 0 16px 0;
  height: 42px; /* Fixed height for 2 lines */
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.card-footer {
  display: flex;
  justify-content: flex-end;
}

.loading-container {
  max-width: 800px;
  margin: 40px auto;
  padding: 20px;
  background: white;
  border-radius: 12px;
}

.image-placeholder {
  width: 100%;
  height: 100%;
  background: #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #94a3b8;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
