import { get } from './client'
import { resolveLicense } from './utils'
import type { LimitUpItem } from './types'
// 为保证“先使用动态数据，再后台更新股票池”，此处仅返回数据；股票池更新在页面层处理

export const UNIFIED_DATE = '2025-12-05'
const BASE = import.meta.env.VITE_BIYING_API_BASE ?? 'https://api.biyingapi.com/hslt/ztgc'

export async function fetchLimitUpList(date: string): Promise<LimitUpItem[]> {
  const license = resolveLicense()
  if (!license) return []
  const url = `${BASE}/${date}/${license}`
  const data = await get<LimitUpItem[]>(url)
  return Array.isArray(data) ? data : []
}
