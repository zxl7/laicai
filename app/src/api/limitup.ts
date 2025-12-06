import { get } from './client'
import { resolveLicense } from './utils'
import type { LimitUpItem } from './types'
import { initCompanyCache, upsertCompanyRecord, upsertDateEntry } from '../services/companyStore'

export const UNIFIED_DATE = '2025-12-05'
const BASE = import.meta.env.VITE_BIYING_API_BASE ?? 'https://api.biyingapi.com/hslt/ztgc'

export async function fetchLimitUpList(date: string): Promise<LimitUpItem[]> {
  const license = resolveLicense()
  if (!license) throw new Error('缺少 VITE_BIYING_LICENSE 环境变量或 URL 参数 ?license')
  const url = `${BASE}/${date}/${license}`
  const data = await get<LimitUpItem[]>(url)
  const list = Array.isArray(data) ? data : []
  try {
    await initCompanyCache()
    for (const item of list) {
      const code = item.dm
      upsertCompanyRecord(code, {})
      if (date) upsertDateEntry(code, date, { list: item })
    }
  } catch {}
  return list
}

