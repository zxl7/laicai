import { TrendingUp, TrendingDown, Minus, Star } from 'lucide-react'
import { Sector } from '../types'

/**
 * 单个板块卡片
 * 用途：展示板块的涨/跌停个股数与趋势，支持收藏标记
 */
interface SectorCardProps {
  sector: Sector
  onFavorite?: (sectorId: string) => void
  isFavorite?: boolean
}

/**
 * 板块卡片主组件
 */
export function SectorCard({ sector, onFavorite, isFavorite }: SectorCardProps) {
  /** 返回板块趋势图标 */
  const getTrendIcon = () => {
    switch (sector.trend_direction) {
      case 'up':
        return <TrendingUp className="w-4 h-4 text-red-500" />
      case 'down':
        return <TrendingDown className="w-4 h-4 text-green-500" />
      default:
        return <Minus className="w-4 h-4 text-slate-500" />
    }
  }

  /** 根据板块状态返回卡片样式（主升/退潮强调动效） */
  const getCardStyles = () => {
    let baseClasses = "bg-slate-800/50 backdrop-blur-sm rounded-xl p-4 border transition-all duration-300 hover:shadow-lg"
    
    if (sector.is_rising) {
      baseClasses += " border-amber-400/50 shadow-amber-400/20 animate-pulse"
    } else if (sector.is_falling) {
      baseClasses += " border-red-500/50 shadow-red-500/20 animate-pulse"
    } else {
      baseClasses += " border-slate-700 hover:border-slate-600"
    }
    
    return baseClasses
  }

  /** 净额颜色（涨停-跌停） */
  const getScoreColor = () => {
    const score = sector.limit_up_stocks - sector.limit_down_stocks
    if (score >= 5) return 'text-red-500'
    if (score >= 0) return 'text-yellow-500'
    return 'text-green-500'
  }

  /** 计算净额（涨停-跌停） */
  const getScore = () => {
    return sector.limit_up_stocks - sector.limit_down_stocks
  }

  return (
    <div className={getCardStyles()}>
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center space-x-2">
          <h3 className="text-white font-semibold">{sector.name}</h3>
          {getTrendIcon()}
        </div>
        {onFavorite && (
          <button
            onClick={() => onFavorite(sector.id)}
            className={cn(
              "p-1 rounded-full transition-colors",
              isFavorite ? "text-amber-400 hover:text-amber-300" : "text-slate-500 hover:text-slate-400"
            )}
          >
            <Star className={cn("w-4 h-4", isFavorite && "fill-current")} />
          </button>
        )}
      </div>

      <div className="grid grid-cols-2 gap-3 mb-3">
        <div className="bg-slate-700/30 rounded-lg p-2">
          <div className="text-red-500 font-semibold text-sm">{sector.limit_up_stocks}</div>
          <div className="text-slate-400 text-xs">涨停</div>
        </div>
        <div className="bg-slate-700/30 rounded-lg p-2">
          <div className="text-green-500 font-semibold text-sm">{sector.limit_down_stocks}</div>
          <div className="text-slate-400 text-xs">跌停</div>
        </div>
      </div>

      <div className="flex items-center justify-between">
        <div className="text-xs text-slate-400">
          净额: <span className={cn("font-medium", getScoreColor())}>{getScore()}</span>
        </div>
        <div className="text-xs text-slate-500">
          {new Date(sector.updated_at).toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })}
        </div>
      </div>

      {sector.is_rising && (
        <div className="absolute inset-0 rounded-xl border-2 border-amber-400 opacity-50 animate-ping"></div>
      )}
      {sector.is_falling && (
        <div className="absolute inset-0 rounded-xl border-2 border-red-500 opacity-50 animate-ping animation-delay-1000"></div>
      )}
    </div>
  )
}

function cn(...classes: string[]) {
  return classes.filter(Boolean).join(' ')
}
