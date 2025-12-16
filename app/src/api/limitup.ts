import { get } from './client'
import type { LimitUpItem } from './types'
// 为保证“先使用动态数据，再后台更新股票池”，此处仅返回数据；股票池更新在页面层处理

const now = new Date()
const yyyy = `${now.getFullYear()}`
const mm = `${now.getMonth() + 1}`.padStart(2, '0')
const dd = `${now.getDate()}`.padStart(2, '0')
export const UNIFIED_DATE = `${yyyy}-${mm}-${dd}`

export async function fetchLimitUpList(date: string): Promise<LimitUpItem[]> {
  const url = `/api/quote/zt-stock-pool/${date}`
  try {
    const result = await get<{ code: number; message: string; data: { date: string; total: number; stocks: LimitUpItem[] } }>(url)
    const stocks = (result as any)?.data?.stocks
    return Array.isArray(stocks) ? stocks : []
  } catch (error) {
    console.error('Failed to fetch limit-up list:', error)
    return []
  }
}
