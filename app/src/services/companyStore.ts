import type { CompanyProfile, LimitUpItem } from '../api/types'

export type CompanyRecord = {
  code: string
  profile?: CompanyProfile
  list?: LimitUpItem
  trades?: unknown
  lastUpdated?: string
}

export type Store = Record<string, CompanyRecord>

const LS_KEY = 'COMPANY_CACHE_V1'
let inited = false

function readLocal(): Store {
  try {
    const raw = localStorage.getItem(LS_KEY)
    return raw ? JSON.parse(raw) : {}
  } catch {
    return {}
  }
}

function writeLocal(store: Store) {
  try {
    localStorage.setItem(LS_KEY, JSON.stringify(store))
  } catch {}
}

export async function initCompanyCache(): Promise<void> {
  if (inited) return
  const current = readLocal()
  try {
    const res = await fetch('/company-cache.json')
    if (res.ok) {
      const fileStore = (await res.json()) as any
      const normalized: Store = {}
      for (const [code, rec] of Object.entries(fileStore as Record<string, any>)) {
        const next: CompanyRecord = { code }
        if (rec.profile) next.profile = rec.profile
        // 兼容旧结构：从 dates 中提取最新 list
        if (rec.dates && typeof rec.dates === 'object') {
          const dates = Object.keys(rec.dates as Record<string, any>)
          dates.sort()
          const latest = dates[dates.length - 1]
          const latestEntry = latest ? rec.dates[latest] : null
          if (latestEntry && latestEntry.list) next.list = latestEntry.list as LimitUpItem
        }
        if (rec.list) next.list = rec.list as LimitUpItem
        if (rec.trades) next.trades = rec.trades
        if (rec.lastUpdated) next.lastUpdated = rec.lastUpdated
        normalized[code] = next
      }
      const merged = { ...normalized, ...current }
      writeLocal(merged)
    }
  } catch {}
  inited = true
}

export function getCompanyRecord(code: string): CompanyRecord | undefined {
  const s = readLocal()
  return s[code]
}

export function getCompanyCache(): Store {
  return readLocal()
}

export const getCompanyPool = getCompanyCache

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

export function upsertList(code: string, list: LimitUpItem): CompanyRecord {
  return upsertCompanyRecord(code, { list })
}

export function exportCompanyCache(): void {
  const s = readLocal()
  const blob = new Blob([JSON.stringify(s, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'company-cache.json'
  document.body.appendChild(a)
  a.click()
  a.remove()
  URL.revokeObjectURL(url)
}
