import { } from 'react'
import { RefreshCcw } from 'lucide-react'
import { StrongStocksTable } from '../components/StrongStocksTable'
import { useStrongStocks } from '../hooks/useStrongStocks'

export function Sectors() {
  const { data: strongStocks, loading: luLoading, refresh: refreshUp, date, changeDate } = useStrongStocks()
  








  return (
    <div className="min-h-screen bg-slate-900 text-white p-4">
      <div className="max-w-7xl mx-auto">

        {/* 日期选择器和刷新按钮 */}
        <div className="flex items-center gap-2 mb-4 animate-slide-up">
            <span className="text-slate-300 text-sm">日期:</span>
            <input
              type="date"
              value={date}
              onChange={(e) => {
                changeDate(e.target.value)
              }}
              max={new Date().toISOString().split('T')[0]} // 限制最大日期为今天
              className="bg-slate-800 text-white border border-slate-700 rounded px-4 py-2 text-sm transition-all duration-300 hover:border-slate-600 hover:shadow-md"
            />
            <button
              onClick={() => {
                refreshUp()
              }}
              className="bg-slate-800 text-white border border-slate-700 rounded px-4 py-2 text-sm hover:bg-slate-700 flex items-center space-x-2 transition-all duration-300 hover:border-slate-600 hover:shadow-md hover:scale-105"
              title="刷新数据"
            >
              <RefreshCcw className="w-3 h-3 transition-transform duration-300 hover:rotate-180" />
              <span>刷新</span>
            </button>
        </div>

        <div className="mt-4 animate-fade-in">
          <StrongStocksTable data={strongStocks} loading={luLoading} onRefresh={refreshUp} title="强势股（按连板/强度排序）" date={date} />
        </div>
      </div>
    </div>
  )
}
