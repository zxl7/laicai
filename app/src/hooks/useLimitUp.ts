import { useEffect, useState, useCallback } from 'react'
import { fetchLimitUpList, UNIFIED_DATE } from '../api/limitup'
import type { LimitUpItem } from '../api/types'

export function useLimitUpList(date?: string) {
  const [data, setData] = useState<LimitUpItem[]>([])
  const [loading, setLoading] = useState<boolean>(false)
  const [error, setError] = useState<string | null>(null)
  const targetDate = date ?? UNIFIED_DATE

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    const list = await fetchLimitUpList(targetDate)
    setData(list)
    setLoading(false)
  }, [targetDate])

  useEffect(() => {
    load()
    const id = setInterval(load, 10 * 60 * 1000) // 每10分钟刷新
    return () => clearInterval(id)
  }, [load])

  return { data, loading, error, refresh: load, date: targetDate }
}
