import { useEffect, useState, useCallback } from 'react'
import { fetchLimitUpList, getTodayDateStr } from '../services/limitUpApi'
import type { LimitUpItem } from '../types/biying'

export function useLimitUpList(date?: string) {
  const [data, setData] = useState<LimitUpItem[]>([])
  const [loading, setLoading] = useState<boolean>(false)
  const [error, setError] = useState<string | null>(null)
  const targetDate = date ?? getTodayDateStr()

  const load = useCallback(async () => {
    try {
      setLoading(true)
      setError(null)
      // const list = await fetchLimitUpList(targetDate)
      const list = await fetchLimitUpList('2025-12-05')
      setData(list)
    } catch (e) {
      setError(e instanceof Error ? e.message : '加载失败')
    } finally {
      setLoading(false)
    }
  }, [targetDate])

  useEffect(() => {
    load()
    const id = setInterval(load, 10 * 60 * 1000) // 每10分钟刷新
    return () => clearInterval(id)
  }, [load])

  return { data, loading, error, refresh: load, date: targetDate }
}

