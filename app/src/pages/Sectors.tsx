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
        <div className="mb-8 animate-fade-in">
          <h1 className="text-3xl font-bold text-white mb-2">板块情绪矩阵</h1>
          <p className="text-slate-400">实时监控各板块情绪变化和热点识别</p>
        </div>

        {/* 筛选器和日期选择器 */}
        <div className="flex flex-wrap items-center gap-4 mb-6 animate-slide-up">
          <div className="flex items-center space-x-2">
            <Filter className="w-4 h-4 text-slate-400 transition-transform duration-300 hover:rotate-180" />
            <span className="text-slate-300 text-sm">筛选:</span>
          </div>
          <div className="flex space-x-2">
            {[
              { value: 'all', label: '全部' },
              { value: 'rising', label: '主升' },
              { value: 'falling', label: '退潮' }
            ].map((option, index) => (
              <button
                key={option.value}
                onClick={() => setFilter(option.value as 'all' | 'rising' | 'falling')}
                className={`px-3 py-1 rounded-full text-sm font-medium transition-all duration-300 hover:scale-105 hover:shadow-md ${filter === option.value
                  ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30 shadow-amber-500/10'
                  : 'bg-slate-800 text-slate-300 hover:bg-slate-700'}`}
                style={{ animationDelay: `${index * 50}ms` }}
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
              className="bg-slate-800 text-white border border-slate-700 rounded px-3 py-1 text-sm transition-all duration-300 hover:border-slate-600 hover:shadow-md"
            />
            <button
              onClick={() => {
                refresh()
                refreshUp()
              }}
              className="bg-slate-800 text-white border border-slate-700 rounded px-3 py-1 text-sm hover:bg-slate-700 flex items-center space-x-1 transition-all duration-300 hover:border-slate-600 hover:shadow-md hover:scale-105"
              title="刷新数据"
            >
              <RefreshCcw className="w-3 h-3 transition-transform duration-300 hover:rotate-180" />
              <span>刷新</span>
            </button>
          </div>
        </div>

        {/* 统计信息 */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          {[
            { value: sectors.length, label: '总板块数', color: 'text-white', borderColor: 'border-slate-700' },
            { value: risingSectors.length, label: '主升板块', color: 'text-amber-400', borderColor: 'border-amber-500/30' },
            { value: fallingSectors.length, label: '退潮板块', color: 'text-red-400', borderColor: 'border-red-500/30' },
            { value: hotSectors.length, label: '热点板块', color: 'text-slate-400', borderColor: 'border-slate-700' }
          ].map((stat, index) => (
            <div 
              key={stat.label} 
              className={`bg-slate-800/50 backdrop-blur-sm rounded-xl p-4 border transition-all duration-500 hover:shadow-lg hover:-translate-y-1 animate-slide-up`}
              style={{ borderColor: stat.borderColor, animationDelay: `${index * 100}ms` }}
            >
              <div className={`text-2xl font-bold ${stat.color} transition-all duration-300 hover:scale-105`}>{stat.value}</div>
              <div className="text-slate-400 text-sm">{stat.label}</div>
            </div>
          ))}
        </div>
        
        {/* 热点板块识别 */}
        {hotSectors.length > 0 && (
          <div className="mb-8">
            <h2 className="text-xl font-semibold text-amber-400 mb-4 flex items-center animate-fade-in">
              <Flame className="w-5 h-5 text-amber-500 mr-2 animate-pulse" />
              今日热点板块
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
              {hotSectors.map((sector, index) => (
                <div 
                  key={sector.id} 
                  className="bg-gradient-to-r from-amber-500/20 to-red-500/20 backdrop-blur-sm rounded-xl p-4 border border-amber-500/30 hover:shadow-lg hover:shadow-amber-500/10 transition-all duration-300 hover:scale-105"
                  style={{ animationDelay: `${index * 100}ms`, animation: 'slide-up 0.5s ease-out forwards' }}
                >
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="text-white font-bold transition-colors duration-300 hover:text-amber-400">{sector.name}</h3>
                    <Flame className="w-4 h-4 text-amber-500 animate-pulse" />
                  </div>
                  <div className="grid grid-cols-2 gap-3">
                    <div className="bg-slate-800/50 rounded p-2 transition-all duration-300 hover:bg-slate-700/50 hover:scale-105">
                      <div className="text-red-400 font-semibold text-xs">涨停</div>
                      <div className="text-white font-bold">{sector.limit_up_stocks}</div>
                    </div>
                    <div className="bg-slate-800/50 rounded p-2 transition-all duration-300 hover:bg-slate-700/50 hover:scale-105">
                      <div className="text-green-400 font-semibold text-xs">跌停</div>
                      <div className="text-white font-bold">{sector.limit_down_stocks}</div>
                    </div>
                  </div>
                  <div className="mt-3 flex items-center text-xs text-amber-300">
                    {sector.trend_direction === 'up' ? (
                      <TrendingUp className="w-3 h-3 mr-1 animate-pulse" />
                    ) : sector.trend_direction === 'down' ? (
                      <TrendingDown className="w-3 h-3 mr-1 animate-pulse" />
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
          <div className="mb-8 bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700 transition-all duration-500 hover:shadow-lg animate-fade-in">
            <h2 className="text-xl font-semibold text-white mb-4 animate-slide-up">板块情绪变化分析</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {[
                {
                  title: '上涨动力',
                  icon: <TrendingUp className="w-5 h-5 text-green-400 mr-2" />,
                  color: 'text-green-400',
                  content: (
                    <>
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
                    </>
                  )
                },
                {
                  title: '下跌压力',
                  icon: <TrendingDown className="w-5 h-5 text-red-400 mr-2" />,
                  color: 'text-red-400',
                  content: (
                    <>
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
                    </>
                  )
                },
                {
                  title: '热点轮动',
                  icon: <Flame className="w-5 h-5 text-amber-400 mr-2" />,
                  color: 'text-amber-400',
                  content: (
                    <>
                      <p className="text-slate-300 text-sm">
                        今日热点板块: <span className="text-white font-bold">{hotSectors.length}</span> 个
                      </p>
                      <p className="text-slate-300 text-sm mt-2">
                        市场热点主要集中在: 
                        {hotSectors.map(s => s.name).join(', ')}
                        {hotSectors.length === 0 ? '无明显热点' : '等板块'}
                      </p>
                    </>
                  )
                }
              ].map((item, index) => (
                <div 
                  key={item.title} 
                  className="bg-slate-700/30 rounded-lg p-4 transition-all duration-300 hover:bg-slate-700/50 hover:-translate-y-1"
                  style={{ animationDelay: `${index * 100}ms` }}
                >
                  <div className="flex items-center mb-3">
                    {item.icon}
                    <h3 className={`${item.color} font-medium`}>{item.title}</h3>
                  </div>
                  {item.content}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* 主升板块 */}
        {risingSectors.length > 0 && (
          <div className="mb-8">
            <h2 className="text-xl font-semibold text-amber-400 mb-4 flex items-center animate-fade-in">
              <div className="w-2 h-2 bg-amber-400 rounded-full mr-2 animate-pulse"></div>
              主升板块
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {risingSectors.map((sector, index) => (
                <div key={sector.id} style={{ animationDelay: `${index * 50}ms` }}>
                  <SectorCard
                    sector={sector}
                    onFavorite={toggleFavorite}
                    isFavorite={favorites.includes(sector.id)}
                  />
                </div>
              ))}
            </div>
          </div>
        )}

        {/* 退潮板块 */}
        {fallingSectors.length > 0 && (
          <div className="mb-8">
            <h2 className="text-xl font-semibold text-red-400 mb-4 flex items-center animate-fade-in">
              <div className="w-2 h-2 bg-red-400 rounded-full mr-2 animate-pulse"></div>
              退潮板块
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {fallingSectors.map((sector, index) => (
                <div key={sector.id} style={{ animationDelay: `${index * 50}ms` }}>
                  <SectorCard
                    sector={sector}
                    onFavorite={toggleFavorite}
                    isFavorite={favorites.includes(sector.id)}
                  />
                </div>
              ))}
            </div>
          </div>
        )}

        {/* 普通板块 */}
        {normalSectors.length > 0 && (
          <div className="mb-8">
            <h2 className="text-xl font-semibold text-slate-400 mb-4 animate-fade-in">其他板块</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {normalSectors.map((sector, index) => (
                <div key={sector.id} style={{ animationDelay: `${index * 50}ms` }}>
                  <SectorCard
                    sector={sector}
                    onFavorite={toggleFavorite}
                    isFavorite={favorites.includes(sector.id)}
                  />
                </div>
              ))}
            </div>
          </div>
        )}

        {loading && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {[...Array(8)].map((_, i) => (
              <div 
                key={i} 
                className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-4 border border-slate-700 animate-pulse"
                style={{ animationDelay: `${i * 50}ms` }}
              >
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
          <div className="mt-12 animate-fade-in">
            <h2 className="text-xl font-semibold text-white mb-4 flex items-center">
              <Star className="w-5 h-5 text-amber-400 mr-2 animate-pulse" />
              关注板块
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {sectors
                .filter(sector => favorites.includes(sector.id))
                .map((sector, index) => (
                  <div key={sector.id} style={{ animationDelay: `${index * 50}ms` }}>
                    <SectorCard
                      sector={sector}
                      onFavorite={toggleFavorite}
                      isFavorite={favorites.includes(sector.id)}
                    />
                  </div>
                ))}
            </div>
          </div>
        )}

        <div className="mt-8 animate-fade-in">
          <StrongStocksTable data={strongStocks} loading={luLoading} onRefresh={refreshUp} title="强势股（按连板/强度排序）" date={date} />
        </div>
      </div>
    </div>
  )
}
