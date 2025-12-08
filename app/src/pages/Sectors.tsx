import { useState, useEffect } from 'react'
import { useSectors } from '../hooks/useSentimentData'
import { SectorCard } from '../components/SectorCard'
import { Filter, Star, Flame, TrendingUp, TrendingDown, RefreshCcw } from 'lucide-react'
import { StrongStocksTable } from '../components/StrongStocksTable'
import { useStrongStocks } from '../hooks/useStrongStocks'
import { Sector } from '../types'

export function Sectors() {
  const { sectors, loading, error, refresh } = useSectors()
  const [favorites, setFavorites] = useState<string[]>([])
  const [filter, setFilter] = useState<'all' | 'rising' | 'falling'>('all')
  const { data: strongStocks, loading: luLoading, refresh: refreshUp, date, changeDate } = useStrongStocks()
  const [hotSectors, setHotSectors] = useState<Sector[]>([])
  
  // 识别热点板块
  useEffect(() => {
    if (sectors.length > 0) {
      // 热点板块定义：涨停股数大于等于3且占比超过20%
      const identifiedHotSectors = sectors.filter(sector => 
        sector.limit_up_stocks >= 3 && 
        sector.trend_direction === 'up'
      ).slice(0, 5) // 只显示前5个热点板块
      
      setHotSectors(identifiedHotSectors)
    }
  }, [sectors])

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
          
          {/* 日期选择器和刷新按钮 */}
          <div className="flex items-center space-x-2 ml-auto">
            <span className="text-slate-300 text-sm">日期:</span>
            <input
              type="date"
              value={date}
              onChange={(e) => {
                changeDate(e.target.value)
                refresh() // 日期变化时刷新板块数据
              }}
              max={new Date().toISOString().split('T')[0]} // 限制最大日期为今天
              className="bg-slate-800 text-white border border-slate-700 rounded px-3 py-1 text-sm"
            />
            <button
              onClick={() => {
                refresh()
                refreshUp()
              }}
              className="bg-slate-800 text-white border border-slate-700 rounded px-3 py-1 text-sm hover:bg-slate-700 flex items-center space-x-1"
              title="刷新数据"
            >
              <RefreshCcw className="w-3 h-3" />
              <span>刷新</span>
            </button>
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
            <div className="text-2xl font-bold text-slate-400">{hotSectors.length}</div>
            <div className="text-slate-400 text-sm">热点板块</div>
          </div>
        </div>
        
        {/* 热点板块识别 */}
        {hotSectors.length > 0 && (
          <div className="mb-8">
            <h2 className="text-xl font-semibold text-amber-400 mb-4 flex items-center">
              <Flame className="w-5 h-5 text-amber-500 mr-2" />
              今日热点板块
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
              {hotSectors.map(sector => (
                <div 
                  key={sector.id} 
                  className="bg-gradient-to-r from-amber-500/20 to-red-500/20 backdrop-blur-sm rounded-xl p-4 border border-amber-500/30 hover:shadow-lg hover:shadow-amber-500/10 transition-all"
                >
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="text-white font-bold">{sector.name}</h3>
                    <Flame className="w-4 h-4 text-amber-500" />
                  </div>
                  <div className="grid grid-cols-2 gap-3">
                    <div className="bg-slate-800/50 rounded p-2">
                      <div className="text-red-400 font-semibold text-xs">涨停</div>
                      <div className="text-white font-bold">{sector.limit_up_stocks}</div>
                    </div>
                    <div className="bg-slate-800/50 rounded p-2">
                      <div className="text-green-400 font-semibold text-xs">跌停</div>
                      <div className="text-white font-bold">{sector.limit_down_stocks}</div>
                    </div>
                  </div>
                  <div className="mt-3 flex items-center text-xs text-amber-300">
                    {sector.trend_direction === 'up' ? (
                      <TrendingUp className="w-3 h-3 mr-1" />
                    ) : sector.trend_direction === 'down' ? (
                      <TrendingDown className="w-3 h-3 mr-1" />
                    ) : null}
                    <span>
                      {sector.trend_direction === 'up' ? '强势上涨' : 
                       sector.trend_direction === 'down' ? '快速下跌' : '横盘震荡'}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
        
        {/* 板块情绪变化分析 */}
        {sectors.length > 0 && (
          <div className="mb-8 bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
            <h2 className="text-xl font-semibold text-white mb-4">板块情绪变化分析</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-slate-700/30 rounded-lg p-4">
                <div className="flex items-center mb-3">
                  <TrendingUp className="w-5 h-5 text-green-400 mr-2" />
                  <h3 className="text-green-400 font-medium">上涨动力</h3>
                </div>
                <p className="text-slate-300 text-sm">
                  主升板块: <span className="text-white font-bold">{risingSectors.length}</span> 个，
                  占比 <span className="text-white font-bold">{((risingSectors.length / sectors.length) * 100).toFixed(1)}%</span>
                </p>
                <p className="text-slate-300 text-sm mt-2">
                  涨停个股主要集中在: 
                  {sectors
                    .filter(s => s.limit_up_stocks > 0)
                    .sort((a, b) => b.limit_up_stocks - a.limit_up_stocks)
                    .slice(0, 3)
                    .map(s => s.name)
                    .join(', ')}
                  等板块
                </p>
              </div>
              <div className="bg-slate-700/30 rounded-lg p-4">
                <div className="flex items-center mb-3">
                  <TrendingDown className="w-5 h-5 text-red-400 mr-2" />
                  <h3 className="text-red-400 font-medium">下跌压力</h3>
                </div>
                <p className="text-slate-300 text-sm">
                  退潮板块: <span className="text-white font-bold">{fallingSectors.length}</span> 个，
                  占比 <span className="text-white font-bold">{((fallingSectors.length / sectors.length) * 100).toFixed(1)}%</span>
                </p>
                <p className="text-slate-300 text-sm mt-2">
                  跌停个股主要集中在: 
                  {sectors
                    .filter(s => s.limit_down_stocks > 0)
                    .sort((a, b) => b.limit_down_stocks - a.limit_down_stocks)
                    .slice(0, 3)
                    .map(s => s.name)
                    .join(', ')}
                  等板块
                </p>
              </div>
              <div className="bg-slate-700/30 rounded-lg p-4">
                <div className="flex items-center mb-3">
                  <Flame className="w-5 h-5 text-amber-400 mr-2" />
                  <h3 className="text-amber-400 font-medium">热点轮动</h3>
                </div>
                <p className="text-slate-300 text-sm">
                  今日热点板块: <span className="text-white font-bold">{hotSectors.length}</span> 个
                </p>
                <p className="text-slate-300 text-sm mt-2">
                  市场热点主要集中在: 
                  {hotSectors.map(s => s.name).join(', ')}
                  {hotSectors.length === 0 ? '无明显热点' : '等板块'}
                </p>
              </div>
            </div>
          </div>
        )}

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
        
        {/* 关注板块 */}
        {favorites.length > 0 && (
          <div className="mt-12">
            <h2 className="text-xl font-semibold text-white mb-4 flex items-center">
              <Star className="w-5 h-5 text-amber-400 mr-2" />
              关注板块
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {sectors
                .filter(sector => favorites.includes(sector.id))
                .map(sector => (
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

        <div className="mt-8">
          <StrongStocksTable data={strongStocks} loading={luLoading} onRefresh={refreshUp} title="强势股（按连板/强度排序）" date={date} />
        </div>
      </div>
    </div>
  )
}
