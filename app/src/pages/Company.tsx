import { useEffect, useState } from 'react'
import { getCompanyCache, Store } from '../services/companyStore'
import { formatCurrency, formatPercent } from '../api/utils'

export function Company() {
  const [pool, setPool] = useState<Store>({})
  useEffect(() => {
    setPool(getCompanyCache())
  }, [])

  const entries = Object.entries(pool)

  return (
    <div className="min-h-screen bg-slate-900 text-white p-6">
      <div className="max-w-7xl mx-auto space-y-6">
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
                  {['代码', '名称', '涨幅', '价格', '成交额', '最近更新', '详情状态'].map(h => (
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
                  </tr>
                ))}
                {entries.length === 0 && (
                  <tr>
                    <td className="px-4 py-8 text-center text-slate-400" colSpan={7}>暂无股票池数据</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  )
}
