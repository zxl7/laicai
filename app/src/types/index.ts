export interface MarketSentimentData {
  timestamp: string;
  sentiment: 'increasing' | 'decreasing' | 'oscillating';
  sentimentScore: number; // 0-100
  limitUpCount: number;
  limitDownCount: number;
  trendDirection: 'up' | 'down' | 'flat';
}

export interface SectorSentimentData {
  sectorCode: string;
  sectorName: string;
  limitUpCount: number;
  limitDownCount: number;
  sentiment: 'increasing' | 'decreasing' | 'oscillating';
  trendDirection: 'up' | 'down' | 'flat';
  isLeading?: boolean; // 主升板块
  isDeclining?: boolean; // 退潮板块
}

export interface SentimentTrendData {
  timestamp: string;
  limitUpCount: number;
  limitDownCount: number;
  sentimentScore: number;
}