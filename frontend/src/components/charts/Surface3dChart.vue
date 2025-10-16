<script setup>
import { ref, onMounted, watch, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import 'echarts-gl'

const props = defineProps({
  surfaceData: {
    type: Object,
    required: true
  },
  dataReduction: {
    type: Number,
    default: 1, // 1 = no reduction, 2 = every 2nd point, etc.
    validator: (value) => value >= 1 && value <= 10
  }
})

const chartRef = ref(null)
let chartInstance = null
let resizeHandler = null

const formatFrequency = (freq) => {
  if (freq >= 10000) {
    return (freq / 1000).toFixed(0) + 'k'
  } else if (freq >= 1000) {
    return (freq / 1000).toFixed(1).replace('.0', '') + 'k'
  } else if (freq >= 100) {
    return freq.toFixed(0)
  } else {
    return freq.toFixed(0)
  }
}

const formatTime = (time) => {
  if (time < 1) {
    return (time * 1000).toFixed(0) + 'ms'
  } else {
    return time.toFixed(2) + 's'
  }
}

const initChart = () => {
  if (!chartRef.value || !props.surfaceData?.Sxx?.length) return
  
  // Dispose existing chart
  if (chartInstance) {
    chartInstance.dispose()
  }
  
  chartInstance = echarts.init(chartRef.value)
  
  const { Sxx, f, t, min_db, max_db } = props.surfaceData
  
  // Data reduction for performance
  const step = props.dataReduction
  const data = []
  const reducedF = []
  const reducedT = []
  
  // Sample data at intervals for better performance
  for (let i = 0; i < f.length; i += step) {
    reducedF.push(f[i])
  }
  // Reverse time array so it points towards the viewer
  for (let j = t.length - 1; j >= 0; j -= step) {
    reducedT.push(t[j])
  }
  
  // Prepare reduced data
  for (let i = 0; i < reducedF.length; i++) {
    for (let j = 0; j < reducedT.length; j++) {
      const origI = i * step
      // Reverse the j index to match the reversed time array
      const origJ = (t.length - 1) - (j * step)
      if (Sxx[origI] && Sxx[origI][origJ] !== undefined) {
        data.push([i, j, Sxx[origI][origJ]])
      }
    }
  }
  
  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      formatter: (params) => {
        if (!params.data || params.data.length < 3) return ''
        
        const freqIdx = params.data[0]
        const timeIdx = params.data[1]
        const freq = reducedF[freqIdx]
        const time = reducedT[timeIdx]
        const value = params.data[2]
        
        return `Frequency: ${freq.toFixed(1)} Hz<br/>` +
               `Time: ${(time * 1000).toFixed(1)} ms<br/>` +
               `Power: ${value.toFixed(1)} dB`
      }
    },
    grid3D: {
      viewControl: {
        alpha: 20,
        beta: -30,
        distance: 250,
        autoRotate: false,
        rotateSensitivity: 1,
        zoomSensitivity: 1,
        panSensitivity: 1,
        // Disable damping for more responsive controls
        damping: 0.8,
        rotateSensitivity: 2
      },
      boxWidth: 200,
      boxHeight: 100,
      boxDepth: 80,
      light: {
        main: {
          intensity: 1.0,
          shadow: false
        },
        ambient: {
          intensity: 0.5
        }
      }
    },
    xAxis3D: {
      type: 'category',
      name: 'Frequency (Hz)',
      nameTextStyle: {
        fontSize: 12,
        color: 'rgba(255, 255, 255, 0.9)'
      },
      data: reducedF.map(formatFrequency),
      axisLabel: {
        interval: Math.floor(reducedF.length / 8),
        fontSize: 10,
        color: 'rgba(255, 255, 255, 0.8)'
      },
      axisLine: {
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.6)'
        }
      },
      splitLine: {
        show: false,
        interval: Math.floor(reducedF.length / 8),
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.2)',
          opacity: 0.3
        }
      }
    },
    yAxis3D: {
      type: 'category',
      name: 'Time',
      nameTextStyle: {
        fontSize: 12,
        color: 'rgba(255, 255, 255, 0.9)'
      },
      data: reducedT.map(formatTime),
      axisLabel: {
        interval: Math.floor(reducedT.length / 6),
        fontSize: 10,
        color: 'rgba(255, 255, 255, 0.8)'
      },
      axisLine: {
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.6)'
        }
      },
      splitLine: {
        show: false,
        interval: Math.floor(reducedT.length / 6),
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.2)',
          opacity: 0.3
        }
      }
    },
    zAxis3D: {
      type: 'value',
      name: 'Power (dB)',
      nameTextStyle: {
        fontSize: 12,
        color: 'rgba(255, 255, 255, 0.9)'
      },
      min: min_db,
      max: max_db,
      axisLabel: {
        formatter: '{value} dB',
        fontSize: 10,
        color: 'rgba(255, 255, 255, 0.8)'
      },
      axisLine: {
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.6)'
        }
      },
      splitLine: {
        show: true,
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.2)',
          opacity: 0.3
        }
      }
    },
    visualMap: {
      min: min_db,
      max: max_db,
      calculable: true,
      orient: 'vertical',
      right: '5%',
      top: 'center',
      dimension: 2, // Explicitly map to z-axis value
      inRange: {
        color: [
          '#00008F', // Deep Blue
          '#0000FF', // Blue
          '#00FFFF', // Cyan
          '#00FF00', // Green
          '#FFFF00', // Yellow
          '#FF7F00', // Orange
          '#FF0000', // Red
          '#800000'  // Dark Red
        ]
      },
      formatter: (value) => value.toFixed(0) + ' dB',
      textStyle: {
        fontSize: 10,
        color: 'rgba(255, 255, 255, 0.9)'
      }
    },
    series: [
      {
        type: 'scatter3D',
        data: data,
        symbolSize: 3,
        itemStyle: {
          opacity: 0.8
        },
        emphasis: {
          itemStyle: {
            borderWidth: 1,
            borderColor: '#fff'
          }
        }
      }
    ]
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

onMounted(() => {
  initChart()
})

watch(() => props.surfaceData, () => {
  initChart()
}, { deep: true })

watch(() => props.dataReduction, () => {
  initChart()
})

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
  <div class="surface-3d-container">
    <div ref="chartRef" class="chart-wrapper"></div>
    
    <!-- Optional controls -->
    <div class="chart-controls" v-if="$slots.controls">
      <slot name="controls"></slot>
    </div>
  </div>
</template>

<style scoped>
.surface-3d-container {
  width: 100%;
  position: relative;
}

.chart-wrapper {
  width: 100%;
  height: 600px;
  min-height: 400px;
}

.chart-controls {
  position: absolute;
  top: 10px;
  left: 10px;
  z-index: 10;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 4px;
  padding: 8px;
}
</style>