import { get } from './client'
import { StrongStockItem } from './types'

/**
 * 获取股票总池数据
 * @param bypassCache 是否绕过缓存，默认为false
 * @returns 股票总池列表
 */
export async function fetchStockPool(bypassCache: boolean = false): Promise<StrongStockItem[]> {
  const url = '/api/quote/stock-pool'
  console.log('Stock pool API URL:', url)
  
  try {
    const result = await get<StrongStockItem[]>(url, { bypassCache })
    console.log('Stock pool API response:', result)
    // 确保返回的是数组
    return Array.isArray(result) ? result : []
  } catch (error) {
    console.error('Failed to fetch stock pool:', error)
    return []
  }
}