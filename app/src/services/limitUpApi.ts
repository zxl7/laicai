import type { LimitUpItem } from '../types/biying'

const BASE = import.meta.env.VITE_BIYING_API_BASE ?? 'https://api.biyingapi.com/hslt/ztgc'

export function getStoredLicense(): string | null {
  const fromEnv = import.meta.env.VITE_BIYING_LICENSE as string | undefined
  if (fromEnv && fromEnv.trim()) return fromEnv.trim()
  try {
    const fromLocal = localStorage.getItem('BIYING_LICENSE')
    if (fromLocal && fromLocal.trim()) return fromLocal.trim()
  } catch {}
  return null
}

export function setStoredLicense(license: string) {
  try {
    localStorage.setItem('BIYING_LICENSE', license.trim())
  } catch {}
}

function resolveLicense(): string | null {
  const envOrLocal = getStoredLicense()
  if (envOrLocal) return envOrLocal
  try {
    const url = new URL(window.location.href)
    const q = url.searchParams.get('license')
    if (q && q.trim()) {
      setStoredLicense(q.trim())
      return q.trim()
    }
  } catch {}
  return null
}

export function getTodayDateStr(): string {
  const now = new Date()
  const y = now.getFullYear()
  const m = String(now.getMonth() + 1).padStart(2, '0')
  const d = String(now.getDate()).padStart(2, '0')
  return `${y}-${m}-${d}`
}

export const EARLIEST_DATE = '2019-11-28'

export async function fetchLimitUpList(date: string): Promise<LimitUpItem[]> {
  const license = resolveLicense()
  if (!license) throw new Error('缺少 VITE_BIYING_LICENSE 环境变量或 URL 参数 ?license')
  const url = `${BASE}/${date}/${license}`
  const res = await fetch(url)
  if (!res.ok) {
    throw new Error(`请求失败: ${res.status}`)
  }
  const data = await res.json()
  return Array.isArray(data) ? data as LimitUpItem[] : []
}

export function formatCurrency(n: number): string {
  if (n == null) return '-'
  // 显示为亿元/万元单位更易读
  if (n >= 1e8) return `${(n / 1e8).toFixed(2)}亿`
  if (n >= 1e4) return `${(n / 1e4).toFixed(2)}万`
  return n.toFixed(2)
}

export function formatPercent(n: number): string {
  if (n == null) return '-'
  return `${n.toFixed(2)}%`
}
