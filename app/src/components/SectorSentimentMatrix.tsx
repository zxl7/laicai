import React from 'react';
import { Card, Row, Col, Tag, Badge } from 'antd';
import { RiseOutlined, FallOutlined } from '@ant-design/icons';
import { SectorSentimentData } from '../types';

interface SectorSentimentMatrixProps {
  data: SectorSentimentData[];
  loading: boolean;
}

const SectorSentimentMatrix: React.FC<SectorSentimentMatrixProps> = ({ data, loading }) => {
  if (loading) {
    return (
      <Card title="板块情绪矩阵" className="backdrop-blur-sm bg-white/80 shadow-lg">
        <Row gutter={[16, 16]}>
          {[...Array(8)].map((_, i) => (
            <Col span={6} key={i}>
              <Card className="animate-pulse">
                <div className="h-24 bg-gray-200 rounded"></div>
              </Card>
            </Col>
          ))}
        </Row>
      </Card>
    );
  }

  const leadingSectors = data.filter(sector => sector.isLeading);
  const decliningSectors = data.filter(sector => sector.isDeclining);
  const normalSectors = data.filter(sector => !sector.isLeading && !sector.isDeclining);

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

  const getSentimentBg = (sentiment: string) => {
    switch (sentiment) {
      case 'increasing':
        return 'bg-increase-green-100';
      case 'decreasing':
        return 'bg-decrease-red-100';
      case 'oscillating':
        return 'bg-gray-100';
      default:
        return 'bg-gray-50';
    }
  };

  const getSentimentText = (sentiment: string) => {
    switch (sentiment) {
      case 'increasing':
        return '递增';
      case 'decreasing':
        return '递减';
      case 'oscillating':