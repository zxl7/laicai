import { useState, useEffect } from "react"
import { fetchLimitUpList, UNIFIED_DATE } from "../api/limitup"
import type { LimitUpItem } from "../api/types"
import { formatCurrency, formatPercent } from "../api/utils"
import { Card, Tag, Spin, Empty } from "antd"
import { Trophy } from "lucide-react"
import { resolveTagColor } from "../lib/tagColors"
import { getCompanyRecord } from "../services/companyStore"
import { DateSelector } from "../components/DateSelector"

/**
 * 连板天梯页面
 * 用途：展示按连板数分组的涨停股票，形成天梯效果
 */
export function BoardLadder() {
  // 日期状态管理
  const [selectedDate, setSelectedDate] = useState<string>(UNIFIED_DATE)

  // 根据选择的日期从本地存储加载数据
  const [stocks, setStocks] = useState<LimitUpItem[]>(() => {
    const savedData = localStorage.getItem(`boardLadderStocks_${UNIFIED_DATE}`)
    if (savedData) {
      try {
        return JSON.parse(savedData)
      } catch (error) {
        console.error("解析本地存储数据失败:", error)
      }
    }
    return []
  })
  const [loading, setLoading] = useState(stocks.length === 0)

  // 日期变化处理函数
  const handleDateChange = (date: string) => {
    if (date) {
      setSelectedDate(date)
    }
  }

  useEffect(() => {
    /**
     * 获取涨停股票数据
     */
    const fetchData = async () => {
      const dateString = selectedDate
      
      // 优先从本地存储加载数据
      const savedData = localStorage.getItem(`boardLadderStocks_${dateString}`)
      if (savedData) {
        try {
          setStocks(JSON.parse(savedData))
          setLoading(false) // 如果有本地数据，立即停止加载状态
        } catch (error) {
          console.error("解析本地存储数据失败:", error)
        }
      } else {
        setLoading(true) // 没有本地数据时才显示加载状态
      }

      // 在后台请求最新数据
      try {
        const data = await fetchLimitUpList(dateString)
        // 确保数据格式正确
        if (Array.isArray(data) && data.length > 0) {
          setStocks(data)
          // 按日期保存到本地存储
          localStorage.setItem(`boardLadderStocks_${dateString}`, JSON.stringify(data))
        } else {
          console.warn("涨停股数据为空:", data)
        }
      } catch (error) {
        console.error("获取涨停股数据失败:", error)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [selectedDate])

  /**
   * 从股票数据中解析连板天数和板数
   * 数据格式固定为tj: "X/Y"，其中X为天数，Y为板数
   * 优先从tj字段解析，失败则使用lbc字段（默认1天X板）
   */
  const getBoardInfo = (stock: LimitUpItem): { days: number; boards: number } => {
    try {
      // 首先检查tj字段，格式固定为 "X/Y"
      if (typeof stock.tj === "string" && stock.tj.trim()) {
        const parts = stock.tj.split("/")
        if (parts.length === 2) {
          const days = parseInt(parts[0], 10)
          const boards = parseInt(parts[1], 10)
          if (!isNaN(days) && !isNaN(boards)) {
            return { days, boards }
          }
        }
      }
      // 回退使用lbc字段，默认1天
      if (typeof stock.lbc === "number" && !isNaN(stock.lbc)) {
        return { days: 1, boards: stock.lbc }
      }
    } catch (error) {
      console.error("解析连板信息失败:", error, "股票数据:", stock)
    }
    // 默认返回0天0板
    return { days: 0, boards: 0 }
  }

  /**
   * 按连板数分组股票
   */
  const groupByBoardCount = () => {
    const groups: Record<number, LimitUpItem[]> = {}

    stocks.forEach((stock) => {
      const boardCount = getBoardInfo(stock).boards
      if (!groups[boardCount]) {
        groups[boardCount] = []
      }
      groups[boardCount].push(stock)
    })

    // 按连板数降序排序
    return Object.entries(groups)
      .sort(([a], [b]) => Number(b) - Number(a))
      .map(([boardCount, stocks]) => ({
        boardCount: Number(boardCount),
        stocks: stocks.sort((a, b) => {
          // 优先显示连续涨停（天数=板数）的数据
          const aIsContinuous = getBoardInfo(a).days === getBoardInfo(a).boards
          const bIsContinuous = getBoardInfo(b).days === getBoardInfo(b).boards
          
          if (aIsContinuous && !bIsContinuous) return -1
          if (!aIsContinuous && bIsContinuous) return 1
          
          // 同一连板数内按涨幅降序排序
          return (b.zf || 0) - (a.zf || 0)
        }),
      }))
  }

  const groupedStocks = groupByBoardCount()

  /**
   * 获取连板数对应的样式类名
   */
  const getBoardCountClassName = (count: number) => {
    if (count >= 5) return "bg-red-500/20 border-red-500 text-red-400"
    if (count >= 3) return "bg-amber-500/20 border-amber-500 text-amber-400"
    if (count >= 2) return "bg-green-500/20 border-green-500 text-green-400"
    return "bg-blue-500/20 border-blue-500 text-blue-400"
  }

  return (
    <div className="min-h-screen bg-slate-900 text-white p-8">
      <div className="max-w-[90rem] mx-auto">
        {/* 页面标题 */}
        <div className="mb-8">
          <div className="flex items-center space-x-3">
            <Trophy className="w-8 h-8 text-amber-400" />
            <h1 className="text-3xl font-bold text-white">连板天梯</h1>
          </div>
          <p className="text-slate-400 mt-2">按连板数展示涨停股票，连板数越高排名越靠前</p>
          <div className="flex flex-wrap items-center gap-x-4 gap-y-2 text-sm text-slate-500 mt-1">
            <div className="flex items-center space-x-2">
              <span>数据日期：</span>
              <DateSelector value={selectedDate} onChange={handleDateChange} className="w-[150px]" />
            </div>
            <span>每10分钟更新</span>
          </div>
        </div>

        {/* 连板天梯列表 */}
        <div className="space-y-4">
          {loading ? (
            <div className="flex justify-center items-center py-12">
              <div className="text-center">
                <Spin size="large" />
                <div className="mt-2 text-slate-400">加载中...</div>
              </div>
            </div>
          ) : groupedStocks.length === 0 ? (
            <Empty description="暂无连板股票数据" />
          ) : (
            groupedStocks.map((group) => (
              <div key={group.boardCount} className="flex gap-3 items-start mb-4">
                {/* 连板数标题 - 左侧固定宽度 */}
                <div className={`flex flex-col items-center justify-center px-3 py-2 rounded-lg border text-sm min-w-[80px] ${getBoardCountClassName(group.boardCount)}`}>
                  <div className="text-lg font-bold">{group.boardCount}板</div>
                  <div className="text-xs text-slate-400 mt-1">共 {group.stocks.length} 只</div>
                </div>

                {/* 股票列表 - 调整宽度布局 - 右侧占据剩余空间 */}
                <div className="flex-grow grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-3">
                  {group.stocks.map((stock) => {
                    // 获取股票概念标签
                    const rec = getCompanyRecord(stock.dm)
                    const tags = (rec?.idea || "")
                      .split(",")
                      .map((s) => s.trim())
                      .filter(Boolean)
                      .slice(0, 2)

                    return (
                      <Card key={stock.dm} className="bg-slate-800/50 border-slate-700 hover:border-amber-500/50 transition-all duration-300" bodyStyle={{ padding: 8 }}>
                        <div className="space-y-2">
                          {/* 股票基本信息 */}
                          <div className="flex items-start justify-between">
                            <div>
                              <div className="flex items-center space-x-1">
                                <h3 className="text-xs font-bold text-white truncate max-w-[120px]">{stock.mc}</h3>
                                <span className="text-slate-500 text-xs">{stock.dm}</span>
                              </div>
                              <div className="mt-0.5 flex items-center space-x-2">
                                <span className="text-red-400 font-medium text-xs">{formatPercent(stock.zf)}</span>
                                <span className="text-slate-300 text-xs">{stock.p?.toFixed(2)}元</span>
                              </div>
                            </div>
                            <Tag color={getBoardInfo(stock).boards >= 5 ? "red" : getBoardInfo(stock).boards >= 3 ? "orange" : "green"}>{getBoardInfo(stock).days}天{getBoardInfo(stock).boards}板</Tag>
                          </div>

                          {/* 股票概念标签 */}
                          {tags.length > 0 && (
                            <div className="flex flex-wrap gap-1">
                              {tags.map((tag) => (
                                <Tag key={tag} color={resolveTagColor(tag)} style={{ fontSize: "12px", padding: "0 4px" }}>
                                  {tag}
                                </Tag>
                              ))}
                            </div>
                          )}

                          {/* 股票详细信息 - 水平紧凑结构 */}
                          <div className="text-xs">
                            <div className="flex justify-between">
                              <div className="text-slate-400 flex items-center space-x-1">
                                <div className="text-slate-500">成交额:</div>
                                <div className="text-slate-200 truncate max-w-[120px]">{formatCurrency(stock.cje)}</div>
                              </div>
                              <div className="text-slate-400 flex items-center space-x-1">
                                <div className="text-slate-500">封板资金:</div>
                                <div className="text-slate-200 truncate max-w-[120px]">{formatCurrency(stock.zj)}</div>
                              </div>
                            </div>
                            <div className="flex justify-between">
                              <div className="text-slate-400 flex items-center space-x-1">
                                <div className="text-slate-500">流通市值:</div>
                                <div className="text-slate-200 truncate max-w-[120px]">{formatCurrency(stock.lt)}</div>
                              </div>
                              <div className="text-slate-400 flex items-center space-x-1">
                                <div className="text-slate-500">换手率:</div>
                                <div className="text-slate-200 max-w-[120px]">{formatPercent(stock.hs)}</div>
                              </div>
                            </div>
                          </div>

                          {/* 封板信息 */}
                          <div className="text-xs text-slate-500 flex items-center space-x-2 mt-1">
                            <div>首封: {stock.fbt ? stock.fbt.slice(0, 5) : "-"}</div>
                            <div>炸板: {stock.zbc || 0}次</div>
                          </div>
                        </div>
                      </Card>
                    )
                  })}
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  )
}
