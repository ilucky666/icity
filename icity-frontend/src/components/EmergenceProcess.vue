<template>
  <div class="emergence-container">
    <!-- Sidebar for Project Selection -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <h3>涌现过程</h3>
        <p>更新前后时空演变</p>
      </div>
      <div class="project-list">
        <div 
          v-for="unit in units" 
          :key="unit.id" 
          class="project-item"
          :class="{ active: selectedUnitId === unit.id }"
          @click="selectUnit(unit)"
        >
          <span class="project-name">{{ unit.unitName }}</span>
          <el-tag size="small" effect="plain" round :type="getTagType(unit.category)" class="custom-tag">{{ unit.category }}</el-tag>
        </div>
      </div>
    </aside>

    <!-- Main Content Area -->
    <main class="content-area">
      <div v-if="loading" class="loading-overlay">
        <el-skeleton animated />
      </div>

      <!-- Map Container -->
      <div class="map-wrapper">
         <div ref="mapContainer" class="map-view"></div>
      </div>

      <!-- Bottom Control Panel -->
      <div class="control-panel">
        <div class="panel-header">
          <h4>{{ currentUnit?.unitName || '请选择项目' }}</h4>
          <span class="sub-header">POI 分布演变</span>
        </div>
        
        <div class="year-selector">
          <span class="year-label" :class="{ active: !isAfterRenewal }">2014</span>
          <el-switch
            v-model="isAfterRenewal"
            style="--el-switch-on-color: #10b981; --el-switch-off-color: #f59e0b"
            size="default"
            @change="handleYearChange"
          />
          <span class="year-label" :class="{ active: isAfterRenewal }">2022</span>
        </div>

        <div class="stats-info" v-if="poiData.length > 0">
          <div class="stat-box">
            <span class="stat-value">{{ poiData.length }}</span>
            <span class="stat-label">舒适物总量</span>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-box">
            <span class="stat-value">{{ uniqueTypes }}</span>
            <span class="stat-label">类型丰富度</span>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick, computed, shallowRef } from 'vue';
import axios from 'axios';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

const props = defineProps({
  units: {
    type: Array,
    default: () => []
  }
});

const selectedUnitId = ref(null);
const currentUnit = ref(null);
const isAfterRenewal = ref(false); // false = 2014, true = 2022
const loading = ref(false);

// Use shallowRef for Leaflet instances to avoid Vue's deep reactivity performance cost
const map = shallowRef(null);
const mapContainer = ref(null);
const poiLayerGroup = shallowRef(null);
const unitLayerGroup = shallowRef(null);

const poiData = shallowRef([]); // Use shallowRef for large data to prevent freezing

const uniqueTypes = computed(() => {
  if (!poiData.value) return 0;
  const types = new Set(poiData.value.map(p => p.originalType));
  return types.size;
});

const getTagType = (category) => {
  switch (category) {
    case '强功能单元': return 'danger';
    case '补短板单元': return 'primary';
    case '显特色单元': return 'success';
    default: return 'info';
  }
};

const initMap = async () => {
  if (map.value) return;
  
  await nextTick();
  
  if (!mapContainer.value) {
    console.error("Map container not found");
    return;
  }
  
  map.value = L.map(mapContainer.value, {
    zoomControl: false,
    attributionControl: false,
    preferCanvas: true // Use Canvas renderer for better performance with many points
  }).setView([30.5928, 114.3055], 13);

  L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
    maxZoom: 20
  }).addTo(map.value);

  poiLayerGroup.value = L.layerGroup().addTo(map.value);
  unitLayerGroup.value = L.layerGroup().addTo(map.value);
  
  // Force map to recalculate size after a short delay
  setTimeout(() => {
    map.value.invalidateSize();
  }, 200);
};

onUnmounted(() => {
  if (map.value) {
    map.value.remove();
    map.value = null;
  }
});

