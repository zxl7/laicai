import { Sector } from '../types'

/**
 * 板块情绪监控矩阵
 * 用途：按主升/退潮/普通分区展示板块情绪与关键指标
 */
interface SectorSentimentMatrixProps {
  sectors: Sector[]
  loading: boolean
}

/**
 * 矩阵主组件
 */
export function SectorSentimentMatrix({ sectors, loading }: SectorSentimentMatrixProps) {
  if (loading) {
    return (
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
    )
  }

  /** 分类板块列表 */
  const risingSectors = sectors.filter(s => s.is_rising)
  const fallingSectors = sectors.filter(s => s.is_falling)
  const normalSectors = sectors.filter(s => !s.is_rising && !s.is_falling)

  return (
    <div className="space-y-8">
      {/* 主升板块 */}
      {risingSectors.length > 0 && (
        <div>
          <h2 className="text-xl font-semibold text-amber-400 mb-4 flex items-center">
            <div className="w-2 h-2 bg-amber-400 rounded-full mr-2 animate-pulse"></div>
            主升板块
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {risingSectors.map(sector => (
              <div key={sector.id} className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-4 border border-amber-400/50 shadow-amber-400/20">
                <div className="flex items-center justify-between mb-3">
                  <h3 className="text-white font-semibold">{sector.name}</h3>
                  <div className="w-2 h-2 bg-amber-400 rounded-full animate-pulse"></div>
                </div>
                <div className="grid grid-cols-2 gap-3 mb-3">
                  <div className="bg-slate-700/30 rounded-lg p-2">
                    <div className="text-green-500 font-semibold text-sm">{sector.limit_up_stocks}</div>
                    <div className="text-slate-400 text-xs">涨停</div>
                  </div>
                  <div className="bg-slate-700/30 rounded-lg p-2">
                    <div className="text-red-500 font-semibold text-sm">{sector.limit_down_stocks}</div>
                    <div className="text-slate-400 text-xs">跌停</div>
                  </div>
                </div>
                <div className="text-xs text-slate-400">
                  净额: <span className="font-medium text-green-500">{sector.limit_up_stocks - sector.limit_down_stocks}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 退潮板块 */}
      {fallingSectors.length > 0 && (
        <div>
          <h2 className="text-xl font-semibold text-red-400 mb-4 flex items-center">
            <div className="w-2 h-2 bg-red-400 rounded-full mr-2 animate-pulse"></div>
            退潮板块
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {fallingSectors.map(sector => (
              <div key={sector.id} className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-4 border border-red-500/50 shadow-red-500/20">
                <div className="flex items-center justify-between mb-3">
                  <h3 className="text-white font-semibold">{sector.name}</h3>
                  <div className="w-2 h-2 bg-red-400 rounded-full animate-pulse"></div>
                </div>
                <div className="grid grid-cols-2 gap-3 mb-3">
                  <div className="bg-slate-700/30 rounded-lg p-2">
                    <div className="text-green-500 font-semibold text-sm">{sector.limit_up_stocks}</div>
                    <div className="text-slate-400 text-xs">涨停</div>
                  </div>
                  <div className="bg-slate-700/30 rounded-lg p-2">
                    <div className="text-red-500 font-semibold text-sm">{sector.limit_down_stocks}</div>
                    <div className="text-slate-400 text-xs">跌停</div>
                  </div>
                </div>
                <div className="text-xs text-slate-400">
                  净额: <span className="font-medium text-red-500">{sector.limit_up_stocks - sector.limit_down_stocks}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 普通板块 */}
      {normalSectors.length > 0 && (
        <div>
          <h2 className="text-xl font-semibold text-slate-400 mb-4">其他板块</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {normalSectors.map(sector => (
              <div key={sector.id} className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-4 border border-slate-700">
                <div className="flex items-center justify-between mb-3">
                  <h3 className="text-white font-semibold">{sector.name}</h3>
                  <div className="w-2 h-2 bg-slate-500 rounded-full"></div>
                </div>
                <div className="grid grid-cols-2 gap-3 mb-3">
                  <div className="bg-slate-700/30 rounded-lg p-2">
                    <div className="text-green-500 font-semibold text-sm">{sector.limit_up_stocks}</div>
                    <div className="text-slate-400 text-xs">涨停</div>
                  </div>
                  <div className="bg-slate-700/30 rounded-lg p-2">
                    <div className="text-red-500 font-semibold text-sm">{sector.limit_down_stocks}</div>
                    <div className="text-slate-400 text-xs">跌停</div>
                  </div>
                </div>
                <div className="text-xs text-slate-400">
                  净额: <span className="font-medium text-slate-300">{sector.limit_up_stocks - sector.limit_down_stocks}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {!loading && sectors.length === 0 && (
        <div className="text-center py-12">
          <div className="text-slate-400 text-lg mb-2">暂无板块数据</div>
          <div className="text-slate-500 text-sm">请稍后再试</div>
        </div>
      )}
    </div>
  )
}
