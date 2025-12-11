import { useState, useEffect } from 'react'
import { MarketSentiment, Sector } from '../types'
import { getCompanyCache } from '../services/companyStore'
import type { CompanyRecord } from '../services/companyStore'

export function useMarketSentiment() {
  const [sentiment, setSentiment] = useState<MarketSentiment | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    // 暂停后端依赖，保留占位逻辑以便前端继续工作
    setLoading(false)
  }, [])

  const fetchMarketSentiment = async () => {
    // 已移除数据库读取，返回占位数据
    setSentiment(null)
    setError(null)
  }

  return { sentiment, loading, error }
}

/**
 * 分析板块情绪数据
 * @param companyRecords 公司记录数据
 * @returns 板块情绪分析结果
 */
function analyzeSectorSentiment(companyRecords: CompanyRecord[]): Sector[] {
  // 按行业/板块分组
  const sectorMap = new Map<string, CompanyRecord[]>()
  
  companyRecords.forEach(record => {
    // 只统计有详情数据的公司
    if (record.hy) {
      const sectorName = record.hy
      if (!sectorMap.has(sectorName)) {
        sectorMap.set(sectorName, [])
      }
      sectorMap.get(sectorName)!.push(record)
    }
  })
  
  // 转换为板块数组并计算情绪指标
  const sectors: Sector[] = Array.from(sectorMap.entries()).map(([name, companies]) => {
    // 计算板块指标
    const totalCompanies = companies.length
    const limitUpCount = companies.filter(c => c.list?.zf && parseFloat(c.list.zf.toString()) >= 9.9).length
    const risingCount = companies.filter(c => {
      const zf = typeof c.zf === 'string' ? parseFloat(c.zf) : c.zf
      return zf > 0
    }).length
    const fallingCount = companies.filter(c => {
      const zf = typeof c.zf === 'string' ? parseFloat(c.zf) : c.zf
      return zf < 0
    }).length
    const limitDownCount = companies.filter(c => c.listDown?.zf && parseFloat(c.listDown.zf.toString()) <= -9.9).length
    
    // 计算平均涨幅
    const avgIncrease = companies
      .filter(c => typeof c.zf === 'string' || typeof c.zf === 'number')
      .reduce((sum, c) => {
        const zf = typeof c.zf === 'string' ? parseFloat(c.zf) : c.zf
        return sum + zf
      }, 0) / totalCompanies
    
    // 确定趋势方向
    let trendDirection: 'up' | 'down' | 'sideways' = 'sideways'
    if (avgIncrease > 1) trendDirection = 'up'
    if (avgIncrease < -1) trendDirection = 'down'
    
    return {
      id: `sector-${name}`,
      name,
      code: name,
      limit_up_stocks: limitUpCount,
      rising_stocks: risingCount,
      falling_stocks: fallingCount,
      limit_down_stocks: limitDownCount,
      trend_direction: trendDirection,
      is_rising: limitUpCount > totalCompanies * 0.2 || avgIncrease > 2, // 20%涨停或平均涨幅>2%视为主升
      is_falling: limitDownCount > totalCompanies * 0.1 || avgIncrease < -1, // 10%跌停或平均涨幅<-1%视为退潮
      updated_at: new Date().toISOString()
    }
  })
  
  // 按涨停数量和平均涨幅排序，热点板块靠前
  return sectors.sort((a, b) => {
    // 先按涨停数量排序
    const upDiff = b.limit_up_stocks - a.limit_up_stocks
    if (upDiff !== 0) return upDiff
    
    // 再按趋势方向排序（上涨>横盘>下跌）
    const trendOrder = { up: 3, sideways: 2, down: 1 }
    return trendOrder[b.trend_direction] - trendOrder[a.trend_direction]
  })
}

export function useSectors() {
  const [sectors, setSectors] = useState<Sector[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchSectors = async () => {
    try {
      setLoading(true)
      setError(null)
      
      // 从公司存储获取数据
      const companyCache = getCompanyCache()
      const companyRecords = Object.values(companyCache)
      
      // 分析板块情绪
      const analyzedSectors = analyzeSectorSentiment(companyRecords)
      setSectors(analyzedSectors)
    } catch (err) {
      setError('获取板块数据失败')
      console.error('Failed to fetch sectors:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchSectors()
  }, [])

  return { sectors, loading, error, refresh: fetchSectors }
}
