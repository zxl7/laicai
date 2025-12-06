import { useMarketSentiment } from "../hooks/useSentimentData"
import { SentimentCard } from "../components/SentimentCard"
import { SentimentTrendChart } from "../components/SentimentTrendChart"
import { useLimitUpList } from "../hooks/useLimitUp"
import { LimitUpTable } from "../components/LimitUpTable"
import { useMemo, useState } from "react"
import { getTodayDateStr, getStoredLicense, setStoredLicense } from "../services/limitUpApi"

export function Home() {
  const { sentiment, loading, error } = useMarketSentiment()
  const [selectedDate, setSelectedDate] = useState<string>(getTodayDateStr())
  const { data: limitUpList, loading: luLoading, error: luError, refresh, date } = useLimitUpList(selectedDate)
  const today = useMemo(() => getTodayDateStr(), [])
  const [licenseInput, setLicenseInput] = useState<string>(getStoredLicense() || "")

  // 模拟历史数据用于图表显示
  const mockChartData = [
    { timestamp: "2024-01-01T09:30:00", limit_up_count: 35, limit_down_count: 18 },
    { timestamp: "2024-01-01T10:00:00", limit_up_count: 42, limit_down_count: 15 },
    { timestamp: "2024-01-01T10:30:00", limit_up_count: 38, limit_down_count: 22 },
    { timestamp: "2024-01-01T11:00:00", limit_up_count: 45, limit_down_count: 12 },
    { timestamp: "2024-01-01T11:30:00", limit_up_count: 52, limit_down_count: 8 },
    { timestamp: "2024-01-01T13:00:00", limit_up_count: 48, limit_down_count: 14 },
    { timestamp: "2024-01-01T13:30:00", limit_up_count: 41, limit_down_count: 19 },
    { timestamp: "2024-01-01T14:00:00", limit_up_count: 46, limit_down_count: 16 },
    { timestamp: "2024-01-01T14:30:00", limit_up_count: 39, limit_down_count: 21 },
    { timestamp: "2024-01-01T15:00:00", limit_up_count: 45, limit_down_count: 12 },
  ]

  // 避免因情绪数据错误阻断页面，其它模块继续渲染

  return (
    <div className="min-h-screen bg-slate-900 text-white p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">市场情绪监控面板</h1>
          <p className="text-slate-400">实时监控A股市场情绪状态和板块变化</p>
        </div>

        {error && <div className="mb-6 bg-red-900/20 border border-red-500/30 rounded-lg p-4 text-red-400">情绪数据加载异常：{error}</div>}

        <div className="mb-6 bg-slate-800/50 backdrop-blur-sm rounded-xl p-4 border border-slate-700">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
            <div>
              <h2 className="text-white font-semibold">涨停股池查询</h2>
              <p className="text-xs text-slate-400">选择交易日查询涨停列表（2019-11-28 至 今）。</p>
            </div>
            <div className="flex items-center gap-3">
              <input
                type="date"
                value={selectedDate}
                max={today}
                min={"2019-11-28"}
                onChange={(e) => setSelectedDate(e.target.value)}
                className="px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500"
              />
              <input
                type="text"
                placeholder="输入API Token"
                value={licenseInput}
                onChange={(e) => setLicenseInput(e.target.value)}
                className="w-64 px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500"
              />
              <button
                onClick={() => {
                  if (licenseInput.trim()) {
                    setStoredLicense(licenseInput.trim())
                    refresh()
                  }
                }}
                className="px-3 py-2 rounded-md text-sm font-medium bg-slate-700 hover:bg-slate-600 text-slate-200">
                保存Token
              </button>
              <button onClick={() => setSelectedDate(today)} className="px-3 py-2 rounded-md text-sm font-medium bg-slate-700 hover:bg-slate-600 text-slate-200">
                今天
              </button>
              <button onClick={refresh} disabled={luLoading} className="px-3 py-2 rounded-md text-sm font-medium bg-amber-500 hover:bg-amber-600 disabled:bg-slate-600 text-white">
                查询
              </button>
            </div>
          </div>
          {!licenseInput && <div className="mt-3 text-xs text-red-400">未设置Token：请通过URL参数 ?license=... 或在此输入并点击保存</div>}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <div className="lg:col-span-1">
            <SentimentCard sentiment={sentiment} loading={loading} />
          </div>
          <div className="lg:col-span-2">
            <SentimentTrendChart data={mockChartData} loading={loading} />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
            <h3 className="text-lg font-semibold text-white mb-4">市场概览</h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-slate-400">情绪状态</span>
                <span className={`font-medium ${sentiment?.trend_direction === "up" ? "text-green-500" : sentiment?.trend_direction === "down" ? "text-red-500" : "text-yellow-500"}`}>
                  {sentiment?.trend_direction === "up" ? "递增" : sentiment?.trend_direction === "down" ? "递减" : "震荡"}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-slate-400">涨跌比</span>
                <span className="text-white">{sentiment ? (sentiment.limit_up_count / Math.max(sentiment.limit_down_count, 1)).toFixed(2) : "-"}</span>
              </div>
            </div>
          </div>

          <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
            <h3 className="text-lg font-semibold text-white mb-4">风险提示</h3>
            <div className="space-y-2">
              {sentiment?.sentiment_score && sentiment.sentiment_score < 30 && <div className="text-red-400 text-sm">⚠️ 市场情绪低迷，注意风险</div>}
              {sentiment?.sentiment_score && sentiment.sentiment_score > 80 && <div className="text-yellow-400 text-sm">⚠️ 市场情绪过热，谨慎追高</div>}
              {sentiment?.limit_down_count && sentiment.limit_down_count > 50 && <div className="text-red-400 text-sm">⚠️ 跌停家数较多，市场恐慌</div>}
              {!sentiment?.sentiment_score ||
                (sentiment.sentiment_score >= 30 && sentiment.sentiment_score <= 80 && sentiment.limit_down_count <= 50 && <div className="text-green-400 text-sm">✅ 市场情绪正常</div>)}
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

        <div className="space-y-4">
          {luError && <div className="bg-red-900/20 border border-red-500/30 rounded-lg p-4 text-red-400">涨停股池加载异常：{luError}</div>}
          <LimitUpTable data={limitUpList} loading={luLoading} onRefresh={refresh} date={date} />
        </div>
      </div>
    </div>
  )
}
