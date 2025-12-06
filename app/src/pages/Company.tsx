import { useEffect, useMemo, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { useCompanyProfile } from '../hooks/useCompanyProfile'
import { CompanyProfileCard } from '../components/CompanyProfileCard'
import { getStoredLicense, setStoredLicense } from '../services/limitUpApi'

export function Company() {
  const [params, setParams] = useSearchParams()
  const initialCode = params.get('code') || ''
  const [code, setCode] = useState<string>(initialCode)
  const [license, setLicense] = useState<string>(getStoredLicense() || '')
  const { data, loading, error, refresh } = useCompanyProfile(code)

  useEffect(() => {
    if (code) {
      params.set('code', code)
      setParams(params, { replace: true })
    }
  }, [code])

  return (
    <div className="min-h-screen bg-slate-900 text-white p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        <div>
          <h1 className="text-3xl font-bold">公司简介查询</h1>
          <p className="text-slate-400">根据股票代码查询上市公司基本信息、概念与发行信息</p>
        </div>

        <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-4 border border-slate-700">
          <div className="flex flex-col md:flex-row md:items-center md:space-x-3 space-y-3 md:space-y-0">
            <input
              type="text"
              value={code}
              placeholder="输入股票代码，如 000001"
              onChange={(e) => setCode(e.target.value)}
              className="w-full md:w-64 px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500"
            />
            <input
              type="text"
              value={license}
              placeholder="输入API Token"
              onChange={(e) => setLicense(e.target.value)}
              className="w-full md:w-96 px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500"
            />
            <button
              onClick={() => { if (license.trim()) { setStoredLicense(license.trim()); refresh() } }}
              className="px-3 py-2 rounded-md text-sm font-medium bg-slate-700 hover:bg-slate-600 text-slate-200"
            >
              保存Token
            </button>
            <button
              onClick={refresh}
              disabled={loading || !code}
              className="px-3 py-2 rounded-md text-sm font-medium bg-amber-500 hover:bg-amber-600 disabled:bg-slate-600 text-white"
            >
              查询
            </button>
          </div>
          {!license && (
            <div className="mt-3 text-xs text-red-400">未设置Token：请通过URL参数 ?license=... 或在此输入并点击保存</div>
          )}
        </div>

        {error && (
          <div className="bg-red-900/20 border border-red-500/30 rounded-lg p-4 text-red-400">{error}</div>
        )}

        {loading && (
          <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700 animate-pulse">
            <div className="h-6 bg-slate-700 rounded mb-3"></div>
            <div className="h-64 bg-slate-700 rounded"></div>
          </div>
        )}

        {data && data.length > 0 && (
          <CompanyProfileCard profile={data[0]} />
        )}

        {data && data.length === 0 && !loading && (
          <div className="text-slate-400">未查询到该代码的公司信息</div>
        )}
      </div>
    </div>
  )
}

