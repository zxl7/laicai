import { useState } from 'react'
import { useAuth } from '../hooks/useAuth'
import { Link, useNavigate } from 'react-router-dom'
import { Mail, Lock, User, ArrowRight } from 'lucide-react'

export function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [isSignUp, setIsSignUp] = useState(false)
  const { signIn, signUp, loading, error } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    const result = isSignUp 
      ? await signUp(email, password)
      : await signIn(email, password)
    
    if (!result.error) {
      navigate('/')
    }
  }

  return (
    <div className="min-h-screen bg-slate-900 flex items-center justify-center px-4">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <h2 className="text-3xl font-bold text-white mb-2">
            {isSignUp ? '注册账户' : '登录账户'}
          </h2>
          <p className="text-slate-400">
            {isSignUp ? '创建新账户开始使用' : '登录查看完整数据'}
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
            <div className="space-y-4">
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-slate-300 mb-2">
                  邮箱地址
                </label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-slate-400" />
                  <input
                    id="email"
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full pl-10 pr-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500"
                    placeholder="请输入邮箱地址"
                  />
                </div>
              </div>

              <div>
                <label htmlFor="password" className="block text-sm font-medium text-slate-300 mb-2">
                  密码
                </label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-slate-400" />
                  <input
                    id="password"
                    type="password"
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full pl-10 pr-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500"
                    placeholder="请输入密码"
                  />
                </div>
              </div>
            </div>

            {error && (
              <div className="mt-4 p-3 bg-red-900/20 border border-red-500/30 rounded-lg text-red-400 text-sm">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full mt-6 bg-amber-500 hover:bg-amber-600 disabled:bg-slate-600 text-white font-medium py-2 px-4 rounded-lg transition-colors flex items-center justify-center"
            >
              {loading ? (
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
              ) : (
                <>
                  {isSignUp ? '注册' : '登录'}
                  <ArrowRight className="ml-2 w-4 h-4" />
                </>
              )}
            </button>
          </div>
        </form>

        <div className="text-center">
          <button
            onClick={() => setIsSignUp(!isSignUp)}
            className="text-amber-400 hover:text-amber-300 text-sm font-medium transition-colors"
          >
            {isSignUp ? '已有账户？立即登录' : '没有账户？立即注册'}
          </button>
        </div>

        <div className="bg-slate-800/30 rounded-lg p-4 border border-slate-700">
          <h3 className="text-white font-medium mb-2 flex items-center">
            <User className="w-4 h-4 mr-2" />
            访客访问
          </h3>
          <p className="text-slate-400 text-sm mb-3">
            无需注册即可查看基础市场情绪数据，但无法使用收藏和提醒功能。
          </p>
          <Link
            to="/"
            className="text-amber-400 hover:text-amber-300 text-sm font-medium transition-colors"
          >
            继续作为访客访问 →
          </Link>
        </div>
      </div>
    </div>
  )
}