import { useMarketSentiment } from "../hooks/useSentimentData"
import { SentimentCard } from "../components/SentimentCard"
import { SentimentTrendChart } from "../components/SentimentTrendChart"
import { useLimitUpList } from "../hooks/useLimitUp"
import { useLimitDownList } from "../hooks/useLimitDown"
import { LimitUpTable } from "../components/LimitUpTable"
import { LimitDownTable } from "../components/LimitDownTable"
import { useMemo, useState } from "react"
import { DateSelector } from "../components/DateSelector"
import type { MarketSentiment } from "../types"
import { getStoredLicense, setStoredLicense } from "../api/utils"
import { UNIFIED_DATE } from "../api/limitup"

export function Home() {
  const { loading, error } = useMarketSentiment()
  const [selectedDate, setSelectedDate] = useState<string>(UNIFIED_DATE)
  const { data: limitUpList, loading: luLoading, error: luError, refresh } = useLimitUpList(selectedDate)
  const { data: limitDownList, loading: ldLoading, error: ldError, refresh: refreshDown } = useLimitDownList(selectedDate)
  const today = useMemo(() => UNIFIED_DATE, [])
  const [licenseInput, setLicenseInput] = useState<string>(getStoredLicense() || "")
  const displayLimitUp = limitUpList
  const displayLoading = luLoading

  // 基于涨跌停数据生成真实图表数据（按时间累积）
  const normalizeTime = (val: string): string => {
    if (!val && val !== "0") return "-"
    const v = String(val)
    const m = v.match(/(\d{1,2}):(\d{1,2}):(\d{1,2})/)
    if (m) {
      const [, h, mi, s] = m
      return `${h.padStart(2, "0")}:${mi.padStart(2, "0")}:${s.padStart(2, "0")}`
    }
    if (/^\d{6}$/.test(v)) {
      const h = v.slice(0, 2)
      const mi = v.slice(2, 4)
      const s = v.slice(4, 6)
      return `${h}:${mi}:${s}`
    }
    const d = new Date(v)
    if (!isNaN(d.getTime())) {
      const h = `${d.getHours()}`.padStart(2, "0")
      const mi = `${d.getMinutes()}`.padStart(2, "0")
      const s = `${d.getSeconds()}`.padStart(2, "0")
      return `${h}:${mi}:${s}`
    }
    return v
  }
  const toSec = (t: string): number => {
    const m = String(t).match(/(\d{2}):(\d{2}):(\d{2})/)
    if (!m) return -1
    return Number(m[1]) * 3600 + Number(m[2]) * 60 + Number(m[3])
  }
  const chartData = useMemo(() => {
    const basePoints = ["09:30:00", "10:00:00", "10:30:00", "11:00:00", "11:30:00", "13:00:00", "13:30:00", "14:00:00", "14:30:00", "15:00:00"]
    return basePoints.map((ts) => {
      const tsSec = toSec(ts)
      const upCount = displayLimitUp.filter((it) => toSec(normalizeTime(it.lbt)) <= tsSec).length
      const downCount = limitDownList.filter((it) => toSec(normalizeTime(it.lbt)) <= tsSec).length
      return { timestamp: ts, limit_up_count: upCount, limit_down_count: downCount }
    })
  }, [displayLimitUp, limitDownList])

  const aggSentiment = useMemo<MarketSentiment>(() => {
    const up = displayLimitUp.length
    const down = limitDownList.length
    const total = up + down
    const score = Math.round((up / Math.max(total, 1)) * 100)
    const trend_direction: MarketSentiment["trend_direction"] = up > down ? "up" : up < down ? "down" : "sideways"
    const now = new Date().toISOString()
    return {
      id: "derived",
      timestamp: now,
      sentiment_score: score,
      trend_direction,
      limit_up_count: up,
      limit_down_count: down,
      created_at: now,
    }
  }, [displayLimitUp, limitDownList])

  // 避免因情绪数据错误阻断页面，其它模块继续渲染

  return (
    <div className="min-h-screen bg-[var(--bg-base)] text-white p-8">
      <div className="max-w-8xl mx-auto">
        {error && <div className="mb-8 bg-red-900/20 border border-red-500/30 rounded-lg p-4 text-red-400">情绪数据加载异常：{error}</div>}

        <div className="mb-8 bg-[var(--bg-container-50)] backdrop-blur-sm rounded-xl p-4 border border-[var(--border)]">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div>
              <h2 className="text-white font-semibold">查询设置</h2>
              <p className="text-xs text-slate-400">统一日期查询涨停/跌停</p>
            </div>
            <div className="flex items-center gap-4">
              <DateSelector
                value={selectedDate}
                min="2019-11-28"
                max={today}
                onChange={setSelectedDate}
                className="px-4 py-3 bg-[var(--bg-container-60)] border border-[var(--border)] rounded-lg text-white text-sm"
              />
              <input
                type="text"
                placeholder="输入API Token"
                value={licenseInput}
                onChange={(e) => setLicenseInput(e.target.value)}
                className="w-64 px-4 py-3 bg-[var(--bg-container-60)] border border-[var(--border)] rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500"
              />
              <button
                onClick={() => {
                  if (licenseInput.trim()) {
                    setStoredLicense(licenseInput.trim())
                    refresh()
                    refreshDown()
                  }
                }}
                className="px-4 py-3 rounded-md text-sm font-medium bg-[var(--bg-container-60)] hover:bg-slate-600 text-slate-200">
                保存Token
              </button>
              <button
                onClick={() => {
                  refresh()
                  refreshDown()
                }}
                disabled={luLoading || ldLoading}
                className="px-4 py-3 rounded-md text-sm font-medium bg-amber-500 hover:bg-amber-600 disabled:bg-slate-600 text-white">
                查询
              </button>
            </div>
          </div>
          {!licenseInput && <div className="mt-4 text-xs text-red-400">未设置Token：请通过URL参数 ?license=... 或在此输入并点击保存</div>}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-4">
          <div className="lg:col-span-1">
            <SentimentCard sentiment={aggSentiment} loading={loading} />
          </div>
          <div className="lg:col-span-2">
            <SentimentTrendChart data={chartData} loading={loading} />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-4">
          <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-4 border border-slate-700">
            <h3 className="text-lg font-semibold text-white mb-2">市场概览</h3>
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-slate-400">情绪状态</span>
                <span className={`font-medium ${aggSentiment.trend_direction === "up" ? "text-red-500" : aggSentiment.trend_direction === "down" ? "text-green-500" : "text-yellow-500"}`}>
                  {aggSentiment.trend_direction === "up" ? "递增" : aggSentiment.trend_direction === "down" ? "递减" : "震荡"}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-slate-400">涨跌比</span>
                <span className="text-white">{(aggSentiment.limit_up_count / Math.max(aggSentiment.limit_down_count, 1)).toFixed(2)}</span>
              </div>
            </div>
          </div>

          <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-8 border border-slate-700">
            <h3 className="text-lg font-semibold text-white mb-2">风险提示</h3>
            <div className="space-y-4">
              {aggSentiment.sentiment_score < 30 && <div className="text-red-400 text-sm">⚠️ 市场情绪低迷，注意风险</div>}
              {aggSentiment.sentiment_score > 80 && <div className="text-yellow-400 text-sm">⚠️ 市场情绪过热，谨慎追高</div>}
              {aggSentiment.limit_down_count > 50 && <div className="text-red-400 text-sm">⚠️ 跌停家数较多，市场恐慌</div>}
              {aggSentiment.sentiment_score >= 30 && aggSentiment.sentiment_score <= 80 && aggSentiment.limit_down_count <= 50 && <div className="text-green-400 text-sm">✅ 市场情绪正常</div>}
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-4">
            {luError && <div className="bg-red-900/20 border border-red-500/30 rounded-lg p-4 text-red-400">涨停股池加载异常：{luError}</div>}
            <LimitUpTable data={displayLimitUp} loading={displayLoading} onRefresh={refresh} date={selectedDate} />
          </div>
          <div className="space-y-4">
            {ldError && <div className="bg-red-900/20 border border-red-500/30 rounded-lg p-4 text-red-400">跌停股池加载异常：{ldError}</div>}
            <LimitDownTable data={limitDownList} loading={ldLoading} onRefresh={refreshDown} date={selectedDate} />
          </div>
        </div>
      </div>
    </div>
  )
}
