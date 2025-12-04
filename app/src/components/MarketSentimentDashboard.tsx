import React from 'react';
import { Card, Row, Col, Statistic } from 'antd';
import { ArrowUpOutlined, ArrowDownOutlined, MinusOutlined } from '@ant-design/icons';
import { MarketSentimentData } from '../types';

interface MarketSentimentDashboardProps {
  data: MarketSentimentData | null;
  loading: boolean;
}

const MarketSentimentDashboard: React.FC<MarketSentimentDashboardProps> = ({ data, loading }) => {
  if (loading || !data) {
    return (
      <Row gutter={16}>
        {[...Array(4)].map((_, i) => (
          <Col span={6} key={i}>
            <Card className="animate-pulse">
              <div className="h-20 bg-gray-200 rounded"></div>
            </Card>
          </Col>
        ))}
      </Row>
    );
  }

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case 'increasing':
        return 'text-increase-green-400';
      case 'decreasing':
        return 'text-decrease-red-400';
      case 'oscillating':
        return 'text-oscillation-gray';
      default:
        return 'text-gray-500';
    }
  };

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'up':
        return <ArrowUpOutlined className="text-increase-green-400" />;
      case 'down':
        return <ArrowDownOutlined className="text-decrease-red-400" />;
      case 'flat':
        return <MinusOutlined className="text-oscillation-gray" />;
      default:
        return null;
    }
  };

  const getSentimentText = (sentiment: string) => {
    switch (sentiment) {
      case 'increasing':
        return '递增';
      case 'decreasing':
        return '递减';
      case 'oscillating':
        return '震荡';
      default:
        return '未知';
    }
  };

  return (
    <Row gutter={16}>
      <Col span={6}>
        <Card className="h-full backdrop-blur-sm bg-white/80 shadow-lg border border-white/20 hover:shadow-xl transition-shadow duration-300">
          <div className="text-center">
            <div className="text-sm text-gray-600 mb-2">市场情绪</div>
            <div className={`text-2xl font-bold ${getSentimentColor(data.sentiment)}`}>
              {getSentimentText(data.sentiment)}
            </div>
            <div className="flex justify-center mt-2 text-2xl">
              {getTrendIcon(data.trendDirection)}
            </div>
          </div>
        </Card>
      </Col>
      
      <Col span={6}>
        <Card className="h-full backdrop-blur-sm bg-white/80 shadow-lg border border-white/20 hover:shadow-xl transition-shadow duration-300">
          <div className="text-center">
            <div className="text-sm text-gray-600 mb-2">情绪强度</div>
            <div className="text-2xl font-bold text-gold">
              {data.sentimentScore}
            </div>
            <div className="text-xs text-gray-500 mt-1">满分100</div>
          </div>
        </Card>
      </Col>
      
      <Col span={6}>
        <Card className="h-full backdrop-blur-sm bg-white/80 shadow-lg border border-white/20 hover:shadow-xl transition-shadow duration-300">
          <div className="text-center">
            <div className="text-sm text-gray-600 mb-2">涨停家数</div>
            <div className="text-2xl font-bold text-increase-green-400">
              {data.limitUpCount}
            </div>
            <div className="text-xs text-gray-500 mt-1">只个股</div>
          </div>
        </Card>
      </Col>
      
      <Col span={6}>
        <Card className="h-full backdrop-blur-sm bg-white/80 shadow-lg border border-white/20 hover:shadow-xl transition-shadow duration-300">
          <div className="text-center">
            <div className="text-sm text-gray-600 mb-2">跌停家数</div>
            <div className="text-2xl font-bold text-decrease-red-400">
              {data.limitDownCount}
            </div>
            <div className="text-xs text-gray-500 mt-1">只个股</div>
          </div>
        </Card>
      </Col>
    </Row>
  );
};

export default MarketSentimentDashboard;