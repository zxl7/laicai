import { Link, useLocation } from 'react-router-dom'
import { Activity, Grid3X3, User, LogOut, Download } from 'lucide-react'
import { cn } from '../lib/utils'
import { useAuth } from '../hooks/useAuth'
import { exportCompanyCache } from '../services/companyStore'

/**
 * 顶部导航栏
 * 用途：页面路由切换、用户登录/退出入口（移动端含折叠导航）
 */
export function Navigation() {
  const location = useLocation()
  const { user, signOut, loading } = useAuth()

  /** 主导航项定义 */
  const navItems = [
    { path: '/', label: '市场情绪', icon: Activity },
    { path: '/sectors', label: '板块矩阵', icon: Grid3X3 },
    { path: '/company', label: '公司简介', icon: User }
  ]

  /** 退出登录 */
  const handleSignOut = async () => {
    await signOut()
  }

  return (
    <nav className="bg-slate-900/80 backdrop-blur-sm border-b border-slate-700 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-8">
            <div className="flex-shrink-0">
              <h1 className="text-xl font-bold text-amber-400">市场情绪面板</h1>
            </div>
            <div className="hidden md:block">
              <div className="ml-10 flex items-baseline space-x-4">
                {navItems.map((item) => {
                  const Icon = item.icon
                  const isActive = location.pathname === item.path
                  
                  return (
                    <Link
                      key={item.path}
                      to={item.path}
                      className={cn(
                        'flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium transition-colors',
                        isActive
                          ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                          : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                      )}
                    >
                      <Icon className="w-4 h-4" />
                      <span>{item.label}</span>
                    </Link>
                  )
                })}
              </div>
            </div>
          </div>

          {/* 用户菜单 */}
          <div className="flex items-center space-x-4">
            {user ? (
              <div className="flex items-center space-x-3">
                <div className="text-slate-300 text-sm">
                  {user.email}
                </div>
                <button
                  onClick={exportCompanyCache}
                  className="flex items-center space-x-1 px-3 py-1 rounded-md text-sm text-slate-300 hover:bg-slate-800 hover:text-white transition-colors"
                >
                  <Download className="w-4 h-4" />
                  <span>导出股票池</span>
                </button>
                <button
                  onClick={handleSignOut}
                  disabled={loading}
                  className="flex items-center space-x-1 px-3 py-1 rounded-md text-sm text-slate-300 hover:bg-slate-800 hover:text-white transition-colors"
                >
                  <LogOut className="w-4 h-4" />
                  <span>退出</span>
                </button>
              </div>
            ) : (
              <div className="flex items-center space-x-2">
                <Link
                  to="/login"
                  className={cn(
                    'flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium transition-colors',
                    location.pathname === '/login'
                      ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                      : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                  )}
                >
                  <User className="w-4 h-4" />
                  <span>登录</span>
                </Link>
                <button
                  onClick={exportCompanyCache}
                  className="flex items-center space-x-1 px-3 py-2 rounded-md text-sm text-slate-300 hover:bg-slate-800 hover:text-white transition-colors"
                >
                  <Download className="w-4 h-4" />
                  <span>导出股票池</span>
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
      
      {/* 移动端导航 */}
      <div className="md:hidden border-t border-slate-700">
        <div className="px-2 pt-2 pb-3 space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon
            const isActive = location.pathname === item.path
            
            return (
              <Link
                key={item.path}
                to={item.path}
                className={cn(
                  'flex items-center space-x-3 px-3 py-2 rounded-md text-base font-medium transition-colors',
                  isActive
                    ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                    : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                )}
              >
                <Icon className="w-5 h-5" />
                <span>{item.label}</span>
              </Link>
            )
          })}
          
          {user ? (
            <button
              onClick={handleSignOut}
              disabled={loading}
              className="flex items-center space-x-3 px-3 py-2 rounded-md text-base font-medium text-slate-300 hover:bg-slate-800 hover:text-white transition-colors w-full"
            >
              <LogOut className="w-5 h-5" />
              <span>退出登录</span>
            </button>
          ) : (
            <Link
              to="/login"
              className={cn(
                'flex items-center space-x-3 px-3 py-2 rounded-md text-base font-medium transition-colors',
                location.pathname === '/login'
                  ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                  : 'text-slate-300 hover:bg-slate-800 hover:text-white'
              )}
            >
              <User className="w-5 h-5" />
              <span>登录</span>
            </Link>
          )}
        </div>
      </div>
    </nav>
  )
}
