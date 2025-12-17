import { useState, useEffect } from 'react'
import { fetchLimitUpList, UNIFIED_DATE } from '../api/limitup'
import type { LimitUpItem } from '../api/types'
import { formatCurrency, formatPercent } from '../api/utils'
import { Card, Tag, Spin, Empty } from 'antd'
import { Trophy } from 'lucide-react'
import { resolveTagColor } from '../lib/tagColors'
import { getCompanyRecord } from '../services/companyStore'

/**
 * 连板天梯页面
 * 用途：展示按连板数分组的涨停股票，形成天梯效果
 */
export function BoardLadder() {
  const [stocks, setStocks] = useState<LimitUpItem[]>(() => {
    // 从本地存储加载数据
    const savedData = localStorage.getItem('boardLadderStocks')
    if (savedData) {
      try {
        return JSON.parse(savedData)
      } catch (error) {
        console.error('解析本地存储数据失败:', error)
      }
    }
    return []
  })
  const [loading, setLoading] = useState(stocks.length === 0)
  const [date] = useState(UNIFIED_DATE)

  useEffect(() => {
    /**
     * 获取涨停股票数据
     */
    const fetchData = async () => {
      setLoading(true)
      try {
        const data = await fetchLimitUpList(date)
        // 确保数据格式正确
        if (Array.isArray(data) && data.length > 0) {
          setStocks(data)
          // 保存到本地存储
          localStorage.setItem('boardLadderStocks', JSON.stringify(data))
        } else {
          console.warn('涨停股数据为空:', data)
          // 如果API返回空数据，尝试使用本地存储的数据
          const savedData = localStorage.getItem('boardLadderStocks')
          if (savedData) {
            try {
              setStocks(JSON.parse(savedData))
            } catch (error) {
              console.error('解析本地存储数据失败:', error)
            }
          }
        }
      } catch (error) {
        console.error('获取涨停股数据失败:', error)
        // 错误情况下也尝试使用本地存储的数据
        const savedData = localStorage.getItem('boardLadderStocks')
        if (savedData) {
          try {
            setStocks(JSON.parse(savedData))
          } catch (error) {
            console.error('解析本地存储数据失败:', error)
          }
        }
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [date])

  /**
   * 从股票数据中解析连板数
   * 优先从tj字段解析（格式：X天/Y板），失败则使用lbc字段
   */
  const getBoardCount = (stock: LimitUpItem): number => {
    try {
      // 首先检查tj字段
      if (typeof stock.tj === 'string' && stock.tj.trim()) {
        // 解析tj字段：支持 "X天/Y板" 或直接 "X/Y"
        const tjMatch = stock.tj.match(/^(\d+)\/?(天)?\/(\d+)\/?(板)?$/)
        if (tjMatch && tjMatch[3]) {
          const boardCount = parseInt(tjMatch[3], 10)
          if (!isNaN(boardCount)) {
            return boardCount
          }
        }
        // 尝试直接按斜线分割
        const parts = stock.tj.split('/')
        if (parts.length >= 2) {
          const boardCount = parseInt(parts[1], 10)
          if (!isNaN(boardCount)) {
            return boardCount
          }
        }
      }
      // 回退使用lbc字段
      if (typeof stock.lbc === 'number' && !isNaN(stock.lbc)) {
        return stock.lbc
      }
    } catch (error) {
      console.error('解析连板数失败:', error, '股票数据:', stock)
    }
    // 默认返回0
    return 0
  }

  /**
   * 按连板数分组股票
   */
  const groupByBoardCount = () => {
    const groups: Record<number, LimitUpItem[]> = {}
    
    stocks.forEach(stock => {
      const boardCount = getBoardCount(stock)
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
          // 同一连板数内按涨幅降序排序
          return (b.zf || 0) - (a.zf || 0)
        })
      }))
  }

  const groupedStocks = groupByBoardCount()

  /**
   * 获取连板数对应的样式类名
   */
  const getBoardCountClassName = (count: number) => {
    if (count >= 5) return 'bg-red-500/20 border-red-500 text-red-400'
    if (count >= 3) return 'bg-amber-500/20 border-amber-500 text-amber-400'
    if (count >= 2) return 'bg-green-500/20 border-green-500 text-green-400'
    return 'bg-blue-500/20 border-blue-500 text-blue-400'
  }

  return (
    <div className="min-h-screen bg-slate-900 text-white p-8">
      <div className="max-w-7xl mx-auto">
        {/* 页面标题 */}
        <div className="mb-8">
          <div className="flex items-center space-x-3">
            <Trophy className="w-8 h-8 text-amber-400" />
            <h1 className="text-3xl font-bold text-white">连板天梯</h1>
          </div>
          <p className="text-slate-400 mt-2">按连板数展示涨停股票，连板数越高排名越靠前</p>
          <div className="text-sm text-slate-500 mt-1">
            数据日期：{date} | 每10分钟更新
          </div>
        </div>

        {/* 连板天梯列表 */}
        <div className="space-y-6">
          {loading ? (
            <div className="flex justify-center items-center py-20">
              <div className="text-center">
                <Spin size="large" />
                <div className="mt-4 text-slate-400">加载中...</div>
              </div>
            </div>
          ) : groupedStocks.length === 0 ? (
            <Empty description="暂无连板股票数据" />
          ) : (
            groupedStocks.map((group) => (
              <div key={group.boardCount} className="space-y-3">
                {/* 连板数标题 */}
                <div className={`flex items-center space-x-3 px-4 py-3 rounded-lg border ${getBoardCountClassName(group.boardCount)}`}>
                  <div className="text-2xl font-bold">{group.boardCount}板</div>
                  <div className="text-sm text-slate-400">
                    共 {group.stocks.length} 只股票
                  </div>
                </div>

                {/* 股票列表 */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {group.stocks.map((stock) => {
                    // 获取股票概念标签
                    const rec = getCompanyRecord(stock.dm)
                    const tags = (rec?.idea || "")
                      .split(",")
                      .map((s) => s.trim())
                      .filter(Boolean)
                      .slice(0, 3)

                    return (
                      <Card
                        key={stock.dm}
                        className="bg-slate-800/50 border-slate-700 hover:border-amber-500/50 transition-all duration-300"
                        bodyStyle={{ padding: 16 }}
                      >
                        <div className="space-y-3">
                          {/* 股票基本信息 */}
                          <div className="flex items-start justify-between">
                            <div>
                              <div className="flex items-center space-x-2">
                                <h3 className="text-xl font-bold text-white">{stock.mc}</h3>
                                <span className="text-slate-500 text-sm">{stock.dm}</span>
                              </div>
                              <div className="mt-1 flex items-center space-x-4">
                                <span className="text-red-400 font-medium">{formatPercent(stock.zf)}</span>
                                <span className="text-slate-300 text-sm">{stock.p?.toFixed(2)}元</span>
                              </div>
                            </div>
                            <Tag color={getBoardCount(stock) >= 5 ? 'red' : getBoardCount(stock) >= 3 ? 'orange' : 'green'}>
                              {getBoardCount(stock)}板
                            </Tag>
                          </div>

                          {/* 股票概念标签 */}
                          {tags.length > 0 && (
                            <div className="flex flex-wrap gap-2">
                              {tags.map((tag) => (
                                <Tag key={tag} color={resolveTagColor(tag)}>
                                  {tag}
                                </Tag>
                              ))}
                            </div>
                          )}

                          {/* 股票详细信息 */}
                          <div className="grid grid-cols-2 gap-2 text-sm">
                            <div className="text-slate-400">
                              <div className="text-slate-500">成交额</div>
                              <div className="text-slate-200">{formatCurrency(stock.cje)}</div>
                            </div>
                            <div className="text-slate-400">
                              <div className="text-slate-500">封板资金</div>
                              <div className="text-slate-200">{formatCurrency(stock.zj)}</div>
                            </div>
                            <div className="text-slate-400">
                              <div className="text-slate-500">流通市值</div>
                              <div className="text-slate-200">{formatCurrency(stock.lt)}</div>
                            </div>
                            <div className="text-slate-400">
                              <div className="text-slate-500">换手率</div>
                              <div className="text-slate-200">{formatPercent(stock.hs)}</div>
                            </div>
                          </div>

                          {/* 封板信息 */}
                          <div className="text-xs text-slate-500 flex items-center space-x-4">
                            <div>首封: {stock.fbt ? stock.fbt.slice(0, 5) : '-'}</div>
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
