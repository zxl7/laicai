import type { LimitUpItem, CompanyProfile } from "../api/types"
import { formatCurrency, formatPercent } from "../api/utils"
import { useEffect, useState } from "react"
import { fetchCompanyProfile } from "../api/company"
import { getCompanyCache, updateCompanyCache, getCompanyRecord } from "../services/companyStore"
import { CompanyProfileCard } from "./CompanyProfileCard"
import { Tag, Table, Modal, Button, Tooltip } from "antd"
import type { TableColumnsType } from "antd"
import { resolveTagColor } from "../lib/tagColors"

/**
 * 涨停股池表格
 * 用途：展示指定日期的涨停股票明细，支持手动刷新与表头固定
 */
interface Props {
  data: LimitUpItem[]
  loading?: boolean
  onRefresh?: () => void
  date?: string
}

/**
 * 表格主组件
 */
export function LimitUpTable({ data, loading, onRefresh, date }: Props) {
  const [cachingCode, setCachingCode] = useState<string | null>(null)
  const [detailOpen, setDetailOpen] = useState(false)
  const [detailProfile, setDetailProfile] = useState<CompanyProfile | null>(null)

  // 打印当前股票池（不进行任何更新）
  useEffect(() => {
    console.log("股票池", getCompanyCache())
  }, [data])

  const handleFetchDetail = async (item: LimitUpItem) => {
    const local = getCompanyRecord(item.dm)
    if (local && local.name) {
      setDetailProfile(local as unknown as CompanyProfile)
      setDetailOpen(true)
      return
    }
    setCachingCode(item.dm)
    const profiles = await fetchCompanyProfile(item.dm)
    const profile = profiles[0] || null
    if (!profile) throw new Error("公司简介为空")
    const payload = {
      [item.dm]: {
        code: item.dm,
        list: item,
        lastUpdated: new Date().toISOString(),
        ...profile,
      },
    }
    updateCompanyCache(payload)
    setDetailProfile(profile)
    setDetailOpen(true)
    setCachingCode(null)
    console.log("股票池", getCompanyCache())
  }
  const toHHMMSS = (val: string) => {
    if (!val && val !== "0") return "-"
    const v = String(val)
    const m = v.match(/(\d{1,2}):(\d{1,2}):(\d{1,2})/)
    if (m) {
      const [, h, mi, s] = m
      return `${h.padStart(2, "0")}:${mi.padStart(2, "0")}:${s.padStart(2, "0")}`
    }
    if (/^\d{6}$/.test(v)) {
      const h = v.slice(0, 2)
      const mi = v.slice(2, 4)
      const s = v.slice(4, 6)
      return `${h}:${mi}:${s}`
    }
    const d = new Date(v)
    if (!isNaN(d.getTime())) {
      const h = `${d.getHours()}`.padStart(2, "0")
      const mi = `${d.getMinutes()}`.padStart(2, "0")
      const s = `${d.getSeconds()}`.padStart(2, "0")
      return `${h}:${mi}:${s}`
    }
    return v
  }
  const toSec = (val: string): number => {
    if (!val && val !== "0") return -1
    const v = String(val)
    const m = v.match(/(\d{1,2}):(\d{1,2}):(\d{1,2})/)
    if (m) {
      const h = Number(m[1]) || 0
      const mi = Number(m[2]) || 0
      const s = Number(m[3]) || 0
      return h * 3600 + mi * 60 + s
    }
    if (/^\d{6}$/.test(v)) {
      const h = Number(v.slice(0, 2)) || 0
      const mi = Number(v.slice(2, 4)) || 0
      const s = Number(v.slice(4, 6)) || 0
      return h * 3600 + mi * 60 + s
    }
    const d = new Date(v)
    if (!isNaN(d.getTime())) return d.getHours() * 3600 + d.getMinutes() * 60 + d.getSeconds()
    return -1
  }
  const columns: TableColumnsType<LimitUpItem> = [
    { title: "名称", dataIndex: "mc", key: "mc", render: (mc: string) => <span className="text-slate-200">{mc}</span> },
    { title: "涨幅", dataIndex: "zf", key: "zf", render: (zf: number) => <span className={`font-medium ${zf >= 0 ? "text-red-400" : "text-green-400"}`}>{formatPercent(zf)}</span> },
    {
      title: "首封时间",
      dataIndex: "fbt",
      key: "fbt",
      render: (v: string) => <span className="text-slate-200">{toHHMMSS(v)}</span>,
      sorter: (a, b) => toSec(a.fbt) - toSec(b.fbt),
      sortDirections: ["ascend", "descend"],
    },
    {
      title: "成交额",
      dataIndex: "cje",
      key: "cje",
      render: (v: number) => <span className="text-slate-200">{formatCurrency(v)}</span>,
      sorter: (a, b) => (a.cje || 0) - (b.cje || 0),
      sortDirections: ["ascend", "descend"],
    },
    {
      title: "封板资金",
      dataIndex: "zj",
      key: "zj",
      render: (v: number) => <span className="text-slate-200">{formatCurrency(v)}</span>,
      sorter: (a, b) => (a.zj || 0) - (b.zj || 0),
      sortDirections: ["ascend", "descend"],
    },
    {
      title: "连板数",
      dataIndex: "lbc",
      key: "lbc",
      render: (v: number) => <span className={`text-slate-100 ${v >= 3 ? "text-amber-400" : ""}`}>{v}</span>,
      sorter: (a, b) => (a.lbc || 0) - (b.lbc || 0),
      sortDirections: ["ascend", "descend"],
    },
    { title: "统计", key: "tj", render: (_: unknown, item: LimitUpItem) => <span className="text-red-400 text-xs">{`${item.lbc}天${item.lbc}板`}</span> },

    { title: "价格", dataIndex: "p", key: "p", render: (p?: number) => <span className="text-slate-200">{p != null ? p.toFixed(2) : "-"}</span> },
    {
      title: "概念",
      key: "idea",
      render: (_: unknown, item: LimitUpItem) => {
        const rec = getCompanyRecord(item.dm)
        const tags = (rec?.idea || "")
          .split(",")
          .map((s) => s.trim())
          .filter(Boolean)
        if (tags.length === 0) return <span className="text-slate-500 text-xs">-</span>
        const firstTwo = tags.slice(0, 2)
        return (
          <Tooltip
            color="var(--tooltip-bg)"
            title={
              <div className="flex flex-wrap gap-2">
                {tags.map((t) => (
                  <Tag key={t} className="m-0" color={resolveTagColor(t)}>
                    {t}
                  </Tag>
                ))}
              </div>
            }>
            <div className="flex flex-wrap gap-2">
              {firstTwo.map((t) => (
                <Tag key={t} className="m-0" color={resolveTagColor(t)}>
                  {t}
                </Tag>
              ))}
              {tags.length > 2 && <span className="text-slate-500 text-xs">+{tags.length - 2}</span>}
            </div>
          </Tooltip>
        )
      },
    },
    { title: "末封时间", dataIndex: "lbt", key: "lbt", render: (v: string) => <span className="text-slate-200">{toHHMMSS(v)}</span> },
    { title: "炸板次数", dataIndex: "zbc", key: "zbc", render: (v: number) => <span className="text-slate-200">{v}</span> },
    { title: "流通市值", dataIndex: "lt", key: "lt", render: (v: number) => <span className="text-slate-200">{formatCurrency(v)}</span> },
    { title: "总市值", dataIndex: "zsz", key: "zsz", render: (v: number) => <span className="text-slate-200">{formatCurrency(v)}</span> },
    { title: "换手率", dataIndex: "hs", key: "hs", render: (v: number) => <span className="text-slate-200">{formatPercent(v)}</span> },
  ]

  return (
    <div className="bg-[var(--bg-container-50)] backdrop-blur-sm rounded-xl border border-[var(--border)] overflow-hidden">
      <div className="flex items-center justify-between px-6 py-4 border-b border-[var(--border)]">
        <div>
          <h3 className="text-lg font-semibold text-white">涨停股池</h3>
          <p className="text-xs text-slate-400">{date ? `日期：${date}` : ""}（每10分钟更新）</p>
        </div>
        <Button onClick={onRefresh} disabled={!!loading} size="small" type="primary">
          刷新
        </Button>
      </div>

      <Table
        dataSource={data}
        columns={columns}
        rowKey={(item) => `${item.dm}-${item.fbt}`}
        loading={!!loading}
        pagination={false}
        scroll={{ x: "max-content", y: "70vh" }}
        sticky
        locale={{ emptyText: "暂无数据" }}
        onRow={(record) => ({
          onClick: () => {
            if (cachingCode !== record.dm) handleFetchDetail(record)
          },
          style: { cursor: cachingCode === record.dm ? "not-allowed" : "pointer" },
        })}
      />

      <Modal
        title="公司详情"
        open={detailOpen && !!detailProfile}
        onCancel={() => {
          setDetailOpen(false)
          setDetailProfile(null)
        }}
        footer={null}
        width={800}>
        {detailProfile && (
          <div className="space-y-4">
            <CompanyProfileCard profile={detailProfile} />
            {/* <pre className="bg-[var(--bg-container-60)] text-slate-200 text-xs rounded-lg p-3 overflow-auto max-h-[40vh]">{JSON.stringify(detailProfile, null, 2)}</pre> */}
          </div>
        )}
      </Modal>
    </div>
  )
}
