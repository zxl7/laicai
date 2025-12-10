import { get } from './client'
import type { CompanyProfile } from './types'

/**
 * 获取公司简介信息
 * @param code 股票代码
 * @returns 公司简介信息数组
 */
export async function fetchCompanyProfile(code: string): Promise<CompanyProfile[]> {
  const url = `/api/quote/company-profile/${code}`
  let data = await get<unknown>(url)
  data = (data as any).data

  if (Array.isArray(data)) return data as CompanyProfile[]
  if (data && typeof data === 'object') return [data as CompanyProfile]
  return []
}
