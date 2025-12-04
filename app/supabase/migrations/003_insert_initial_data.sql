-- 插入初始市场情绪数据
INSERT INTO market_sentiment (sentiment_score, trend_direction, limit_up_count, limit_down_count) VALUES
(65, 'up', 45, 12),
(58, 'up', 38, 15),
(72, 'up', 52, 8),
(45, 'down', 22, 35),
(39, 'down', 18, 42),
(51, 'sideways', 31, 28);

-- 插入初始板块数据
INSERT INTO sectors (name, code, limit_up_stocks, limit_down_stocks, trend_direction, is_rising, is_falling) VALUES
('新能源', 'NEW_ENERGY', 8, 2, 'up', true, false),
('半导体', 'SEMICONDUCTOR', 6, 1, 'up', true, false),
('医药生物', 'PHARMACEUTICAL', 4, 3, 'up', false, false),
('金融服务', 'FINANCIAL', 2, 7, 'down', false, true),
('房地产', 'REAL_ESTATE', 1, 9, 'down', false, true),
('消费电子', 'CONSUMER_ELECTRONICS', 5, 2, 'up', false, false),
('汽车整车', 'AUTOMOBILE', 3, 4, 'sideways', false, false),
('化工', 'CHEMICAL', 2, 5, 'down', false, false),
('电力设备', 'POWER_EQUIPMENT', 7, 1, 'up', true, false),
('通信设备', 'COMMUNICATION', 4, 2, 'up', false, false);