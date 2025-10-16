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
  chartData: {
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
  if (!chartRef.value) return
  
  // Dispose existing instance if any
  if (chartInstance) {
    chartInstance.dispose()
  }
  
  chartInstance = echarts.init(chartRef.value)
  
  const option = {
    backgroundColor: 'transparent',
    grid: {
      left: '3%',
      right: '4%',
      bottom: '10%',
      top: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: props.chartData.labels,
      axisLine: {
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.3)'
        }
      },
      axisLabel: {
        color: 'rgba(255, 255, 255, 0.7)',
        formatter: (value) => parseFloat(value).toFixed(3) + 's'
      },
      name: 'Time (s)',
      nameLocation: 'middle',
      nameGap: 30,
      nameTextStyle: {
        color: 'rgba(255, 255, 255, 0.9)'
      }
    },
    yAxis: {
      type: 'value',
      axisLine: {
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.3)'
        }
      },
      axisLabel: {
        color: 'rgba(255, 255, 255, 0.7)'
      },
      splitLine: {
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.1)'
        }
      },
      name: 'Amplitude',
      nameLocation: 'middle',
      nameGap: 50,
      nameTextStyle: {
        color: 'rgba(255, 255, 255, 0.9)'
      }
    },
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(50, 50, 50, 0.9)',
      borderColor: '#777',
      textStyle: {
        color: '#fff'
      },
      formatter: (params) => {
        const data = params[0]
        return `Time: ${parseFloat(data.name).toFixed(4)}s<br/>Amplitude: ${data.value.toFixed(4)}`
      }
    },
    series: [{
      name: 'Waveform',
      type: 'line',
      data: props.chartData.datasets[0].data,
      lineStyle: {
        color: '#5a1de0',
        width: 2
      },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0,
          y: 0,
          x2: 0,
          y2: 1,
          colorStops: [{
            offset: 0,
            color: 'rgba(90, 29, 224, 0.3)'
          }, {
            offset: 1,
            color: 'rgba(90, 29, 224, 0.05)'
          }]
        }
      },
      symbol: 'none',
      sampling: 'lttb',
      smooth: false
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

watch(() => props.chartData, () => {
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
  height: 400px;
}
</style>