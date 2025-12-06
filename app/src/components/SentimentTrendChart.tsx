import { Line } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ChartOptions
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)

const PointValueLabel = {
  id: 'point-value-label',
  afterDatasetsDraw(chart: any) {
    const { ctx } = chart
    ctx.save()
    const datasets = chart.data.datasets || []
    datasets.forEach((ds: any, di: number) => {
      const meta = chart.getDatasetMeta(di)
      const color = ds.borderColor || '#e2e8f0'
      meta.data.forEach((el: any, i: number) => {
        const val = ds.data[i]
        if (val == null) return
        const { x, y } = el.tooltipPosition()
        ctx.fillStyle = color
        ctx.font = '10px sans-serif'
        ctx.textAlign = 'center'
        const offsetY = di === 0 ? -8 : 12
        ctx.fillText(String(val), x, y + offsetY)
      })
    })
    ctx.restore()
  }
}

ChartJS.register(PointValueLabel)

/**
 * 涨跌停趋势图组件
 * 用途：以折线图展示时间维度上的涨停/跌停家数变化
 */
interface SentimentTrendChartProps {
  data: Array<{
    timestamp: string
    limit_up_count: number
    limit_down_count: number
  }>
  loading?: boolean
}

/**
 * 趋势图主组件
 */
export function SentimentTrendChart({ data, loading }: SentimentTrendChartProps) {
  if (loading) {
    return (
      <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
        <div className="h-64 bg-slate-700 rounded animate-pulse"></div>
      </div>
    )
  }

  /** 构造 Chart.js 数据 */
  const chartData = {
    labels: data.map(item => {
      const v = item.timestamp
      if (/^\d{2}:\d{2}:\d{2}$/.test(v)) return v.slice(0, 5)
      const d = new Date(v)
      if (!isNaN(d.getTime())) return d.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
      return String(v)
    }),
    datasets: [
      {
        label: '涨停家数',
        data: data.map(item => item.limit_up_count),
        borderColor: '#ef4444',
        backgroundColor: 'rgba(239, 68, 68, 0.1)',
        tension: 0.4,
        fill: false,
        pointRadius: 3,
        pointHoverRadius: 4
      },
      {
        label: '跌停家数',
        data: data.map(item => item.limit_down_count),
        borderColor: '#10b981',
        backgroundColor: 'rgba(16, 185, 129, 0.1)',
        tension: 0.4,
        fill: false,
        pointRadius: 3,
        pointHoverRadius: 4
      }
    ]
  }

  /** 图表配置项（深色主题适配） */
  const options: ChartOptions<'line'> = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top' as const,
        labels: {
          color: '#94a3b8',
          usePointStyle: true,
          padding: 20
        }
      },
      title: {
        display: true,
        text: '涨跌停统计趋势',
        color: '#e2e8f0',
        font: {
          size: 16,
          weight: 'bold'
        }
      },
      // 自定义插件已在全局注册，无需额外配置
    },
    scales: {
      x: {
        grid: {
          color: 'rgba(148, 163, 184, 0.1)'
        },
        ticks: {
          color: '#94a3b8'
        }
      },
      y: {
        grid: {
          color: 'rgba(148, 163, 184, 0.1)'
        },
        ticks: {
          color: '#94a3b8'
        }
      }
    }
  }

  return (
    <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
      <div className="h-64">
        <Line data={chartData} options={options} />
      </div>
    </div>
  )
}
