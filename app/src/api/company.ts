import { get } from './client'
import type { CompanyProfile } from './types'
import { getStoredLicense } from './utils'
import { initCompanyCache, upsertCompanyRecord } from '../services/companyStore'

const BASE = import.meta.env.VITE_COMPANY_API_BASE ?? 'https://api.biyingapi.com/hscp/gsjj'

export async function fetchCompanyProfile(code: string): Promise<CompanyProfile[]> {
  const license = getStoredLicense()
  if (!license) throw new Error('缺少接口Token：请设置 VITE_BIYING_LICENSE 或 URL 参数 ?license')
  const url = `${BASE}/${code}/${license}`
  const data = await get<CompanyProfile[]>(url)
  const list = Array.isArray(data) ? data : []
  try {
    await initCompanyCache()
    if (list[0]) {
      upsertCompanyRecord(code, { profile: list[0] })
    } else {
      upsertCompanyRecord(code, {})
    }
  } catch {}
  return list
}

