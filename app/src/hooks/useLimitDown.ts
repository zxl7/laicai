import { useEffect, useState, useCallback } from 'react'
import { fetchLimitDownList, UNIFIED_DATE } from '../api/limitdown'
import { updateCompanyCache } from '../services/companyStore'
import type { LimitDownItem } from '../api/types'

export function useLimitDownList(date?: string) {
  const [data, setData] = useState<LimitDownItem[]>([])
  const [loading, setLoading] = useState<boolean>(false)
  const [error, setError] = useState<string | null>(null)
  const targetDate = date ?? UNIFIED_DATE

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const list = await fetchLimitDownList(targetDate)
      setData(list)
      const payload = Object.fromEntries(list.map(item => [item.dm, { listDown: item, code: item.dm }]))
      updateCompanyCache(payload)
    } catch (e: any) {
      setError(e?.message || '加载失败')
    } finally {
      setLoading(false)
    }
  }, [targetDate])

  useEffect(() => {
    load()
    const id = setInterval(load, 10 * 60 * 1000)
    return () => clearInterval(id)
  }, [load])

  return { data, loading, error, refresh: load, date: targetDate }
}
