-- 创建市场情绪表
CREATE TABLE market_sentiment (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    sentiment_score INTEGER CHECK (sentiment_score >= 0 AND sentiment_score <= 100),
    trend_direction VARCHAR(10) CHECK (trend_direction IN ('up', 'down', 'sideways')),
    limit_up_count INTEGER DEFAULT 0,
    limit_down_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 创建板块表
CREATE TABLE sectors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) UNIQUE NOT NULL,
    limit_up_stocks INTEGER DEFAULT 0,
    limit_down_stocks INTEGER DEFAULT 0,
    trend_direction VARCHAR(10) CHECK (trend_direction IN ('up', 'down', 'sideways')),
    is_rising BOOLEAN DEFAULT FALSE,
    is_falling BOOLEAN DEFAULT FALSE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 创建情绪历史表
CREATE TABLE sentiment_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sentiment_id UUID REFERENCES market_sentiment(id) ON DELETE CASCADE,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    score INTEGER,
    limit_up INTEGER,
    limit_down INTEGER
);

-- 创建用户偏好表
CREATE TABLE user_preference (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    favorite_sectors JSON DEFAULT '[]',
    alert_settings JSON DEFAULT '{}',
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 创建索引
CREATE INDEX idx_market_sentiment_timestamp ON market_sentiment(timestamp DESC);
CREATE INDEX idx_market_sentiment_trend ON market_sentiment(trend_direction);
CREATE INDEX idx_sectors_trend ON sectors(trend_direction);
CREATE INDEX idx_sectors_rising ON sectors(is_rising);
CREATE INDEX idx_sectors_falling ON sectors(is_falling);
CREATE INDEX idx_sentiment_history_sentiment_id ON sentiment_history(sentiment_id);
CREATE INDEX idx_user_preference_user_id ON user_preference(user_id);

-- 设置行级安全策略
ALTER TABLE market_sentiment ENABLE ROW LEVEL SECURITY;
ALTER TABLE sectors ENABLE ROW LEVEL SECURITY;
ALTER TABLE sentiment_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_preference ENABLE ROW LEVEL SECURITY;

-- 创建策略
CREATE POLICY "Allow read access to market sentiment" ON market_sentiment FOR SELECT TO anon, authenticated USING (true);
CREATE POLICY "Allow read access to sectors" ON sectors FOR SELECT TO anon, authenticated USING (true);
CREATE POLICY "Allow read access to sentiment history" ON sentiment_history FOR SELECT TO anon, authenticated USING (true);
CREATE POLICY "Allow full access to user preference for authenticated users" ON user_preference FOR ALL TO authenticated USING (auth.uid() = user_id);