import { get } from './client'
import type { LimitDownItem } from './types'
import { UNIFIED_DATE } from './limitup'

export { UNIFIED_DATE }

export async function fetchLimitDownList(date: string = UNIFIED_DATE): Promise<LimitDownItem[]> {
  const url = `/api/quote/dt-stock-pool/${date}`
  try {
    const result = await get<{ code: number; message: string; data: { date: string; total: number; stocks: LimitDownItem[] } }>(url)
    const stocks = (result as any)?.data?.stocks
    return Array.isArray(stocks) ? stocks : []
  } catch (error) {
    console.error('Failed to fetch limit-down list:', error)
    return []
  }
}
