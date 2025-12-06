import type { CompanyProfile, LimitUpItem } from '../api/types'
import { fetchCompanyProfile } from '../api/company'
/**
 * 股票池本地缓存（扁平结构）
 * 设计目标：
 * - 仅在前端本地维护公司池数据，不写入后端/文件
 * - 兼容旧版 `dates` 结构，初始化时自动提取最新数据为扁平 `list`
 * - 提供读取、补全公司详情、增量更新（list/profile）的能力
 */

export type CompanyRecord = {
  code: string
  list?: LimitUpItem
  trades?: unknown
  lastUpdated?: string
} & Partial<CompanyProfile>
/**
 * 股票池存储结构：键为公司代码，值为该公司最新的聚合数据
 */
export type Store = Record<string, CompanyRecord>

const LS_KEY = 'COMPANY_CACHE_V1'
let inited = false
/**
 * 说明：
 * - LS_KEY 为本地存储键名
 * - inited 用于避免重复初始化读取
 */

function readLocal(): Store {
  const raw = localStorage.getItem(LS_KEY)
  return raw ? JSON.parse(raw) : {}
}
/**
 * 将股票池写入本地存储（JSON 序列化）
 */
function writeLocal(store: Store) {
  localStorage.setItem(LS_KEY, JSON.stringify(store))
}

export async function initCompanyCache(): Promise<void> {
  if (inited) return
  const res = await fetch('/company-cache.json')
  if (res.ok) {
    const fileStore = (await res.json()) as Store
    writeLocal(fileStore)
  }
  inited = true
}
/**
 * 获取单个公司记录
 */
export function getCompanyRecord(code: string): CompanyRecord | undefined {
  const s = readLocal()
  return s[code]
}
/**
 * 获取当前股票池（全部公司）
 */
export function getCompanyCache(): Store {
  return readLocal()
}

export const getCompanyPool = getCompanyCache

export async function enrichMissingProfiles(): Promise<void> {
  const s = getCompanyCache()
  const codes = Object.keys(s).filter(code => !s[code].name)
  for (const code of codes) {
    const list = await fetchCompanyProfile(code)
    if (Array.isArray(list) && list[0]) {
      upsertCompanyRecord(code, { ...list[0] })
    }
  }
}
/**
 * 更新/插入公司记录（增量合并），并写入最近更新时间戳
 */
export function upsertCompanyRecord(code: string, payload: Partial<CompanyRecord>): CompanyRecord {
  const s = readLocal()
  const prev = s[code] || { code }
  const next: CompanyRecord = {
    ...prev,
    ...payload,
    code,
    lastUpdated: new Date().toISOString(),
  }
  s[code] = next
  writeLocal(s)
  return next
}
/**
 * 写入最新的涨停池条目 `list`
 */
export function upsertList(code: string, list: LimitUpItem): CompanyRecord {
  return upsertCompanyRecord(code, { list })
}

// 导出功能已移除，保留控制台打印股票池

export const COMPANY_CACHE_UPDATE_EVENT = 'company-cache:update'

export function updateCompanyCache(input: Record<string, Partial<CompanyRecord>>): Store {
  if (!input || typeof input !== 'object' || Array.isArray(input)) {
    return getCompanyCache()
  }
  const s = readLocal()
  for (const [code, rec] of Object.entries(input)) {
    const prev = s[code] || { code }
    const next: CompanyRecord = {
      ...prev,
      ...rec,
      code,
      lastUpdated: new Date().toISOString()
    }
    s[code] = next
  }
  writeLocal(s)
  // eslint-disable-next-line no-console
  console.log('股票池', s)
  return s
}

export function registerCompanyCacheEvent(): void {
  if (typeof window === 'undefined') return
  window.addEventListener(COMPANY_CACHE_UPDATE_EVENT, (e: Event) => {
    const detail = (e as CustomEvent).detail
    if (detail && typeof detail === 'object' && !Array.isArray(detail)) {
      updateCompanyCache(detail as Record<string, Partial<CompanyRecord>>)
    }
  })
}
