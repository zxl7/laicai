import { useState, useEffect } from 'react';
import { MarketSentimentData, SectorSentimentData, SentimentTrendData } from '../types';
import { mockApi } from '../utils/mockData';

export const useMarketSentiment = () => {
  const [data, setData] = useState<MarketSentimentData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    try {
      setLoading(true);
      const result = await mockApi.getMarketSentiment();
      setData(result);
      setError(null);
    } catch (err) {
      setError('获取市场情绪数据失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 30000); // 每30秒更新一次
    return () => clearInterval(interval);
  }, []);

  return { data, loading, error, refetch: fetchData };
};

export const useSectorSentiment = () => {
  const [data, setData] = useState<SectorSentimentData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    try {
      setLoading(true);
      const result = await mockApi.getSectorSentiment();
      setData(result);
      setError(null);
    } catch (err) {
      setError('获取板块情绪数据失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 60000); // 每分钟更新一次
    return () => clearInterval(interval);
  }, []);

  return { data, loading, error, refetch: fetchData };
};

export const useTrendData = () => {
  const [data, setData] = useState<SentimentTrendData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    try {
      setLoading(true);
      const result = await mockApi.getTrendData();
      setData(result);
      setError(null);
    } catch (err) {
      setError('获取趋势数据失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 120000); // 每2分钟更新一次
    return () => clearInterval(interval);
  }, []);

  return { data, loading, error, refetch: fetchData };
};