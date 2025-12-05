-- 删除应用相关的业务数据表（保留 Supabase 认证表）
-- 顺序：先删除依赖表，再删除主表

BEGIN;

DROP TABLE IF EXISTS sentiment_history CASCADE;
DROP TABLE IF EXISTS user_preference CASCADE;
DROP TABLE IF EXISTS market_sentiment CASCADE;
DROP TABLE IF EXISTS sectors CASCADE;

COMMIT;

