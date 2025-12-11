export interface MarketSentiment {
  id: string
  timestamp: string
  sentiment_score: number
  trend_direction: 'up' | 'down' | 'sideways'
  limit_up_count: number
  limit_down_count: number
  created_at: string
}

export interface Sector {
  id: string
  name: string
  code: string
  limit_up_stocks: number
  rising_stocks: number
  falling_stocks: number
  limit_down_stocks: number
  trend_direction: 'up' | 'down' | 'sideways'
  is_rising: boolean
  is_falling: boolean
  updated_at: string
}

export interface SentimentHistory {
  id: string
  sentiment_id: string
  timestamp: string
  score: number
  limit_up: number
  limit_down: number
}

export interface UserPreference {
  id: string
  user_id: string
  favorite_sectors: string[]
  alert_settings: Record<string, unknown>
  updated_at: string
}