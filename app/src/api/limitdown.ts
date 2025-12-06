import { get } from './client'
import { resolveLicense } from './utils'
import type { LimitDownItem } from './types'
import { UNIFIED_DATE } from './limitup'

const BASE = import.meta.env.VITE_BIYING_API_BASE_DT ?? 'https://api.biyingapi.com/hslt/dtgc'

export { UNIFIED_DATE }

export async function fetchLimitDownList(date: string = UNIFIED_DATE): Promise<LimitDownItem[]> {
  const license = resolveLicense()
  if (!license) return []
  const url = `${BASE}/${date}/${license}`
  const data = await get<LimitDownItem[]>(url)
  return Array.isArray(data) ? data : []
}

