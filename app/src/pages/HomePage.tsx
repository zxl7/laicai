import { MarketSentimentDashboard } from '../components/MarketSentimentDashboard'
import { useMarketSentiment } from '../hooks/useSentimentData'

export function HomePage() {
  const { sentiment, loading, error } = useMarketSentiment()

  if (error) {
    return (
      <div className="min-h-screen bg-slate-900 text-white p-4">
        <div className="max-w-7xl mx-auto">
          <div className="bg-red-900/20 border border-red-500/30 rounded-lg p-4 text-red-400">
            错误: {error}
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-slate-900 text-white p-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-4">
          <h1 className="text-3xl font-bold text-white mb-2">市场情绪监控面板</h1>
          <p className="text-slate-400">实时监控A股市场情绪状态和板块变化</p>
        </div>

        <MarketSentimentDashboard data={sentiment} loading={loading} />
      </div>
    </div>
  )
}