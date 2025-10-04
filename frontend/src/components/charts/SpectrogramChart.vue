<script setup>
// ============================================================================
// IMPORTS
// ============================================================================
import { ref, onMounted, watch, onUnmounted } from 'vue'
import * as echarts from 'echarts'

// ============================================================================
// PROPS
// ============================================================================
const props = defineProps({
  spectrogramData: {
    type: Object,
    required: true
  }
})

// ============================================================================
// STATE
// ============================================================================
const chartRef = ref(null)
let chartInstance = null
let resizeHandler = null

// ============================================================================
// CHART INITIALIZATION
// ============================================================================
const initChart = () => {
  if (!chartRef.value || !props.spectrogramData) return
  
  // Dispose existing instance if any
  if (chartInstance) {
    chartInstance.dispose()
  }
  
  chartInstance = echarts.init(chartRef.value)

  const { Sxx, f, t, min_db, max_db } = props.spectrogramData
  
  const data = [];
  for (let timeIdx = 0; timeIdx < t.length; timeIdx++) {
    for (let freqIdx = 0; freqIdx < f.length; freqIdx++) {
      // The axes are now index-based. The actual values are used for labels.
      data.push([freqIdx, timeIdx, Sxx[freqIdx][timeIdx]]);
    }
  }
  
  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      position: 'top',
      backgroundColor: 'rgba(50, 50, 50, 0.9)',
      borderColor: '#777',
      textStyle: {
        color: '#fff'
      },
      formatter: (params) => {
        const freqIdx = params.data[0];
        const timeIdx = params.data[1];
        const time = t[timeIdx];
        const freq = f[freqIdx];
        const value = params.data[2];
        return `Time: ${time.toFixed(3)}s<br/>Freq: ${freq.toFixed(1)} Hz<br/>Power: ${value.toFixed(1)} dB`;
      }
    },
    grid: {
      left: '10%',
      right: '8%',
      bottom: '15%',
      top: '5%',
      containLabel: true
    },
    xAxis: { // This is now the FREQUENCY axis
      type: 'category',
      // 2. USE THE FREQUENCY ARRAY FROM THE BACKEND FOR LABELS
      data: f.map(freq => freq.toFixed(0)), // Use the 'f' array
      axisLabel: {
        color: 'rgba(255, 255, 255, 0.7)',
        // 3. SIMPLIFY LABEL INTERVAL LOGIC
        // Show fewer labels to avoid clutter
        interval: Math.floor(f.length / 15), 
        formatter: (value) => {
          const freq = parseFloat(value);
          if (freq >= 1000) {
            return (freq / 1000).toFixed(freq < 10000 ? 1 : 0) + 'k';
          }
          return value;
        },
        rotate: 45
      },
      splitLine: {
        show: false
      },
      name: 'Frequency (Hz)',
      nameLocation: 'middle',
      nameGap: 45,
      nameTextStyle: {
        color: 'rgba(255, 255, 255, 0.9)'
      }
    },
    yAxis: { 
      type: 'category',
      data: t.map(v => v.toFixed(3)), 
      inverse: false,
      axisLabel: {
        color: 'rgba(255, 255, 255, 0.7)',
        interval: Math.floor(t.length / 10),
        formatter: (value) => value + 's'
      },
      splitLine: {
        show: false
      },
      name: 'Time (s)',
      nameLocation: 'middle',
      nameGap: 50,
      nameTextStyle: {
        color: 'rgba(255, 255, 255, 0.9)'
      }
    },
    visualMap: {
      // Use the min and max dB values from the backend
      min: min_db,
      max: max_db,
      calculable: true,
      orient: 'vertical',
      right: '0%',
      top: 'center',
      textStyle: {
        color: 'rgba(255, 255, 255, 0.7)'
      },
      formatter: (value) => (value * 100).toFixed(0) + '%',
      inRange: {
        color: [
          '#000428', // Deep blue-purple
          '#004e92', // Dark blue
          '#005f73', // Teal
          '#0a9396', // Cyan
          '#94d2bd', // Light cyan
          '#e9d8a6', // Light yellow
          '#ee9b00', // Orange
          '#ca6702', // Dark orange
          '#bb3e03', // Red-orange
          '#ae2012', // Dark red
          '#9b2226'  // Deep red
        ]
      }
    },
    series: [{
      name: 'Spectrogram',
      type: 'heatmap',
      data: data,
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowColor: 'rgba(255, 255, 255, 0.5)'
        }
      },
      progressive: 1000,
      animation: false,
      blur: {
        itemStyle: {
          opacity: 0.3,
          blur: 8
        }
      }
    }]
  }
  
  chartInstance.setOption(option)
  
  // Setup resize handler
  resizeHandler = () => {
    if (chartInstance) {
      chartInstance.resize()
    }
  }
  window.addEventListener('resize', resizeHandler)
}

// ============================================================================
// LIFECYCLE HOOKS
// ============================================================================
onMounted(() => {
  initChart()
})

watch(() => props.spectrogramData, () => {
  initChart()
}, { deep: true })

onUnmounted(() => {
  if (resizeHandler) {
    window.removeEventListener('resize', resizeHandler)
  }
  if (chartInstance) {
    chartInstance.dispose()
  }
})
</script>

<template>
  <div ref="chartRef" class="chart-wrapper"></div>
</template>

<style scoped>
.chart-wrapper {
  width: 100%;
  height: 500px;
}
</style>