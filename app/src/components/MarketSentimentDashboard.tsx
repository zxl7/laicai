import { MarketSentiment } from '../types'

/**
 * 市场情绪概览仪表板
 * 用途：以卡片形式汇总展示趋势方向、情绪强度、涨/跌停家数
 */
interface MarketSentimentDashboardProps {
  data: MarketSentiment | null
  loading: boolean
}

/**
 * 仪表板主组件
 */
export function MarketSentimentDashboard({ data, loading }: MarketSentimentDashboardProps) {
  if (loading || !data) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700 animate-pulse">
            <div className="h-8 bg-slate-700 rounded mb-4"></div>
            <div className="h-12 bg-slate-700 rounded mb-2"></div>
            <div className="h-4 bg-slate-700 rounded"></div>
          </div>
        ))}
      </div>
    )
  }

  /** 趋势文案颜色 */
  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case 'up':
        return 'text-red-500'
      case 'down':
        return 'text-green-500'
      case 'sideways':
        return 'text-slate-500'
      default:
        return 'text-slate-500'
    }
  }

  /** 趋势中文文案 */
  const getSentimentText = (sentiment: string) => {
    switch (sentiment) {
      case 'up':
        return '递增'
      case 'down':
        return '递减'
      case 'sideways':
        return '震荡'
      default:
        return '未知'
    }
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
        <div className="text-slate-400 text-sm mb-2">市场情绪</div>
        <div className={`text-2xl font-bold ${getSentimentColor(data.trend_direction)}`}>
          {getSentimentText(data.trend_direction)}
        </div>
        <div className="text-xs text-slate-500 mt-1">当前状态</div>
      </div>
      
      <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
        <div className="text-slate-400 text-sm mb-2">情绪强度</div>
        <div className="text-2xl font-bold text-amber-400">
          {data.sentiment_score}
        </div>
        <div className="text-xs text-slate-500 mt-1">满分100</div>
      </div>
      
      <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
        <div className="text-slate-400 text-sm mb-2">涨停家数</div>
        <div className="text-2xl font-bold text-red-500">
          {data.limit_up_count}
        </div>
        <div className="text-xs text-slate-500 mt-1">只个股</div>
      </div>
      
      <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
        <div className="text-slate-400 text-sm mb-2">跌停家数</div>
        <div className="text-2xl font-bold text-green-500">
          {data.limit_down_count}
        </div>
        <div className="text-xs text-slate-500 mt-1">只个股</div>
      </div>
    </div>
  )
}
