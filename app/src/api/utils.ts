export function getStoredLicense(): string | null {
  const fromEnv = import.meta.env.VITE_BIYING_LICENSE as string | undefined
  if (fromEnv && fromEnv.trim()) return fromEnv.trim()
  const fromLocal = localStorage.getItem('BIYING_LICENSE')
  if (fromLocal && fromLocal.trim()) return fromLocal.trim()
  return null
}

export function setStoredLicense(license: string) {
  localStorage.setItem('BIYING_LICENSE', license.trim())
}

export function resolveLicense(): string | null {
  const envOrLocal = getStoredLicense()
  if (envOrLocal) return envOrLocal
  const url = new URL(window.location.href)
  const q = url.searchParams.get('license')
  if (q && q.trim()) {
    setStoredLicense(q.trim())
    return q.trim()
  }
  return null
}

export function formatCurrency(n: number): string {
  if (n == null) return '-'
  if (n >= 1e8) return `${(n / 1e8).toFixed(2)}亿`
  if (n >= 1e4) return `${(n / 1e4).toFixed(2)}万`
  return n.toFixed(2)
}

export function formatPercent(n: number): string {
  if (n == null) return '-'
  return `${n.toFixed(2)}%`
}
