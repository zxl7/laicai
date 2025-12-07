import { useState, useEffect, useCallback } from 'react'
import { fetchStrongStocks } from '../api/strongStocks'
import { StrongStockItem } from '../api/types'

/**
 * 使用强势股数据的Hook
 * @param initialDate 初始日期，默认使用当前日期
 */
export const useStrongStocks = (initialDate?: string) => {
  const [data, setData] = useState<StrongStockItem[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<Error | null>(null)
  const [date, setDate] = useState<string>(initialDate || new Date().toISOString().split('T')[0])

  /**
   * 获取强势股数据
   * @param bypassCache 是否绕过缓存，默认为false
   */
  const getStrongStocks = useCallback(async (bypassCache: boolean = false) => {
    setLoading(true)
    setError(null)
    try {
      const result = await fetchStrongStocks(date, bypassCache)
      setData(result)
    } catch (err) {
      setError(err instanceof Error ? err : new Error('获取强势股数据失败'))
    } finally {
      setLoading(false)
    }
  }, [date])

  // 初始加载数据
  useEffect(() => {
    getStrongStocks()
  }, [getStrongStocks])

  /**
   * 刷新数据
   */
  const refresh = useCallback(() => {
    getStrongStocks(true) // 刷新时绕过缓存
  }, [getStrongStocks])

  /**
   * 更改日期并获取数据
   */
  const changeDate = useCallback((newDate: string) => {
    setDate(newDate)
  }, [])

  return {
    data,
    loading,
    error,
    date,
    refresh,
    changeDate
  }
}