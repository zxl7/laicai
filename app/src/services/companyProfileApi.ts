import { CompanyProfile } from '../types/company'
import { getStoredLicense } from './limitUpApi'

const BASE = import.meta.env.VITE_COMPANY_API_BASE ?? 'https://api.biyingapi.com/hscp/gsjj'

export async function fetchCompanyProfile(code: string): Promise<CompanyProfile[]> {
  const license = getStoredLicense()
  if (!license) throw new Error('缺少接口Token：请设置 VITE_BIYING_LICENSE 或 URL 参数 ?license')
  const url = `${BASE}/${code}/${license}`
  const res = await fetch(url)
  if (!res.ok) throw new Error(`请求失败: ${res.status}`)
  const data = await res.json()
  return Array.isArray(data) ? data as CompanyProfile[] : []
}

