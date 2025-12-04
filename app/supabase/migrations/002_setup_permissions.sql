-- 匿名用户权限
GRANT SELECT ON market_sentiment TO anon;
GRANT SELECT ON sectors TO anon;
GRANT SELECT ON sentiment_history TO anon;

-- 认证用户权限
GRANT ALL PRIVILEGES ON market_sentiment TO authenticated;
GRANT ALL PRIVILEGES ON sectors TO authenticated;
GRANT ALL PRIVILEGES ON sentiment_history TO authenticated;
GRANT ALL PRIVILEGES ON user_preference TO authenticated;