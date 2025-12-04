# 市场情绪面板

一个实时监控A股市场情绪状态和板块情绪变化的金融数据可视化平台。

## 功能特性

### 🎯 核心功能
- **市场情绪监控面板**: 实时情绪指标、涨跌停统计、趋势图表
- **板块情绪矩阵**: 主升板块识别、退潮板块警示、板块趋势分析
- **用户认证系统**: 支持访客访问和用户注册登录
- **实时数据更新**: 通过Supabase实时订阅实现数据自动刷新

### 🎨 视觉设计
- **深色主题**: 专业的金融数据展示界面
- **渐变背景**: 根据情绪分数动态调整颜色
- **动画效果**: 主升板块金色脉冲边框、退潮板块红色闪烁警示
- **响应式设计**: 支持桌面端、平板端和移动端

### 📊 数据指标
- **情绪指数**: 0-100分量化市场情绪强度
- **涨跌停统计**: 实时涨停/跌停家数变化
- **板块识别**: 自动识别涨停个股≥3的板块为主升板块
- **趋势判断**: 基于连续数据点判断递增/递减/震荡趋势

## 技术栈

- **前端**: React 18 + TypeScript + Vite
- **样式**: Tailwind CSS
- **图表**: Chart.js + React Chart.js 2
- **后端**: Supabase (BaaS)
- **数据库**: PostgreSQL
- **实时通信**: Supabase实时订阅
- **状态管理**: React Context + useReducer
- **图标**: Lucide React

## 项目结构

```
src/
├── components/          # 可复用组件
│   ├── SentimentCard.tsx           # 情绪指标卡片
│   ├── SentimentTrendChart.tsx     # 趋势图表组件
│   ├── SectorCard.tsx              # 板块卡片组件
│   ├── Navigation.tsx               # 导航栏组件
│   └── MarketSentimentDashboard.tsx # 情绪仪表板
├── hooks/               # 自定义Hooks
│   ├── useSentimentData.ts        # 市场情绪数据Hook
│   └── useAuth.ts                   # 用户认证Hook
├── lib/                 # 工具库
│   ├── supabase.ts                  # Supabase客户端配置
│   └── utils.ts                     # 工具函数
├── pages/               # 页面组件
│   ├── Home.tsx                     # 市场情绪面板首页
│   ├── Sectors.tsx                  # 板块情绪矩阵页面
│   └── Login.tsx                    # 用户登录页面
├── types/               # TypeScript类型定义
└── utils/               # 工具函数和模拟数据

## 快速开始

### 安装依赖
```bash
npm install
```

### 配置环境变量
在根目录创建 `.env` 文件：
```env
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key
```

### 启动开发服务器
```bash
npm run dev
```

### 构建生产版本
```bash
npm run build
```

## 数据模型

### 市场情绪表 (market_sentiment)
- `id`: UUID主键
- `sentiment_score`: 情绪分数 (0-100)
- `trend_direction`: 趋势方向 (up/down/sideways)
- `limit_up_count`: 涨停家数
- `limit_down_count`: 跌停家数
- `timestamp`: 时间戳

### 板块表 (sectors)
- `id`: UUID主键
- `name`: 板块名称
- `code`: 板块代码
- `limit_up_stocks`: 涨停个股数
- `limit_down_stocks`: 跌停个股数
- `trend_direction`: 趋势方向
- `is_rising`: 是否主升板块
- `is_falling`: 是否退潮板块

## 核心算法

### 情绪分数计算
```
情绪分数 = (涨停家数 - 跌停家数) / 总交易股票数 * 100 + 50
```

### 趋势判断规则
- **递增**: 连续3个时间点分数上升
- **递减**: 连续3个时间点分数下降
- **震荡**: 其他情况

### 板块识别规则
- **主升板块**: 涨停个股数 ≥ 3且趋势向上
- **退潮板块**: 跌停个股数 ≥ 3且趋势向下

## 用户权限

### 访客用户
- ✅ 查看基础市场情绪数据
- ✅ 查看板块情绪矩阵
- ❌ 无法收藏板块
- ❌ 无法设置提醒

### 注册用户
- ✅ 查看完整数据
- ✅ 收藏关注的板块
- ✅ 设置个性化提醒
- ✅ 自定义数据展示

## 部署

### Vercel部署
1. 连接GitHub仓库
2. 配置环境变量
3. 自动部署

### 其他平台
支持任何支持静态网站托管的平台

## 许可证

MIT License

## 联系方式

如有问题或建议，欢迎提交Issue或Pull Request。