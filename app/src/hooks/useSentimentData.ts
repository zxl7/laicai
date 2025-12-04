import { useState, useEffect } from 'react'
import { supabase } from '../lib/supabase'
import { MarketSentiment, Sector } from '../types'

export function useMarketSentiment() {
  const [sentiment, setSentiment] = useState<MarketSentiment | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchMarketSentiment()
    
    // 设置实时订阅
    const subscription = supabase
      .channel('market_sentiment_changes')
      .on('postgres_changes', { event: '*', schema: 'public', table: 'market_sentiment' }, () => {
        fetchMarketSentiment()
      })
      .subscribe()

    return () => {
      subscription.unsubscribe()
    }
  }, [])

  const fetchMarketSentiment = async () => {
    try {
      setLoading(true)
      const { data, error } = await supabase
        .from('market_sentiment')
        .select('*')
        .order('timestamp', { ascending: false })
        .limit(1)
        .single()

      if (error) throw error
      setSentiment(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch market sentiment')
    } finally {
      setLoading(false)
    }
  }

  return { sentiment, loading, error }
}

export function useSectors() {
  const [sectors, setSectors] = useState<Sector[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchSectors()
    
    // 设置实时订阅
    const subscription = supabase
      .channel('sectors_changes')
      .on('postgres_changes', { event: '*', schema: 'public', table: 'sectors' }, () => {
        fetchSectors()
      })
      .subscribe()

    return () => {
      subscription.unsubscribe()
    }
  }, [])

  const fetchSectors = async () => {
    try {
      setLoading(true)
      const { data, error } = await supabase
        .from('sectors')
        .select('*')
        .order('updated_at', { ascending: false })

      if (error) throw error
      setSectors(data || [])
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch sectors')
    } finally {
      setLoading(false)
    }
  }

  return { sectors, loading, error }
}