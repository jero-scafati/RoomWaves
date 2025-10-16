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
  
  // Prepare data for progressive animation
  const fullData = props.chartData.labels.map((freq, idx) => [freq, props.chartData.datasets[0].data[idx]])
  
  const option = {
    backgroundColor: 'transparent',
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      top: '10%',
      containLabel: true
    },
    xAxis: {
      type: 'log',
      min: 20, // Start at 20Hz
      max: 20000, // End at 20kHz
      axisLine: {
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.3)'
        }
      },
      axisLabel: {
        color: 'rgba(255, 255, 255, 0.7)',
        formatter: (value) => {
          if (value >= 1000) {
            return (value / 1000) + 'k'
          }
          return value + ''
        }
      },
      splitLine: {
        show: true,
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.05)'
        }
      },
      minorSplitLine: {
        show: true,
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.02)'
        }
      },
      name: 'Frequency (Hz)',
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
        color: 'rgba(255, 255, 255, 0.7)',
        formatter: '{value} dB'
      },
      splitLine: {
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.1)'
        }
      },
      name: 'Magnitude (dB)',
      nameLocation: 'middle',
      nameGap: 50,
      nameTextStyle: {
        color: 'rgba(255, 255, 255, 0.9)'
      }
    },
    // Add zoom capabilities
    dataZoom: [
      {
        type: 'inside', // Mouse wheel and drag zoom
        xAxisIndex: 0,
        start: 0,
        end: 100,
        minValueSpan: 10, // Minimum zoom range
        filterMode: 'none'
      },
      {
        type: 'slider', // Bottom slider for zoom
        xAxisIndex: 0,
        start: 0,
        end: 100,
        height: 20,
        bottom: 5,
        handleIcon: 'path://M512,512m-16,0a16,16,0,1,0,32,0a16,16,0,1,0,-32,0',
        handleSize: '80%',
        handleStyle: {
          color: '#5a1de0',
          borderColor: '#5a1de0'
        },
        textStyle: {
          color: 'rgba(255, 255, 255, 0.7)'
        },
        borderColor: 'rgba(255, 255, 255, 0.1)',
        fillerColor: 'rgba(90, 29, 224, 0.2)',
        backgroundColor: 'rgba(255, 255, 255, 0.05)',
        dataBackground: {
          lineStyle: {
            color: 'rgba(90, 29, 224, 0.3)'
          },
          areaStyle: {
            color: 'rgba(90, 29, 224, 0.1)'
          }
        }
      }
    ],
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(50, 50, 50, 0.9)',
      borderColor: '#777',
      textStyle: {
        color: '#fff'
      },
      formatter: (params) => {
        const data = params[0]
        return `Freq: ${parseFloat(data.value[0]).toFixed(1)} Hz<br/>Mag: ${data.value[1].toFixed(2)} dB`
      },
      axisPointer: {
        type: 'cross',
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.3)'
        }
      }
    },
    toolbox: {
      feature: {
        restore: {
          show: true,
          title: 'Reset Zoom',
          iconStyle: {
            borderColor: 'rgba(255, 255, 255, 0.7)'
          }
        },
        saveAsImage: {
          show: true,
          title: 'Save Image',
          iconStyle: {
            borderColor: 'rgba(255, 255, 255, 0.7)'
          }
        }
      },
      top: 10,
      right: 10
    },
    series: [{
      name: 'Frequency Response',
      type: 'line',
      data: fullData,
      lineStyle: {
        color: '#5a1de0',
        width: 2.5
      },
      smooth: 0.3,
      symbol: 'none',
      emphasis: {
        focus: 'series',
        lineStyle: {
          width: 3,
          shadowBlur: 10,
          shadowColor: 'rgba(90, 29, 224, 0.5)'
        }
      },
      animation: true,
      animationDuration: 2000,
      animationEasing: 'linear',
      progressive: 400,
      progressiveThreshold: 1000,
      animationDelay: function (idx) {
        return idx * 2;
      },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0,
          y: 0,
          x2: 0,
          y2: 1,
          colorStops: [
            {
              offset: 0,
              color: 'rgba(90, 29, 224, 0.2)'
            },
            {
              offset: 1,
              color: 'rgba(90, 29, 224, 0)'
            }
          ]
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