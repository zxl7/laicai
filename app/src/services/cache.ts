/**
 * 本地组合数据缓存
 * 说明：
 * - 使用 `localStorage` 在浏览器端维护“涨/跌停与公司信息的组合数据”快照
 * - 以代码 `code` 为键，避免重复请求，供页面快速读取
 * - 数据结构由 `CombinedStockData` 定义，仅在前端存在，不写入后端
 */
import type { CombinedStockData } from '../types/combined'

const KEY = 'LIMITUP_COMBINED_CACHE_V1'

type CacheMap = Record<string, CombinedStockData> // code -> combined

/**
 * 读取缓存映射
 * 返回：`Record<code, CombinedStockData>`，若不存在则返回空对象
 */
function readCache(): CacheMap {
  const raw = localStorage.getItem(KEY)
  if (!raw) return {}
  const parsed = JSON.parse(raw)
  return parsed ?? {}
}

/**
 * 写入缓存映射
 * 参数：完整的映射对象，会覆盖旧值
 */
function writeCache(map: CacheMap) {
  localStorage.setItem(KEY, JSON.stringify(map))
}

/**
 * 获取指定代码的组合数据
 * @param code 股票代码
 * @returns 命中则返回 `CombinedStockData`，否则 `null`
 */
export function getCombined(code: string): CombinedStockData | null {
  const map = readCache()
  return map[code] || null
}

/**
 * 写入/更新指定代码的组合数据（幂等，覆盖同键）
 * @param data 组合数据（需包含 `code` 字段）
 */
export function setCombined(data: CombinedStockData) {
  const map = readCache()
  map[data.code] = data
  writeCache(map)
}

/**
 * 判断是否存在指定代码的组合数据
 */
export function hasCombined(code: string): boolean {
  return !!getCombined(code)
}
