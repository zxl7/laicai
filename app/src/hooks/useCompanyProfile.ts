import { useCallback, useEffect, useState } from 'react'
import { fetchCompanyProfile } from '../api/company'
import type { CompanyProfile } from '../api/types'

export function useCompanyProfile(code?: string) {
  const [data, setData] = useState<CompanyProfile[] | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const load = useCallback(async () => {
    if (!code) return
    try {
      setLoading(true)
      setError(null)
      const res = await fetchCompanyProfile(code)
      setData(res)
    } catch (e) {
      setError(e instanceof Error ? e.message : '加载失败')
    } finally {
      setLoading(false)
    }
  }, [code])

  useEffect(() => {
    load()
  }, [load])

  return { data, loading, error, refresh: load }
}
