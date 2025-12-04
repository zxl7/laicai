import { MarketSentimentData, SectorSentimentData, SentimentTrendData } from '../types';

// 生成模拟市场情绪数据
export const generateMarketSentimentData = (): MarketSentimentData => {
  const now = new Date();
  const limitUpCount = Math.floor(Math.random() * 50) + 20;
  const limitDownCount = Math.floor(Math.random() * 30) + 5;
  const sentimentScore = Math.floor(Math.random() * 100);
  
  let sentiment: 'increasing' | 'decreasing' | 'oscillating';
  let trendDirection: 'up' | 'down' | 'flat';
  
  if (sentimentScore > 70) {
    sentiment = 'increasing';
    trendDirection = 'up';
  } else if (sentimentScore < 30) {
    sentiment = 'decreasing';
    trendDirection = 'down';
  } else {
    sentiment = 'oscillating';
    trendDirection = 'flat';
  }
  
  return {
    timestamp: now.toISOString(),
    sentiment,
    sentimentScore,
    limitUpCount,
    limitDownCount,
    trendDirection
  };
};

// 生成模拟板块情绪数据
export const generateSectorSentimentData = (): SectorSentimentData[] => {
  const sectors = [
    { code: 'BK0475', name: '人工智能' },
    { code: 'BK0485', name: '新能源汽车' },
    { code: 'BK0490', name: '半导体' },
    { code: 'BK0500', name: '医药生物' },
    { code: 'BK0510', name: '金融服务' },
    { code: 'BK0520', name: '房地产' },
    { code: 'BK0530', name: '消费电子' },
    { code: 'BK0540', name: '光伏产业' }
  ];
  
  return sectors.map(sector => {
    const limitUpCount = Math.floor(Math.random() * 8);
    const limitDownCount = Math.floor(Math.random() * 6);
    const sentimentScore = Math.floor(Math.random() * 100);
    
    let sentiment: 'increasing' | 'decreasing' | 'oscillating';
    let trendDirection: 'up' | 'down' | 'flat';
    
    if (sentimentScore > 70) {
      sentiment = 'increasing';
      trendDirection = 'up';
    } else if (sentimentScore < 30) {
      sentiment = 'decreasing';
      trendDirection = 'down';
    } else {
      sentiment = 'oscillating';
      trendDirection = 'flat';
    }
    
    return {
      sectorCode: sector.code,
      sectorName: sector.name,
      limitUpCount,
      limitDownCount,
      sentiment,
      trendDirection,
      isLeading: limitUpCount >= 3,
      isDeclining: limitDownCount >= 3
    };
  });
};

// 生成趋势数据
export const generateTrendData = (points: number = 24): SentimentTrendData[] => {
  const data: SentimentTrendData[] = [];
  const now = new Date();
  
  for (let i = points - 1; i >= 0; i--) {
    const time = new Date(now.getTime() - i * 60 * 60 * 1000); // 每小时一个数据点
    const limitUpCount = Math.floor(Math.random() * 50) + 20;
    const limitDownCount = Math.floor(Math.random() * 30) + 5;
    const sentimentScore = Math.floor(Math.random() * 100);
    
    data.push({
      timestamp: time.toISOString(),
      limitUpCount,
      limitDownCount,
      sentimentScore
    });
  }
  
  return data;
};

// 模拟API调用
export const mockApi = {
  getMarketSentiment: async (): Promise<MarketSentimentData> => {
    await new Promise(resolve => setTimeout(resolve, 500)); // 模拟网络延迟
    return generateMarketSentimentData();
  },
  
  getSectorSentiment: async (): Promise<SectorSentimentData[]> => {
    await new Promise(resolve => setTimeout(resolve, 600));
    return generateSectorSentimentData();
  },
  
  getTrendData: async (): Promise<SentimentTrendData[]> => {
    await new Promise(resolve => setTimeout(resolve, 400));
    return generateTrendData();
  }
};