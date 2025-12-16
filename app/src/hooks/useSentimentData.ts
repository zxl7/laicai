import { useState, useEffect } from 'react'
import { MarketSentiment, Sector } from '../types'
import { fetchSectors } from '../api/sectors'

export function useMarketSentiment() {
  const [sentiment] = useState<MarketSentiment | null>(null)
  const [loading, setLoading] = useState(true)
  const [error] = useState<string | null>(null)

  useEffect(() => {
    // 暂停后端依赖，保留占位逻辑以便前端继续工作
    setLoading(false)
  }, [])

  return { sentiment, loading, error }
}



export function useSectors() {
  const [sectors, setSectors] = useState<Sector[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchSectorsData = async () => {
    try {
      setLoading(true)
      setError(null)
      
      // 直接从API获取板块数据，绕过缓存
      const sectorsData = await fetchSectors(true)
      setSectors(sectorsData)
    } catch (err) {
      setError('获取板块数据失败')
      console.error('Failed to fetch sectors:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchSectorsData()
  }, [])

  return { sectors, loading, error, refresh: fetchSectorsData }
}
