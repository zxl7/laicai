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
    const result = await get<{ data: { stocks: StrongStockItem[] } }>(url, { bypassCache })
    // 正确处理接口返回的 { data: { stocks: [...] } } 结构
    return result.data.stocks || []
  } catch (error) {
    console.error('Failed to fetch stock pool:', error)
    return []
  }
}