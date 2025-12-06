import { TrendingUp, TrendingDown, Minus } from 'lucide-react'
import { MarketSentiment } from '../types'

/**
 * 情绪指标卡片组件
 * 用途：展示市场情绪分数、趋势箭头以及涨跌停家数的核心信息
 */

/**
 * 组件入参
 * - sentiment: 市场情绪数据；为空时显示“暂无数据”
 * - loading: 加载占位骨架
 */
interface SentimentCardProps {
  sentiment: MarketSentiment | null
  loading?: boolean
}

/**
 * 情绪卡片主组件
 */
export function SentimentCard({ sentiment, loading }: SentimentCardProps) {
  if (loading) {
    return (
      <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700 animate-pulse">
        <div className="h-8 bg-slate-700 rounded mb-4"></div>
        <div className="h-12 bg-slate-700 rounded mb-4"></div>
        <div className="h-6 bg-slate-700 rounded"></div>
      </div>
    )
  }

  if (!sentiment) {
    return (
      <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
        <div className="text-slate-400 text-center">暂无数据</div>
      </div>
    )
  }

  /** 返回趋势图标（递增/递减/震荡） */
  const getTrendIcon = () => {
    switch (sentiment.trend_direction) {
      case 'up':
        return <TrendingUp className="w-6 h-6 text-red-500" />
      case 'down':
        return <TrendingDown className="w-6 h-6 text-green-500" />
      default:
        return <Minus className="w-6 h-6 text-slate-500" />
    }
  }

  /** 根据分数返回数值颜色 */
  const getScoreColor = () => {
    if (sentiment.sentiment_score >= 70) return 'text-red-500'
    if (sentiment.sentiment_score >= 40) return 'text-yellow-500'
    return 'text-green-500'
  }

  /** 根据分数返回卡片渐变背景 */
  const getBackgroundGradient = () => {
    if (sentiment.sentiment_score >= 70) return 'from-red-900/20 to-red-800/10'
    if (sentiment.sentiment_score >= 40) return 'from-yellow-900/20 to-yellow-800/10'
    return 'from-green-900/20 to-green-800/10'
  }

  return (
    <div className={`bg-gradient-to-br ${getBackgroundGradient()} backdrop-blur-sm rounded-xl p-6 border border-slate-700 shadow-lg`}>
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-slate-300 text-sm font-medium">市场情绪指数</h3>
        {getTrendIcon()}
      </div>
      
      <div className="mb-4">
        <div className={`text-4xl font-bold ${getScoreColor()}`}>
          {sentiment.sentiment_score}
        </div>
        <div className="text-slate-400 text-sm mt-1">/ 100</div>
      </div>

      <div className="grid grid-cols-2 gap-4 text-sm">
        <div className="bg-slate-800/30 rounded-lg p-3">
          <div className="text-red-500 font-semibold">{sentiment.limit_up_count}</div>
          <div className="text-slate-400 text-xs">涨停家数</div>
        </div>
        <div className="bg-slate-800/30 rounded-lg p-3">
          <div className="text-green-500 font-semibold">{sentiment.limit_down_count}</div>
          <div className="text-slate-400 text-xs">跌停家数</div>
        </div>
      </div>

      <div className="mt-4 text-xs text-slate-500">
        更新时间: {new Date(sentiment.timestamp).toLocaleString('zh-CN')}
      </div>
    </div>
  )
}
