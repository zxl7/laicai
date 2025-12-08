import { useState, useEffect, useCallback } from 'react'
import { fetchStrongStocks } from '../api/strongStocks'
import { StrongStockItem } from '../api/types'
import { getCompanyCache } from '../services/companyStore'

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

      // 如果强势股数据为空，从股票总池中获取数据
      if (result.length === 0) {
        const companyCache = getCompanyCache()
        const stockPool = Object.values(companyCache)

        // 将股票总池数据转换为StrongStockItem格式
        const convertedData: StrongStockItem[] = stockPool
          .filter(item => item.list || item.p) // 确保有必要的价格数据
          .map(item => {
            // 优先使用list中的数据（如果有），否则使用直接字段
            const baseData = item.list || item
            // 使用类型断言和可选链操作符安全地访问可能不存在的属性
            const dataObj = baseData as Record<string, any>
            return {
              dm: item.code,
              mc: dataObj.mc || item.name || '',
              p: parseFloat(dataObj.p || '0'),
              ztp: parseFloat(dataObj.ztp || '0'), // 涨停价可能不存在，设置默认值
              zf: parseFloat(dataObj.zf || '0'),
              cje: parseFloat(dataObj.cje || '0'),
              lt: parseFloat(dataObj.lt || '0'),
              zsz: parseFloat(dataObj.zsz || '0'),
              zs: parseFloat(dataObj.zs || '0'), // 涨速可能不存在，设置默认值
              nh: parseInt(dataObj.nh || '0'), // 是否新高可能不存在，设置默认值
              lb: parseFloat(dataObj.lb || '0'), // 量比可能不存在，设置默认值
              hs: parseFloat(dataObj.hs || '0'),
              tj: dataObj.tj || ''
            }
          })
          .filter(item => item.dm && item.mc) // 过滤掉缺少代码或名称的数据
          .sort((a, b) => b.zf - a.zf) // 按照涨幅降序排序

        setData(convertedData)
      } else {

        setData(result)
      }
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