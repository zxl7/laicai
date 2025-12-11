import { TrendingUp, TrendingDown, Minus, Star, Clock } from 'lucide-react'
import { Sector } from '../types'
import { useRef, useEffect, useState } from 'react'

/**
 * 单个板块卡片
 * 用途：展示板块的涨/跌停个股数与趋势，支持收藏标记
 */
interface SectorCardProps {
  sector: Sector
  onFavorite: (sectorId: string) => void
  isFavorite: boolean
}

/**
 * 板块卡片主组件
 */
export function SectorCard({ sector, onFavorite, isFavorite }: SectorCardProps) {
  const cardRef = useRef<HTMLDivElement>(null)
  const [isVisible, setIsVisible] = useState(false)

  // 进入动画效果
  useEffect(() => {
    // 为每个卡片添加不同的延迟，实现交错动画
    const delay = Math.random() * 0.3
    const timer = setTimeout(() => {
      setIsVisible(true)
    }, delay * 1000)

    return () => clearTimeout(timer)
  }, [])

  /** 返回板块趋势图标 */
  const getTrendIcon = () => {
    if (sector.trend_direction === 'up') {
      return <TrendingUp className="w-4 h-4 text-red-400" />
    } else if (sector.trend_direction === 'down') {
      return <TrendingDown className="w-4 h-4 text-green-400" />
    }
    return <Minus className="w-4 h-4 text-slate-400" />
  }

  /** 处理维度点击事件 */
  const handleDimensionClick = (dimension: 'limit_up' | 'rising' | 'falling' | 'limit_down') => {
    // 这里可以添加跳转到对应列表的逻辑
    console.log(`Clicked ${dimension} for sector ${sector.name}`);
  }

  /** 获取趋势颜色 */
  const getTrendColor = () => {
    if (sector.trend_direction === 'up') return 'text-red-400'
    if (sector.trend_direction === 'down') return 'text-green-400'
    return 'text-slate-400'
  }

  /** 根据板块状态返回卡片样式（主升/退潮强调动效） */
  const getCardStyles = () => {
    const baseClasses = 'bg-slate-800/50 backdrop-blur-sm rounded-xl p-4 border transition-all duration-300 hover:shadow-lg hover:scale-105 relative overflow-hidden'
    
    if (sector.is_rising) {
      return `${baseClasses} border-amber-500/30 bg-gradient-to-br from-amber-500/10 to-transparent hover:bg-gradient-to-br from-amber-500/20 to-transparent hover:border-amber-500/50`
    } else if (sector.is_falling) {
      return `${baseClasses} border-red-500/30 bg-gradient-to-br from-red-500/10 to-transparent hover:bg-gradient-to-br from-red-500/20 to-transparent hover:border-red-500/50`
    }
    
    return `${baseClasses} border-slate-700 hover:bg-slate-800 hover:border-slate-600`
  }

  // 计算涨跌比
  const getRiseFallRatio = () => {
    return `${sector.rising_stocks}:${sector.falling_stocks}`
  }

  return (
    <div 
      ref={cardRef}
      className={`${getCardStyles()} ${sector.is_rising ? 'border-amber-500/50' : ''} ${sector.is_falling ? 'border-red-500/50' : ''} ${isVisible ? 'animate-slide-up' : 'opacity-0 translate-y-4'}`}
    >
      {/* 卡片背景动画 */}
      <div className="absolute inset-0 bg-gradient-to-r from-transparent to-slate-700/30 opacity-0 hover:opacity-100 transition-opacity duration-500"></div>

      {/* 板块名称和趋势 */}
      <div className="flex items-center justify-between mb-2 relative z-10">
        <h3 className="text-white font-bold text-sm transition-all duration-300 hover:text-amber-400">{sector.name}</h3>
        <div className="flex items-center space-x-1">
          {getTrendIcon()}
          <button
            onClick={() => onFavorite(sector.id)}
            className={`w-5 h-5 flex items-center justify-center rounded-full transition-all duration-300 ${isFavorite ? 'text-amber-400 scale-110' : 'text-slate-500 hover:text-slate-300 hover:scale-110'}`}
            title={isFavorite ? '取消关注' : '关注板块'}
          >
            <Star className={`w-4 h-4 ${isFavorite ? 'fill-current' : ''}`} />
          </button>
        </div>
      </div>

      {/* 板块数据维度 */}
      <div className="grid grid-cols-2 gap-3 mb-3 relative z-10">
        <div 
          className="bg-slate-700/50 rounded p-2 transition-all duration-300 hover:bg-red-500/20 hover:border-red-500/50 hover:scale-105 cursor-pointer border border-transparent"
          onClick={() => handleDimensionClick('limit_up')}
        >
          <div className="text-xs font-semibold text-red-400">涨停</div>
          <div className="text-white font-bold">{sector.limit_up_stocks}</div>
        </div>
        <div 
          className="bg-slate-700/50 rounded p-2 transition-all duration-300 hover:bg-red-500/10 hover:border-red-500/30 hover:scale-105 cursor-pointer border border-transparent"
          onClick={() => handleDimensionClick('rising')}
        >
          <div className="text-xs font-semibold text-red-400">上涨</div>
          <div className="text-white font-bold">{sector.rising_stocks}</div>
        </div>
        <div 
          className="bg-slate-700/50 rounded p-2 transition-all duration-300 hover:bg-green-500/10 hover:border-green-500/30 hover:scale-105 cursor-pointer border border-transparent"
          onClick={() => handleDimensionClick('falling')}
        >
          <div className="text-xs font-semibold text-green-400">下跌</div>
          <div className="text-white font-bold">{sector.falling_stocks}</div>
        </div>
        <div 
          className="bg-slate-700/50 rounded p-2 transition-all duration-300 hover:bg-green-500/20 hover:border-green-500/50 hover:scale-105 cursor-pointer border border-transparent"
          onClick={() => handleDimensionClick('limit_down')}
        >
          <div className="text-xs font-semibold text-green-400">跌停</div>
          <div className="text-white font-bold">{sector.limit_down_stocks}</div>
        </div>
      </div>

      {/* 趋势信息 */}
      <div className="flex justify-between items-center text-xs relative z-10">
        <div className="flex items-center">
          <span className="text-slate-400 mr-1">涨跌比:</span>
          <span className="font-semibold text-white">
            {getRiseFallRatio()}
          </span>
        </div>
        <div className="flex items-center">
          <span className="text-slate-400 mr-1">趋势:</span>
          <span className={`font-semibold ${getTrendColor()}`}>
            {sector.trend_direction === 'up' ? '上涨' : sector.trend_direction === 'down' ? '下跌' : '横盘'}
          </span>
        </div>
      </div>

      {/* 更新时间 */}
      <div className="text-xs text-slate-500 mt-2 flex items-center relative z-10">
        <Clock className="w-3 h-3 mr-1" />
        {new Date(sector.updated_at).toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })}
      </div>

      {/* 脉冲动画效果 */}
      {(sector.is_rising || sector.is_falling) && (
        <div className={`absolute inset-0 rounded-xl opacity-0 pointer-events-none ${sector.is_rising ? 'animate-pulse-rising' : 'animate-pulse-falling'} transition-opacity duration-500 hover:opacity-30`}></div>
      )}
    </div>
  )
}


