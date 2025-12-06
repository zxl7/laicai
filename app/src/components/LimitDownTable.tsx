import type { LimitDownItem, CompanyProfile } from '../api/types'
import { formatCurrency, formatPercent } from '../api/utils'
import { useEffect, useState } from 'react'
import { fetchCompanyProfile } from '../api/company'
import { getCompanyCache, updateCompanyCache, getCompanyRecord } from '../services/companyStore'
import { CompanyProfileCard } from './CompanyProfileCard'
import { Tag, Table, Modal, Button, Tooltip } from 'antd'
import type { TableColumnsType } from 'antd'
import { resolveTagColor } from '../lib/tagColors'

interface Props {
  data: LimitDownItem[]
  loading?: boolean
  onRefresh?: () => void
  date?: string
}

export function LimitDownTable({ data, loading, onRefresh, date }: Props) {
  const [cachingCode, setCachingCode] = useState<string | null>(null)
  const [detailOpen, setDetailOpen] = useState(false)
  const [detailProfile, setDetailProfile] = useState<CompanyProfile | null>(null)

  useEffect(() => {
    console.log('股票池-跌停', getCompanyCache())
  }, [data])

  const handleFetchDetail = async (item: LimitDownItem) => {
    const local = getCompanyRecord(item.dm)
    if (local && local.name) {
      setDetailProfile(local as unknown as CompanyProfile)
      setDetailOpen(true)
      return
    }
    setCachingCode(item.dm)
    const profiles = await fetchCompanyProfile(item.dm)
    const profile = profiles[0] || null
    if (!profile) throw new Error('公司简介为空')
    const payload = {
      [item.dm]: {
        code: item.dm,
        list: item as any,
        lastUpdated: new Date().toISOString(),
        ...profile
      }
    }
    updateCompanyCache(payload)
    setDetailProfile(profile)
    setDetailOpen(true)
    setCachingCode(null)
    console.log('股票池-跌停', getCompanyCache())
  }

  const columns: TableColumnsType<LimitDownItem> = [
    { title: '代码', dataIndex: 'dm', key: 'dm', render: (dm: string) => <span className="font-mono text-white">{dm}</span> },
    { title: '名称', dataIndex: 'mc', key: 'mc', render: (mc: string) => <span className="text-slate-200">{mc}</span> },
    { title: '价格', dataIndex: 'p', key: 'p', render: (p?: number) => <span className="text-slate-200">{p != null ? p.toFixed(2) : '-'}</span> },
    { title: '跌幅', dataIndex: 'zf', key: 'zf', render: (zf: number) => (
      <span className={`font-medium ${zf >= 0 ? 'text-red-400' : 'text-green-400'}`}>{formatPercent(zf)}</span>
    ) },
    { title: '成交额', dataIndex: 'cje', key: 'cje', render: (v: number) => <span className="text-slate-200">{formatCurrency(v)}</span> },
    { title: '流通市值', dataIndex: 'lt', key: 'lt', render: (v: number) => <span className="text-slate-200">{formatCurrency(v)}</span> },
    { title: '总市值', dataIndex: 'zsz', key: 'zsz', render: (v: number) => <span className="text-slate-200">{formatCurrency(v)}</span> },
    { title: '动态市盈率', dataIndex: 'pe', key: 'pe', render: (v: number) => <span className="text-slate-200">{v != null ? v.toFixed(2) : '-'}</span> },
    { title: '换手率', dataIndex: 'hs', key: 'hs', render: (v: number) => <span className="text-slate-200">{formatPercent(v)}</span> },
    { title: '连续跌停', dataIndex: 'lbc', key: 'lbc', render: (v: number) => <span className={`text-slate-200 ${v >= 3 ? 'text-amber-400' : ''}`}>{v}</span> },
    { title: '最后封板时间', dataIndex: 'lbt', key: 'lbt', render: (v: string) => <span className="text-slate-200">{v}</span> },
    { title: '封单资金', dataIndex: 'zj', key: 'zj', sorter: (a, b) => a.zj - b.zj, defaultSortOrder: 'ascend', render: (v: number) => <span className="text-slate-200">{formatCurrency(v)}</span> },
    { title: '板上成交额', dataIndex: 'fba', key: 'fba', render: (v: number) => <span className="text-slate-200">{formatCurrency(v)}</span> },
    { title: '开板次数', dataIndex: 'zbc', key: 'zbc', render: (v: number) => <span className="text-slate-200">{v}</span> },
    { title: '概念', key: 'idea', render: (_: unknown, item: LimitDownItem) => {
      const rec = getCompanyRecord(item.dm)
      const tags = (rec?.idea || '').split(',').map(s => s.trim()).filter(Boolean)
      if (tags.length === 0) return <span className="text-slate-500 text-xs">-</span>
      const firstTwo = tags.slice(0, 2)
      return (
        <Tooltip color="var(--tooltip-bg)" title={<div className="flex flex-wrap gap-2">{tags.map(t => (<Tag key={t} className="m-0" color={resolveTagColor(t)}>{t}</Tag>))}</div>}>
          <div className="flex flex-wrap gap-2">
            {firstTwo.map(t => (
              <Tag key={t} className="m-0" color={resolveTagColor(t)}>{t}</Tag>
            ))}
            {tags.length > 2 && (
              <span className="text-slate-500 text-xs">+{tags.length - 2}</span>
            )}
          </div>
        </Tooltip>
      )
    } },
    { title: '详情', key: 'action', fixed: 'right', width: 120, render: (_: unknown, item: LimitDownItem) => (
      <Button size="small" type="default" onClick={() => handleFetchDetail(item)} disabled={cachingCode === item.dm}>
        {cachingCode === item.dm ? '查询中…' : '查看详情'}
      </Button>
    ) },
  ]

  return (
    <div className="bg-[var(--bg-container-50)] backdrop-blur-sm rounded-xl border border-[var(--border)] overflow-hidden">
      <div className="flex items-center justify-between px-6 py-4 border-b border-[var(--border)]">
        <div>
          <h3 className="text-lg font-semibold text-white">跌停股池</h3>
          <p className="text-xs text-slate-400">{date ? `日期：${date}` : ''}（每10分钟更新）</p>
        </div>
        <Button onClick={onRefresh} disabled={!!loading} size="small" type="primary">刷新</Button>
      </div>

      <Table
        dataSource={data}
        columns={columns}
        rowKey={(item) => `${item.dm}-${item.lbt}`}
        loading={!!loading}
        pagination={false}
        scroll={{ x: 'max-content', y: '70vh' }}
        sticky
        locale={{ emptyText: '暂无数据' }}
      />

      <Modal title="公司详情" open={detailOpen && !!detailProfile} onCancel={() => { setDetailOpen(false); setDetailProfile(null) }} footer={null} width={800}>
        {detailProfile && (
          <div className="space-y-4">
            <CompanyProfileCard profile={detailProfile} />
            <pre className="bg-[var(--bg-container-60)] text-slate-200 text-xs rounded-lg p-3 overflow-auto max-h-[40vh]">{JSON.stringify(detailProfile, null, 2)}</pre>
          </div>
        )}
      </Modal>
    </div>
  )
}