const selectUnit = (unit) => {
  if (selectedUnitId.value === unit.id) return;
  selectedUnitId.value = unit.id;
  currentUnit.value = unit;
  
  // Render Unit Polygon
  renderUnitPolygon(unit);
  
  // Fetch POIs
  fetchPois();
};

const renderUnitPolygon = (unit) => {
  if (!map.value || !unitLayerGroup.value) return;
  
  unitLayerGroup.value.clearLayers();
  
  if (unit.geojson) {
    try {
      const geoJsonData = JSON.parse(unit.geojson);
      // Simplify geometry if needed (not here, but good to know)
      // Ensure unit layer group is cleared
      if (unitLayerGroup.value) {
          unitLayerGroup.value.clearLayers();
          
          const layer = L.geoJSON(geoJsonData, {
            style: {
              color: '#3b82f6',
              weight: 2,
              opacity: 0.8,
              fillOpacity: 0.05,
              fillColor: '#3b82f6',
              interactive: false
            }
          }).addTo(unitLayerGroup.value);
          
          // Use setTimeOut to allow map to be ready
          setTimeout(() => {
             if (map.value) {
                // If geometry is valid, fly to it
                try {
                  const bounds = layer.getBounds();
                  if (bounds.isValid()) {
                    map.value.flyToBounds(bounds, {
                      padding: [50, 50],
                      duration: 1.0
                    });
                  }
                } catch (err) {
                  console.warn("Cannot get bounds", err);
                }
             }
          }, 300);
      }
      
    } catch (e) {
      console.error("Invalid GeoJSON for unit:", unit.unitName, e);
    }
  }
};

const fetchPois = async () => {
  if (!selectedUnitId.value) return;
  
  loading.value = true;
  const year = isAfterRenewal.value ? 2022 : 2014;
  
  try {
    const res = await axios.get(`http://localhost:8080/api/poi/list`, {
      params: {
        unitId: selectedUnitId.value,
        year: year
      }
    });
    poiData.value = res.data;
    renderPois();
  } catch (error) {
    console.error("Failed to fetch POIs:", error);
    poiData.value = [];
  } finally {
    loading.value = false;
  }
};

const renderPois = () => {
  if (!map.value || !poiLayerGroup.value) return;
  
  poiLayerGroup.value.clearLayers();
  
  if (!poiData.value || poiData.value.length === 0) return;

  // Use simple loop for performance if < 1000, otherwise batch
  if (poiData.value.length < 1000) {
      poiData.value.forEach(poi => {
        if (poi.geom) {
          try {
            const geoJson = JSON.parse(poi.geom);
            const latlng = [geoJson.coordinates[1], geoJson.coordinates[0]];
            
            L.circleMarker(latlng, {
              radius: 3, 
              fillColor: isAfterRenewal.value ? '#10b981' : '#f59e0b',
              color: null, 
              weight: 0,
              fillOpacity: 0.8,
              interactive: false
            }).addTo(poiLayerGroup.value);
          } catch (e) { /* ignore */ }
        }
      });
      return;
  }

  const markers = [];
  
  poiData.value.forEach(poi => {
    if (poi.geom) {
      try {
        const geoJson = JSON.parse(poi.geom);
        const latlng = [geoJson.coordinates[1], geoJson.coordinates[0]];
        
        const marker = L.circleMarker(latlng, {
          radius: 3, // Smaller radius
          fillColor: isAfterRenewal.value ? '#10b981' : '#f59e0b',
          color: null, // No border for performance
          weight: 0,
          fillOpacity: 0.8,
          interactive: false 
        });
        
        markers.push(marker);
      } catch (e) {
        // ignore
      }
    }
  });
  
  // Use batch adding with a larger chunk size since we disabled interactivity
  const batchSize = 1000;
  let index = 0;
  
  const addBatch = () => {
    // Check if component still mounted and layer exists
    if (!poiLayerGroup.value) return;

    const batch = markers.slice(index, index + batchSize);
    batch.forEach(m => m.addTo(poiLayerGroup.value));
    index += batchSize;
    
    if (index < markers.length) {
      requestAnimationFrame(addBatch);
    }
  };
  
  requestAnimationFrame(addBatch);
};

