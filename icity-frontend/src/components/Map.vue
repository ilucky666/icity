<template>
  <div id="map-container" class="map-container"></div>
</template>

<script setup>
import { onMounted, ref, watch, inject } from 'vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

const props = defineProps({
    selectedUnitId: Number, // Add prop to listen for external selection changes
    isVisible: Boolean, // Add prop to know when the map is visible
    units: {
        type: Array,
        default: () => []
    }
});

const emit = defineEmits(['unit-selected']);
const map = ref(null);
const unitLayers = ref({}); // Store layers by ID for easy access
const registerUnits = inject('registerUnits'); // Inject the method to register IDs

// Fix default icon issue with Leaflet in Vue
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41]
});

L.Marker.prototype.options.icon = DefaultIcon;

// Define a palette of light/pastel colors
const lightColors = [
    '#FFB3BA', '#FFDFBA', '#FFFFBA', '#BAFFC9', '#BAE1FF', // Pastel Red, Orange, Yellow, Green, Blue
    '#E6B3FF', '#F0E68C', '#E6E6FA', '#D8BFD8', '#DDA0DD', // Pastel Purple, Khaki, Lavender, Thistle, Plum
    '#B0E0E6', '#AFEEEE', '#FFC3A0', '#FF677D', '#D4A5A5', // Powder Blue, Pale Turquoise, Deep Orange, Pink, Rosy Brown
    '#392F5A', '#9DD9D2', '#FFF8F0', '#F4D35E', '#EE964B'  // Misc Light/Soft Colors
];

// Helper function to get random color based on ID (deterministic)
const getColorByUnitId = (id) => {
    if (!id) return '#3388ff';
    return lightColors[id % lightColors.length];
};

// Helper to darken a hex color for text readability
const darkenColor = (color, percent) => {
    let num = parseInt(color.replace("#",""),16),
    amt = Math.round(2.55 * percent),
    R = (num >> 16) - amt,
    B = (num >> 8 & 0x00FF) - amt,
    G = (num & 0x0000FF) - amt;
    return "#" + (0x1000000 + (R<255?R<1?0:R:255)*0x10000 + (B<255?B<1?0:B:255)*0x100 + (G<255?G<1?0:G:255)).toString(16).slice(1);
};

const initLayers = (units) => {
    if (!map.value) return;
    
    // Clear existing layers if needed (optional, for now just add new ones)
    // Ideally we should clear old layers if units update. 
    // But since units are loaded once, it's fine.
    
    units.forEach(unit => {
        if (unit.geojson && !unitLayers.value[unit.id]) {
            const geoJsonData = JSON.parse(unit.geojson);
            const layer = L.geoJSON(geoJsonData, {
                style: {
                    color: getColorByUnitId(unit.id),
                    weight: 2,
                    opacity: 0.8,
                    fillOpacity: 0.5
                }
            }).addTo(map.value);

            // Store layer reference
            unitLayers.value[unit.id] = layer;

            layer.on('click', () => {
                emit('unit-selected', unit.id);
                // Fly to bounds on click
                map.value.flyToBounds(layer.getBounds(), {
                    padding: [50, 50],
                    duration: 1.5,
                    easeLinearity: 0.25
                });
            });
            
            // Add a permanent tooltip (label)
            layer.bindTooltip(unit.unitName, {
                permanent: true,
                direction: 'center',
                className: 'unit-label-tooltip'
            });
            
            // Apply custom color to the tooltip text element after it's added
            // Leaflet tooltips are a bit tricky with dynamic colors via options, 
            // so we inject a style string into the HTML content
            const baseColor = getColorByUnitId(unit.id);
            const textColor = darkenColor(baseColor, 40); // Darken by 40% for better contrast
            
            layer.setTooltipContent(`<span style="color: ${textColor}">${unit.unitName}</span>`);
        }
    });
};

onMounted(async () => {
  // Initialize map centered on Wuhan
  map.value = L.map('map-container').setView([30.5928, 114.3055], 11);

  // Add a base layer (using Positron base map)
  L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
    subdomains: 'abcd',
    maxZoom: 20
  }).addTo(map.value);

  // Update font size on zoom to keep labels relative to map features
  const updateLabelSize = () => {
      const zoom = map.value.getZoom();
      // Base calculation: At zoom 14, font size is 14px. 
      // Scales with 2^zoom to simulate "physical" size on map.
      const baseZoom = 14;
      const baseSize = 14; 
      const newSize = baseSize * Math.pow(2, zoom - baseZoom);
      
      // Update CSS variable
    map.value.getContainer().style.setProperty('--unit-label-size', `${Math.max(newSize, 10)}px`); // Minimum size 10px to keep readable
};

  map.value.on('zoom', updateLabelSize);
  updateLabelSize(); // Initial call

  // Initial load if units already exist
  if (props.units.length > 0) {
      initLayers(props.units);
  }
});

// Watch for units prop change
watch(() => props.units, (newUnits) => {
    initLayers(newUnits);
});

// Watch for external selection changes (e.g. via Next/Prev buttons)
watch(() => props.selectedUnitId, (newId) => {
    if (newId && unitLayers.value[newId] && map.value) {
        const layer = unitLayers.value[newId];
        map.value.flyToBounds(layer.getBounds(), {
            padding: [50, 50],
            duration: 1.5,
            easeLinearity: 0.25
        });
    }
});

// Watch for visibility changes to fix map size
watch(() => props.isVisible, (visible) => {
    if (visible && map.value) {
        // Wait a small tick for the v-show transition to complete or layout to settle
        setTimeout(() => {
            map.value.invalidateSize();
        }, 100);
    }
});
</script>

<style scoped>
.map-container {
  width: 100%;
  height: calc(100vh - 60px); /* Subtract header height */
  z-index: 1;
  background-color: #f8f9fa; /* Match tile background to avoid black flash */
  outline: none; /* Remove focus outline */
  -webkit-tap-highlight-color: transparent; /* Remove mobile tap highlight */
}
/* Deep selector to ensure Leaflet container also has no outline */
:deep(.leaflet-container) {
    background-color: #f8f9fa;
    outline: none;
    font-family: inherit; /* Ensure font consistency */
}

/* Remove focus outline from all interactive elements inside map */
:deep(.leaflet-interactive) {
    outline: none !important;
    box-shadow: none !important;
}

:deep(path), :deep(svg), :deep(g) {
    outline: none !important;
}

/* Specific fix for browser focus rings */
:deep(.leaflet-container *:focus) {
    outline: none !important;
}
:deep(.leaflet-container *:focus-visible) {
    outline: none !important;
}

/* Custom Tooltip Styling for Unit Labels */
:deep(.unit-label-tooltip) {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    font-size: var(--unit-label-size, 14px); /* Use dynamic size */
    font-weight: 700;
    text-shadow: 
        1px 1px 0 #fff,
        -1px -1px 0 #fff,  
        1px -1px 0 #fff,
        -1px 1px 0 #fff,
        1px 1px 2px rgba(255,255,255,0.8); /* White halo for readability */
    white-space: nowrap;
    text-align: center;
    font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
    letter-spacing: 0.5px;
    transition: font-size 0.1s linear; /* Smooth resizing */
    pointer-events: none; /* Prevent blocking clicks */
}
:deep(.unit-label-tooltip::before) {
    display: none; /* Hide the little triangle pointer if present */
}
</style>
