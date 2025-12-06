import type { CombinedStockData } from '../types/combined'

const KEY = 'LIMITUP_COMBINED_CACHE_V1'

type CacheMap = Record<string, CombinedStockData> // code -> combined

function readCache(): CacheMap {
  const raw = localStorage.getItem(KEY)
  if (!raw) return {}
  const parsed = JSON.parse(raw)
  return parsed ?? {}
}

function writeCache(map: CacheMap) {
  localStorage.setItem(KEY, JSON.stringify(map))
}

export function getCombined(code: string): CombinedStockData | null {
  const map = readCache()
  return map[code] || null
}

export function setCombined(data: CombinedStockData) {
  const map = readCache()
  map[data.code] = data
  writeCache(map)
}

export function hasCombined(code: string): boolean {
  return !!getCombined(code)
}
