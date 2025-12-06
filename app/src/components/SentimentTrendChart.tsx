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
    labels: data.map(item => new Date(item.timestamp).toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })),
    datasets: [
      {
        label: '涨停家数',
        data: data.map(item => item.limit_up_count),
        borderColor: '#10b981',
        backgroundColor: 'rgba(16, 185, 129, 0.1)',
        tension: 0.4,
        fill: false
      },
      {
        label: '跌停家数',
        data: data.map(item => item.limit_down_count),
        borderColor: '#ef4444',
        backgroundColor: 'rgba(239, 68, 68, 0.1)',
        tension: 0.4,
        fill: false
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
      }
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
