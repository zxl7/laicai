import type { CompanyProfile, LimitUpItem } from '../api/types'

type DateEntry = {
  list?: LimitUpItem
  trades?: unknown
}

export type CompanyRecord = {
  code: string
  profile?: CompanyProfile
  lastUpdated?: string
  dates?: Record<string, DateEntry>
}

type Store = Record<string, CompanyRecord>

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
      const fileStore = (await res.json()) as Store
      const merged = { ...fileStore, ...current }
      writeLocal(merged)
    }
  } catch {}
  inited = true
}

export function getCompanyRecord(code: string): CompanyRecord | undefined {
  const s = readLocal()
  return s[code]
}

export function upsertCompanyRecord(code: string, payload: Partial<CompanyRecord>): CompanyRecord {
  const s = readLocal()
  const prev = s[code] || { code, dates: {} }
  const next: CompanyRecord = {
    ...prev,
    ...payload,
    code,
    lastUpdated: new Date().toISOString(),
    dates: prev.dates || {}
  }
  s[code] = next
  writeLocal(s)
  return next
}

export function upsertDateEntry(code: string, date: string, payload: Partial<DateEntry>): CompanyRecord {
  const s = readLocal()
  const prev = s[code] || { code, dates: {} }
  const dprev = prev.dates?.[date] || {}
  const dnext: DateEntry = { ...dprev, ...payload }
  const next: CompanyRecord = {
    ...prev,
    dates: { ...(prev.dates || {}), [date]: dnext },
    lastUpdated: new Date().toISOString()
  }
  s[code] = next
  writeLocal(s)
  return next
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
