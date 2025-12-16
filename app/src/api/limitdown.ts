import { get } from './client'
import type { LimitDownItem } from './types'
import { UNIFIED_DATE } from './limitup'

export { UNIFIED_DATE }

export async function fetchLimitDownList(date: string = UNIFIED_DATE): Promise<LimitDownItem[]> {
  const url = `/api/quote/dt-stock-pool/${date}`
  try {
    // 确保请求的是当前选中的日期
    console.log('Fetching limit-down list for date:', date)
    const result = await get<{ code: number; message: string; data: { date: string; total: number; stocks: LimitDownItem[] } }>(url)
    // 正确解析API响应结构 - get函数已经返回res.data
    console.log('Limit-down list API result:', result)
    const stocks = result?.data?.stocks
    console.log('Limit-down stocks:', stocks)
    return Array.isArray(stocks) ? stocks : []
  } catch (error) {
    console.error('Failed to fetch limit-down list:', error)
    return []
  }
}
