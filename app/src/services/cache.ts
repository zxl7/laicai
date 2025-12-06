import type { CombinedStockData } from '../types/combined'

const KEY = 'LIMITUP_COMBINED_CACHE_V1'

type CacheMap = Record<string, Record<string, CombinedStockData>> // code -> date -> combined

function readCache(): CacheMap {
  try {
    const raw = localStorage.getItem(KEY)
    if (!raw) return {}
    const parsed = JSON.parse(raw)
    return parsed ?? {}
  } catch {
    return {}
  }
}

function writeCache(map: CacheMap) {
  try {
    localStorage.setItem(KEY, JSON.stringify(map))
  } catch {}
}

export function getCombined(code: string, date?: string): CombinedStockData | null {
  const map = readCache()
  const dmap = map[code]
  if (!dmap) return null
  if (date && dmap[date]) return dmap[date]
  // return latest by date
  const dates = Object.keys(dmap)
  if (dates.length === 0) return null
  const latest = dates.sort().pop() as string
  return dmap[latest]
}

export function setCombined(data: CombinedStockData) {
  const map = readCache()
  if (!map[data.code]) map[data.code] = {}
  map[data.code][data.date] = data
  writeCache(map)
}

export function hasCombined(code: string, date?: string): boolean {
  return !!getCombined(code, date)
}

