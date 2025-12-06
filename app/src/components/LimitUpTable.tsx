import type { LimitUpItem } from '../api/types'
import { formatCurrency, formatPercent } from '../api/utils'
import { useEffect, useState } from 'react'
import { fetchCompanyProfile } from '../api/company'
import { setCombined, hasCombined } from '../services/cache'
import type { CombinedStockData } from '../types/combined'
import { exportCompanyCache, initCompanyCache, upsertCompanyRecord, upsertDateEntry, getCompanyRecord } from '../services/companyStore'

/**
 * 涨停股池表格
 * 用途：展示指定日期的涨停股票明细，支持手动刷新与表头固定
 */
interface Props {
  data: LimitUpItem[]
  loading?: boolean
  onRefresh?: () => void
  date?: string
}

/**
 * 表格主组件
 */
export function LimitUpTable({ data, loading, onRefresh, date }: Props) {
  const [cachingCode, setCachingCode] = useState<string | null>(null)
  const [cachedCodes, setCachedCodes] = useState<Record<string, boolean>>({})

  useEffect(() => {
    initCompanyCache()
  }, [])

  // 将涨停池返回的所有数据写入缓存（按日期分散存储），即使没有公司详情
  useEffect(() => {
    if (!date || !Array.isArray(data)) return
    for (const item of data) {
      upsertCompanyRecord(item.dm, {})
      upsertDateEntry(item.dm, date, { list: item })
    }
  }, [data, date])

  const handleFetchDetail = async (item: LimitUpItem) => {
    try {
      setCachingCode(item.dm)
      const profiles = await fetchCompanyProfile(item.dm)
      const profile = profiles[0]
      if (!profile) throw new Error('公司简介为空')
      const combined: CombinedStockData = {
        code: item.dm,
        date: String(date ?? ''),
        list: item,
        profile
      }
      setCombined(combined)
      upsertCompanyRecord(item.dm, { profile })
      if (date) upsertDateEntry(item.dm, date, { list: item })
      setCachedCodes(prev => ({ ...prev, [item.dm]: true }))
    } catch (e) {
      console.error(e)
    } finally {
      setCachingCode(null)
    }
  }
  return (
    <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700 overflow-hidden">
      <div className="flex items-center justify-between px-6 py-4 border-b border-slate-700">
        <div>
          <h3 className="text-lg font-semibold text-white">涨停股池</h3>
          <p className="text-xs text-slate-400">{date ? `日期：${date}` : ''}（每10分钟更新）</p>
        </div>
        <button
          onClick={onRefresh}
          disabled={loading}
          className="px-3 py-1 rounded-md text-sm font-medium bg-amber-500 hover:bg-amber-600 disabled:bg-slate-600 text-white transition-colors"
        >
          刷新
        </button>
        <button
          onClick={exportCompanyCache}
          className="ml-3 px-3 py-1 rounded-md text-sm font-medium bg-slate-700 hover:bg-slate-600 text-slate-200"
        >
          导出缓存
        </button>
      </div>

      {/* 固定表头，容器可滚动 */}
      <div className="overflow-auto max-h-[70vh]">
        <table className="min-w-full divide-y divide-slate-700">
          <thead className="sticky top-0 z-10 bg-slate-900">
            <tr>
              {[
                '代码', '名称', '价格', '涨幅', '成交额', '流通市值', '总市值', '换手率', '连板数', '首封时间', '末封时间', '封板资金', '炸板次数', '统计', '详情'
              ].map((h) => (
                <th key={h} className="px-4 py-2 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800">
            {loading ? (
              Array.from({ length: 10 }).map((_, i) => (
                <tr key={i} className="animate-pulse">
                  {Array.from({ length: 14 }).map((__, j) => (
                    <td key={j} className="px-4 py-3">
                      <div className="h-4 bg-slate-700 rounded" />
                    </td>
                  ))}
                </tr>
              ))
            ) : data.length === 0 ? (
              <tr>
                <td className="px-4 py-8 text-center text-slate-400" colSpan={14}>暂无数据</td>
              </tr>
            ) : (
              data.map((item) => (
                <tr key={`${item.dm}-${item.fbt}`} className="hover:bg-slate-800/40 transition-colors">
                  <td className="px-4 py-3 text-white font-mono">{item.dm}</td>
                  <td className="px-4 py-3 text-slate-200">{item.mc}</td>
                  <td className="px-4 py-3 text-slate-200">{item.p?.toFixed(2)}</td>
                  <td className={`px-4 py-3 font-medium ${item.zf >= 0 ? 'text-red-400' : 'text-green-400'}`}>{formatPercent(item.zf)}</td>
                  <td className="px-4 py-3 text-slate-200">{formatCurrency(item.cje)}</td>
                  <td className="px-4 py-3 text-slate-200">{formatCurrency(item.lt)}</td>
                  <td className="px-4 py-3 text-slate-200">{formatCurrency(item.zsz)}</td>
                  <td className="px-4 py-3 text-slate-200">{formatPercent(item.hs)}</td>
                  <td className={`px-4 py-3 text-slate-200 ${item.lbc >= 3 ? 'text-amber-400' : ''}`}>{item.lbc}</td>
                  <td className="px-4 py-3 text-slate-200">{item.fbt}</td>
                  <td className="px-4 py-3 text-slate-200">{item.lbt}</td>
                  <td className="px-4 py-3 text-slate-200">{formatCurrency(item.zj)}</td>
                  <td className="px-4 py-3 text-slate-200">{item.zbc}</td>
                  <td className="px-4 py-3 text-slate-400 text-xs">{item.tj}</td>
                  <td className="px-4 py-3">
                    <button
                      onClick={() => handleFetchDetail(item)}
                      disabled={cachingCode === item.dm}
                      className="px-3 py-1 rounded-md text-xs font-medium bg-slate-700 hover:bg-slate-600 disabled:bg-slate-600 text-slate-200"
                    >
                      {cachingCode === item.dm
                        ? '保存中…'
                        : (getCompanyRecord(item.dm)?.dates?.[String(date || '')]?.list
                          ? '已缓存'
                          : '查看详情')}
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}