const handleYearChange = () => {
  fetchPois();
};

onMounted(() => {
  initMap();
  // If units are already loaded, select the first one
  if (props.units.length > 0) {
    selectUnit(props.units[0]);
  }
});

// Watch for units prop update (in case of async load)
watch(() => props.units, (newUnits) => {
  if (newUnits.length > 0 && !selectedUnitId.value) {
    selectUnit(newUnits[0]);
  }
});
</script>

<style scoped>
.emergence-container {
  display: flex;
  height: 100%;
  width: 100%;
  background-color: #f8fafc;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Microsoft YaHei', Arial, sans-serif;
}

.sidebar {
  width: 260px; /* 减小侧边栏宽度 */
  background: #fff;
  border-right: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  z-index: 10;
  box-shadow: 2px 0 10px rgba(0,0,0,0.02);
}

.sidebar-header {
  padding: 15px 20px;
  border-bottom: 1px solid #e2e8f0;
  background: #fff;
}

.sidebar-header h3 {
  margin: 0;
  font-size: 1rem; /* 减小字号 */
  color: #1e293b;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.sidebar-header p {
  margin: 4px 0 0;
  font-size: 0.75rem; /* 减小字号 */
  color: #94a3b8;
}

.project-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.project-item {
  padding: 10px 12px;
  margin-bottom: 4px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid transparent;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.project-item:hover {
  background-color: #f8fafc;
}

.project-item.active {
  background-color: #eff6ff;
  border-color: #dbeafe;
}

.project-name {
  font-size: 0.85rem; /* 减小字号 */
  font-weight: 500;
  color: #334155;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 140px;
}

.custom-tag {
  font-size: 10px;
  transform: scale(0.9);
}

.content-area {
  flex: 1;
  position: relative;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.map-wrapper {
  flex: 1;
  width: 100%;
  height: 100%;
  position: relative;
  z-index: 1;
}

.map-view {
  width: 100%;
  height: 100%;
  position: absolute; /* Ensure it fills wrapper */
  top: 0;
  left: 0;
}

/* Control Panel UI Optimization */
.control-panel {
  position: absolute;
  bottom: 25px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(12px);
  padding: 15px 30px;
  border-radius: 50px; /* 胶囊形状 */
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
  z-index: 1000;
  display: flex;
  flex-direction: row; /* 改为横向布局 */
  align-items: center;
  gap: 25px;
  min-width: auto;
  border: 1px solid rgba(255, 255, 255, 0.5);
}

.panel-header {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding-right: 20px;
  border-right: 1px solid #e2e8f0;
}

.panel-header h4 {
  margin: 0;
  color: #0f172a;
  font-size: 0.95rem; /* 减小字号 */
  font-weight: 600;
}

.sub-header {
  font-size: 0.7rem;
  color: #64748b;
  margin-top: 2px;
}

.year-selector {
  display: flex;
  align-items: center;
  gap: 10px;
}

.year-label {
  font-size: 0.8rem; /* 减小字号 */
  font-weight: 500;
  color: #cbd5e1;
  transition: color 0.3s;
}

.year-label.active {
  color: #0f172a;
  font-weight: 700;
}

.stats-info {
  display: flex;
  gap: 15px;
  padding-left: 20px;
  border-left: 1px solid #e2e8f0;
  align-items: center;
}

.stat-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 50px;
}

.stat-value {
  font-size: 1rem; /* 减小字号 */
  font-weight: 700;
  color: #3b82f6;
  line-height: 1.2;
}

.stat-label {
  font-size: 0.7rem; /* 减小字号 */
  color: #64748b;
  transform: scale(0.9);
}

.stat-divider {
  width: 1px;
  height: 20px;
  background: #f1f5f9;
}

.loading-overlay {
  /* ... keep existing ... */
}
</style>
