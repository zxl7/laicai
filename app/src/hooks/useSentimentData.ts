import { useState, useEffect } from 'react'
import { MarketSentiment, Sector } from '../types'

export function useMarketSentiment() {
  const [sentiment, setSentiment] = useState<MarketSentiment | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    // 暂停后端依赖，保留占位逻辑以便前端继续工作
    setLoading(false)
  }, [])

  const fetchMarketSentiment = async () => {
    // 已移除数据库读取，返回占位数据
    setSentiment(null)
    setError(null)
  }

  return { sentiment, loading, error }
}

export function useSectors() {
  const [sectors, setSectors] = useState<Sector[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    setLoading(false)
  }, [])

  const fetchSectors = async () => {
    setSectors([])
    setError(null)
  }

  return { sectors, loading, error }
}
