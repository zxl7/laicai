import { useMarketSentiment } from '../hooks/useSentimentData'
import { SentimentCard } from '../components/SentimentCard'
import { SentimentTrendChart } from '../components/SentimentTrendChart'

export function Home() {
  const { sentiment, loading, error } = useMarketSentiment()

  // 模拟历史数据用于图表显示
  const mockChartData = [
    { timestamp: '2024-01-01T09:30:00', limit_up_count: 35, limit_down_count: 18 },
    { timestamp: '2024-01-01T10:00:00', limit_up_count: 42, limit_down_count: 15 },
    { timestamp: '2024-01-01T10:30:00', limit_up_count: 38, limit_down_count: 22 },
    { timestamp: '2024-01-01T11:00:00', limit_up_count: 45, limit_down_count: 12 },
    { timestamp: '2024-01-01T11:30:00', limit_up_count: 52, limit_down_count: 8 },
    { timestamp: '2024-01-01T13:00:00', limit_up_count: 48, limit_down_count: 14 },
    { timestamp: '2024-01-01T13:30:00', limit_up_count: 41, limit_down_count: 19 },
    { timestamp: '2024-01-01T14:00:00', limit_up_count: 46, limit_down_count: 16 },
    { timestamp: '2024-01-01T14:30:00', limit_up_count: 39, limit_down_count: 21 },
    { timestamp: '2024-01-01T15:00:00', limit_up_count: 45, limit_down_count: 12 }
  ]

  if (error) {
    return (
      <div className="min-h-screen bg-slate-900 text-white p-6">
        <div className="max-w-7xl mx-auto">
          <div className="bg-red-900/20 border border-red-500/30 rounded-lg p-4 text-red-400">
            错误: {error}
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-slate-900 text-white p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">市场情绪监控面板</h1>
          <p className="text-slate-400">实时监控A股市场情绪状态和板块变化</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <div className="lg:col-span-1">
            <SentimentCard sentiment={sentiment} loading={loading} />
          </div>
          <div className="lg:col-span-2">
            <SentimentTrendChart data={mockChartData} loading={loading} />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
            <h3 className="text-lg font-semibold text-white mb-4">市场概览</h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-slate-400">情绪状态</span>
                <span className={`font-medium ${
                  sentiment?.trend_direction === 'up' ? 'text-green-500' :
                  sentiment?.trend_direction === 'down' ? 'text-red-500' : 'text-yellow-500'
                }`}>
                  {sentiment?.trend_direction === 'up' ? '递增' :
                   sentiment?.trend_direction === 'down' ? '递减' : '震荡'}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-slate-400">涨跌比</span>
                <span className="text-white">
                  {sentiment ? (sentiment.limit_up_count / Math.max(sentiment.limit_down_count, 1)).toFixed(2) : '-'}
                </span>
              </div>
            </div>
          </div>

          <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
            <h3 className="text-lg font-semibold text-white mb-4">风险提示</h3>
            <div className="space-y-2">
              {sentiment?.sentiment_score && sentiment.sentiment_score < 30 && (
                <div className="text-red-400 text-sm">⚠️ 市场情绪低迷，注意风险</div>
              )}
              {sentiment?.sentiment_score && sentiment.sentiment_score > 80 && (
                <div className="text-yellow-400 text-sm">⚠️ 市场情绪过热，谨慎追高</div>
              )}
              {sentiment?.limit_down_count && sentiment.limit_down_count > 50 && (
                <div className="text-red-400 text-sm">⚠️ 跌停家数较多，市场恐慌</div>
              )}
              {!sentiment?.sentiment_score || (sentiment.sentiment_score >= 30 && sentiment.sentiment_score <= 80 && sentiment.limit_down_count <= 50) && (
                <div className="text-green-400 text-sm">✅ 市场情绪正常</div>
              )}
            </div>
          </div>

          <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
            <h3 className="text-lg font-semibold text-white mb-4">操作指南</h3>
            <div className="space-y-2 text-sm text-slate-400">
              <div>• 点击导航栏查看板块情绪矩阵</div>
              <div>• 金色边框表示主升板块</div>
              <div>• 红色闪烁表示退潮板块</div>
              <div>• 数据每30秒自动更新</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}