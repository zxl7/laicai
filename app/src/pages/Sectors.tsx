import { useState } from 'react'
import { useSectors } from '../hooks/useSentimentData'
import { SectorCard } from '../components/SectorCard'
import { Filter } from 'lucide-react'
import { StrongStocksTable } from '../components/StrongStocksTable'
import { useStrongStocks } from '../hooks/useStrongStocks'

export function Sectors() {
  const { sectors, loading, error } = useSectors()
  const [favorites, setFavorites] = useState<string[]>([])
  const [filter, setFilter] = useState<'all' | 'rising' | 'falling'>('all')
  const { data: strongStocks, loading: luLoading, refresh: refreshUp, date, changeDate } = useStrongStocks()

  const toggleFavorite = (sectorId: string) => {
    setFavorites(prev => 
      prev.includes(sectorId) 
        ? prev.filter(id => id !== sectorId)
        : [...prev, sectorId]
    )
  }

  const filteredSectors = sectors.filter(sector => {
    if (filter === 'rising') return sector.is_rising
    if (filter === 'falling') return sector.is_falling
    return true
  })

  const risingSectors = filteredSectors.filter(s => s.is_rising)
  const fallingSectors = filteredSectors.filter(s => s.is_falling)
  const normalSectors = filteredSectors.filter(s => !s.is_rising && !s.is_falling)

  if (error) {
    return (
      <div className="min-h-screen bg-slate-900 text-white p-6">
        <div className="max-w-7xl mx-auto">
          <div className="bg-red-900/20 border border-red-500/30 rounded-lg p-4 text-red-400">
            错误: {error}
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-slate-900 text-white p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">板块情绪矩阵</h1>
          <p className="text-slate-400">实时监控各板块情绪变化和热点识别</p>
        </div>

        {/* 筛选器和日期选择器 */}
        <div className="flex flex-wrap items-center gap-4 mb-6">
          <div className="flex items-center space-x-2">
            <Filter className="w-4 h-4 text-slate-400" />
            <span className="text-slate-300 text-sm">筛选:</span>
          </div>
          <div className="flex space-x-2">
            {[
              { value: 'all', label: '全部' },
              { value: 'rising', label: '主升' },
              { value: 'falling', label: '退潮' }
            ].map(option => (
              <button
                key={option.value}
                onClick={() => setFilter(option.value as 'all' | 'rising' | 'falling')}
                className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
                  filter === option.value
                    ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                    : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
                }`}
              >
                {option.label}
              </button>
            ))}
          </div>
          
          {/* 日期选择器 */}
          <div className="flex items-center space-x-2 ml-auto">
            <span className="text-slate-300 text-sm">日期:</span>
            <input
              type="date"
              value={date}
              onChange={(e) => changeDate(e.target.value)}
              max={new Date().toISOString().split('T')[0]} // 限制最大日期为今天
              className="bg-slate-800 text-white border border-slate-700 rounded px-3 py-1 text-sm"
            />
          </div>
        </div>

        {/* 统计信息 */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-4 border border-slate-700">
            <div className="text-2xl font-bold text-white">{sectors.length}</div>
            <div className="text-slate-400 text-sm">总板块数</div>
          </div>
          <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-4 border border-slate-700">
            <div className="text-2xl font-bold text-amber-400">{risingSectors.length}</div>
            <div className="text-slate-400 text-sm">主升板块</div>
          </div>
          <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-4 border border-slate-700">
            <div className="text-2xl font-bold text-red-400">{fallingSectors.length}</div>
            <div className="text-slate-400 text-sm">退潮板块</div>
          </div>
          <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-4 border border-slate-700">
            <div className="text-2xl font-bold text-slate-400">{favorites.length}</div>
            <div className="text-slate-400 text-sm">关注板块</div>
          </div>
        </div>

        {/* 主升板块 */}
        {risingSectors.length > 0 && (
          <div className="mb-8">
            <h2 className="text-xl font-semibold text-amber-400 mb-4 flex items-center">
              <div className="w-2 h-2 bg-amber-400 rounded-full mr-2 animate-pulse"></div>
              主升板块
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {risingSectors.map(sector => (
                <SectorCard
                  key={sector.id}
                  sector={sector}
                  onFavorite={toggleFavorite}
                  isFavorite={favorites.includes(sector.id)}
                />
              ))}
            </div>
          </div>
        )}

        {/* 退潮板块 */}
        {fallingSectors.length > 0 && (
          <div className="mb-8">
            <h2 className="text-xl font-semibold text-red-400 mb-4 flex items-center">
              <div className="w-2 h-2 bg-red-400 rounded-full mr-2 animate-pulse"></div>
              退潮板块
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {fallingSectors.map(sector => (
                <SectorCard
                  key={sector.id}
                  sector={sector}
                  onFavorite={toggleFavorite}
                  isFavorite={favorites.includes(sector.id)}
                />
              ))}
            </div>
          </div>
        )}

        {/* 普通板块 */}
        {normalSectors.length > 0 && (
          <div className="mb-8">
            <h2 className="text-xl font-semibold text-slate-400 mb-4">其他板块</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {normalSectors.map(sector => (
                <SectorCard
                  key={sector.id}
                  sector={sector}
                  onFavorite={toggleFavorite}
                  isFavorite={favorites.includes(sector.id)}
                />
              ))}
            </div>
          </div>
        )}

        {loading && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {[...Array(8)].map((_, i) => (
              <div key={i} className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-4 border border-slate-700 animate-pulse">
                <div className="h-6 bg-slate-700 rounded mb-3"></div>
                <div className="grid grid-cols-2 gap-3 mb-3">
                  <div className="h-8 bg-slate-700 rounded"></div>
                  <div className="h-8 bg-slate-700 rounded"></div>
                </div>
                <div className="h-4 bg-slate-700 rounded"></div>
              </div>
            ))}
          </div>
        )}

        {!loading && filteredSectors.length === 0 && (
          <div className="text-center py-12">
            <div className="text-slate-400 text-lg mb-2">暂无符合条件的板块</div>
            <div className="text-slate-500 text-sm">尝试调整筛选条件或稍后再试</div>
          </div>
        )}

        <div className="mt-8">
          <StrongStocksTable data={strongStocks} loading={luLoading} onRefresh={refreshUp} title="强势股（按连板/强度排序）" />
        </div>
      </div>
    </div>
  )
}
