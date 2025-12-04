// 模拟数据文件 - 用于开发和测试
export const mockMarketData = {
  sentiment_score: 65,
  trend_direction: 'up',
  limit_up_count: 45,
  limit_down_count: 12
}

export const mockSectorData = [
  {
    name: '新能源',
    code: 'NEW_ENERGY',
    limit_up_stocks: 8,
    limit_down_stocks: 2,
    trend_direction: 'up',
    is_rising: true,
    is_falling: false
  },
  {
    name: '半导体',
    code: 'SEMICONDUCTOR',
    limit_up_stocks: 6,
    limit_down_stocks: 1,
    trend_direction: 'up',
    is_rising: true,
    is_falling: false
  },
  {
    name: '金融服务',
    code: 'FINANCIAL',
    limit_up_stocks: 2,
    limit_down_stocks: 7,
    trend_direction: 'down',
    is_rising: false,
    is_falling: true
  }
]