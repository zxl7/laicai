import { get } from './client'
import { StrongStockItem } from './types'

/**
 * 获取强势股数据
 * @param date 日期，格式为yyyy-MM-dd，默认使用今天的日期
 * @param bypassCache 是否绕过缓存，默认为false
 * @returns 强势股票列表
 */
export async function fetchStrongStocks(date: string = new Date().toISOString().split('T')[0], bypassCache: boolean = false): Promise<StrongStockItem[]> {
  console.log('fetchStrongStocks called with date:', date, 'bypassCache:', bypassCache)
  
  // 验证日期格式
  const dateRegex = /^\d{4}-\d{2}-\d{2}$/
  if (!dateRegex.test(date)) {
    throw new Error('日期格式不正确，请使用yyyy-MM-dd格式')
  }
  
  // 使用带日期参数的强势股票池API URL
  const url = `/api/quote/strong-stock-pool/${date}`
  console.log('API URL:', url)
  
  try {
    // API响应格式：{ code: 200, message: "", data: { date: "", total: 0, stocks: [] } }
    const result = await get<{ code: number; message: string; data: { date: string; total: number; stocks: StrongStockItem[] } }>(url, { bypassCache })
    console.log('API response received:', result)
    // 处理完整的API响应格式，数据包含在data.stocks字段中
    return Array.isArray(result?.data?.stocks) ? result.data.stocks : []
  } catch (error) {
    console.error('API request failed:', error)
    return []
  }
}
