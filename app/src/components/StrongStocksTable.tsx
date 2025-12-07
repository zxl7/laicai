import type { StrongStockItem } from '../api/types'

interface StrongStocksTableProps {
  data: StrongStockItem[]
  loading?: boolean
  onRefresh?: () => void
  title?: string
}

const formatPercent = (v: number): string => `${(v).toFixed(2)}%`
const formatCurrency = (v: number): string => {
  if (v >= 1e9) return `${(v / 1e9).toFixed(2)}亿`
  if (v >= 1e8) return `${(v / 1e8).toFixed(2)}亿`
  if (v >= 1e6) return `${(v / 1e6).toFixed(2)}百万`
  if (v >= 1e4) return `${(v / 1e4).toFixed(2)}万`
  return `${v}`
}

export function StrongStocksTable({ data, loading, onRefresh, title }: StrongStocksTableProps) {
  return (
    <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-4 border border-slate-700">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-white">{title || '强势股池'}</h3>
        {onRefresh && (
          <button onClick={onRefresh} className="px-3 py-2 rounded-md text-sm font-medium bg-amber-500 hover:bg-amber-600 text-white disabled:bg-slate-600" disabled={!!loading}>
            刷新
          </button>
        )}
      </div>

      {loading ? (
        <div className="h-48 bg-slate-700 rounded animate-pulse" />
      ) : (
        <div className="overflow-x-auto">
          <table className="min-w-full text-sm">
            <thead>
              <tr className="text-slate-400">
                <th className="text-left px-3 py-2">代码</th>
                <th className="text-left px-3 py-2">名称</th>
                <th className="text-left px-3 py-2">价格</th>
                <th className="text-left px-3 py-2">涨幅</th>
                <th className="text-left px-3 py-2">涨停价</th>
                <th className="text-left px-3 py-2">涨速</th>
                <th className="text-left px-3 py-2">新高</th>
                <th className="text-left px-3 py-2">量比</th>
                <th className="text-left px-3 py-2">换手率</th>
                <th className="text-left px-3 py-2">成交额</th>
                <th className="text-left px-3 py-2">涨停统计</th>
              </tr>
            </thead>
            <tbody>
              {data.slice(0, 20).map((it) => (
                <tr key={it.dm} className="border-t border-slate-700">
                  <td className="px-3 py-2 text-slate-300">{it.dm}</td>
                  <td className="px-3 py-2 text-white">{it.mc}</td>
                  <td className="px-3 py-2 text-slate-300">{it.p.toFixed(2)}</td>
                  <td className={`px-3 py-2 font-medium ${it.zf >= 0 ? 'text-red-400' : 'text-green-400'}`}>{formatPercent(it.zf)}</td>
                  <td className="px-3 py-2 text-slate-300">{it.ztp.toFixed(2)}</td>
                  <td className={`px-3 py-2 ${it.zs >= 0 ? 'text-red-400' : 'text-green-400'}`}>{formatPercent(it.zs)}</td>
                  <td className="px-3 py-2">{it.nh === 1 ? '是' : '否'}</td>
                  <td className="px-3 py-2 text-slate-300">{it.lb.toFixed(2)}</td>
                  <td className="px-3 py-2 text-slate-300">{formatPercent(it.hs)}</td>
                  <td className="px-3 py-2 text-slate-300">{formatCurrency(it.cje)}</td>
                  <td className="px-3 py-2 text-slate-300">{it.tj}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}

