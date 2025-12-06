import { useEffect, useState } from 'react'
import { getCompanyCache, Store, CompanyRecord } from '../services/companyStore'
import { formatCurrency, formatPercent } from '../api/utils'
import { CompanyProfileCard } from '../components/CompanyProfileCard'
import type { CompanyProfile } from '../api/types'
import { Tag } from 'antd'
import { resolveTagColor } from '../lib/tagColors'

export function Company() {
  const [pool, setPool] = useState<Store>({})
  const [detailOpen, setDetailOpen] = useState(false)
  const [detailRec, setDetailRec] = useState<CompanyRecord | null>(null)
  useEffect(() => {
    setPool(getCompanyCache())
  }, [])

  const entries = Object.entries(pool)

  return (
    <div className="min-h-screen bg-slate-900 text-white p-6">
      <div className="max-w-7xl mx-auto">
        <div>
          <h1 className="text-3xl font-bold">股票总池</h1>
          <p className="text-slate-400">显示本地股票池缓存的最新数据</p>
        </div>

        <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700 overflow-hidden">
          <div className="px-6 py-4 border-b border-slate-700 flex items-center justify-between">
            <div className="text-sm text-slate-400">共 {entries.length} 条</div>
          </div>
          <div className="overflow-auto">
            <table className="min-w-full divide-y divide-slate-700">
              <thead className="sticky top-0 bg-slate-900">
                <tr>
                  {['代码', '名称', '涨幅', '价格', '成交额', '最近更新', '详情状态', '概念', '详情'].map(h => (
                    <th key={h} className="px-4 py-2 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {entries.map(([code, rec]) => (
                  <tr key={code} className="hover:bg-slate-800/40 transition-colors">
                    <td className="px-4 py-3 text-white font-mono">{code}</td>
                    <td className="px-4 py-3 text-slate-200">{rec.list?.mc || rec.name || '-'}</td>
                    <td className={`px-4 py-3 font-medium ${rec.list?.zf && rec.list.zf >= 0 ? 'text-red-400' : 'text-green-400'}`}>{rec.list?.zf != null ? formatPercent(rec.list.zf) : '-'}</td>
                    <td className="px-4 py-3 text-slate-200">{rec.list?.p != null ? rec.list.p.toFixed(2) : '-'}</td>
                    <td className="px-4 py-3 text-slate-200">{rec.list?.cje != null ? formatCurrency(rec.list.cje) : '-'}</td>
                    <td className="px-4 py-3 text-slate-400 text-xs">{rec.lastUpdated ? new Date(rec.lastUpdated).toLocaleString('zh-CN') : '-'}</td>
                    <td className="px-4 py-3 text-slate-200">{rec.name ? '已补全' : '缺失'}</td>
                    <td className="px-4 py-3 group">
                      {(() => {
                        const tags = (rec.idea || '').split(',').map(s => s.trim()).filter(Boolean)
                        if (tags.length === 0) return <span className="text-slate-500 text-xs">-</span>
                        const firstTwo = tags.slice(0, 2)
                        return (
                          <>
                            <div className="flex flex-wrap gap-2 group-hover:hidden">
                              {firstTwo.map(t => (
                                <Tag key={t} className="m-0" color={resolveTagColor(t)}>{t}</Tag>
                              ))}
                            </div>
                            <div className="hidden group-hover:flex flex-wrap gap-2">
                              {tags.map(t => (
                                <Tag key={t} className="m-0" color={resolveTagColor(t)}>{t}</Tag>
                              ))}
                            </div>
                          </>
                        )
                      })()}
                    </td>
                    <td className="px-4 py-3">
                      <button
                        onClick={() => { setDetailRec(rec); setDetailOpen(true) }}
                        className="px-3 py-1 rounded-md text-xs font-medium bg-slate-700 hover:bg-slate-600 text-slate-200"
                      >
                        查看详情
                      </button>
                    </td>
                  </tr>
                ))}
                {entries.length === 0 && (
                  <tr>
                    <td className="px-4 py-8 text-center text-slate-400" colSpan={9}>暂无股票池数据</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
        {detailOpen && detailRec && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60">
            <div className="bg-slate-900 rounded-xl border border-slate-700 w-full max-w-3xl max-h-[80vh] overflow-auto">
              <div className="flex items-center justify-between px-4 py-3 border-b border-slate-700">
                <div className="text-white font-semibold">公司详情</div>
                <button
                  onClick={() => { setDetailOpen(false); setDetailRec(null) }}
                  className="text-slate-300 hover:text-white"
                >
                  关闭
                </button>
              </div>
              <div className="p-4 space-y-4">
                {detailRec.name ? (
                  <CompanyProfileCard profile={detailRec as unknown as CompanyProfile} />
                ) : (
                  <div className="text-slate-400 text-sm">该公司详情尚未补全</div>
                )}
                <pre className="bg-slate-800/60 text-slate-200 text-xs rounded-lg p-3 overflow-auto max-h-[40vh]">{JSON.stringify(detailRec, null, 2)}</pre>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
