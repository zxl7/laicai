import type { StrongStockItem, CompanyProfile } from "../api/types"
import { useState, useEffect } from "react"
import { Modal, Button, Table, Tooltip, Tag } from "antd"
import type { TableColumnsType } from "antd"
import { CompanyProfileCard } from "./CompanyProfileCard"
import { fetchCompanyProfile } from "../api/company"
import { getCompanyRecord, updateCompanyCache } from "../services/companyStore"
import { formatPercent, formatCurrency } from "../api/utils"
import { resolveTagColor } from "../lib/tagColors"

interface StrongStocksTableProps {
  data: StrongStockItem[]
  loading?: boolean
  onRefresh?: () => void
  title?: string
  date?: string
}

export function StrongStocksTable({ data, loading, onRefresh, title, date }: StrongStocksTableProps) {
  const [cachingCode, setCachingCode] = useState<string | null>(null)
  const [detailOpen, setDetailOpen] = useState(false)
  const [detailProfile, setDetailProfile] = useState<CompanyProfile | null>(null)

  // 自动添加数据到股票池
  useEffect(() => {
    if (data && data.length > 0) {
      const payload: any = {}
      data.forEach((item) => {
        const local = getCompanyRecord(item.dm)
        payload[item.dm] = {
          code: item.dm,
          list: item as any,
          ...item,
          ...(local || {}),
        }
      })
      updateCompanyCache(payload)
      console.log("自动添加到股票池完成，共处理", data.length, "只股票")
    }
  }, [data])

  // 获取公司详情
  const handleFetchDetail = async (item: StrongStockItem) => {
    const local = getCompanyRecord(item.dm)
    if (local && local.name) {
      setDetailProfile(local as unknown as CompanyProfile)
      setDetailOpen(true)
      return
    }
    setCachingCode(item.dm)
    try {
      const profiles = await fetchCompanyProfile(item.dm)
      const profile = profiles[0] || null
      if (profile) {
        const payload = {
          [item.dm]: {
            code: item.dm,
            list: item as any,
            ...item,
            ...profile,
          },
        }
        updateCompanyCache(payload)
        setDetailProfile(profile)
        setDetailOpen(true)
      } else {
        console.log("未获取到公司详情，使用本地数据")
        // 如果API未返回数据，使用本地缓存的基本信息
        const basicPayload = {
          [item.dm]: {
            code: item.dm,
            list: item as any,
            mc: item.mc, // 公司名称
            dm: item.dm, // 公司代码
          },
        }
        updateCompanyCache(basicPayload)
        setDetailProfile(basicPayload[item.dm] as unknown as CompanyProfile)
        setDetailOpen(true)
      }
    } catch (error) {
      console.error("获取公司详情失败:", error)
      // 出错时仍然显示基本信息
      const basicPayload = {
        [item.dm]: {
          code: item.dm,
          list: item as any,
          mc: item.mc, // 公司名称
          dm: item.dm, // 公司代码
        },
      }
      updateCompanyCache(basicPayload)
      setDetailProfile(basicPayload[item.dm] as unknown as CompanyProfile)
      setDetailOpen(true)
    } finally {
      setCachingCode(null)
    }
  }

  // 定义表格列
  const columns: TableColumnsType<StrongStockItem> = [
    { title: "代码", dataIndex: "dm", key: "dm", render: (dm: string) => <span className="text-slate-200">{dm}</span> },
    { title: "名称", dataIndex: "mc", key: "mc", render: (mc: string) => <span className="text-slate-200">{mc}</span> },
    {
      title: "价格",
      dataIndex: "p",
      key: "p",
      render: (p: number) => <span className="text-slate-200">{p.toFixed(2)}</span>,
      sorter: (a, b) => (a.p || 0) - (b.p || 0),
      sortDirections: ["ascend", "descend"],
    },
    {
      title: "涨幅",
      dataIndex: "zf",
      key: "zf",
      render: (zf: number) => <span className={`font-medium ${zf >= 0 ? "text-red-400" : "text-green-400"}`}>{formatPercent(zf)}</span>,
      sorter: (a, b) => (a.zf || 0) - (b.zf || 0),
      sortDirections: ["ascend", "descend"],
    },
    {
      title: "涨停价",
      dataIndex: "ztp",
      key: "ztp",
      render: (ztp: number) => <span className="text-slate-200">{ztp.toFixed(2)}</span>,
      sorter: (a, b) => (a.ztp || 0) - (b.ztp || 0),
      sortDirections: ["ascend", "descend"],
    },
    {
      title: "涨速",
      dataIndex: "zs",
      key: "zs",
      render: (zs: number) => <span className={`${zs >= 0 ? "text-red-400" : "text-green-400"}`}>{formatPercent(zs)}</span>,
      sorter: (a, b) => (a.zs || 0) - (b.zs || 0),
      sortDirections: ["ascend", "descend"],
    },
    {
      title: "新高",
      dataIndex: "nh",
      key: "nh",
      render: (nh: number) => <span className="text-slate-200">{nh === 1 ? "是" : "否"}</span>,
    },
    {
      title: "量比",
      dataIndex: "lb",
      key: "lb",
      render: (lb: number) => <span className="text-slate-200">{lb.toFixed(2)}</span>,
      sorter: (a, b) => (a.lb || 0) - (b.lb || 0),
      sortDirections: ["ascend", "descend"],
    },
    {
      title: "换手率",
      dataIndex: "hs",
      key: "hs",
      render: (hs: number) => <span className="text-slate-200">{formatPercent(hs)}</span>,
      sorter: (a, b) => (a.hs || 0) - (b.hs || 0),
      sortDirections: ["ascend", "descend"],
    },
    {
      title: "成交额",
      dataIndex: "cje",
      key: "cje",
      render: (cje: number) => <span className="text-slate-200">{formatCurrency(cje)}</span>,
      sorter: (a, b) => (a.cje || 0) - (b.cje || 0),
      sortDirections: ["ascend", "descend"],
    },
    {
      title: "流通市值",
      dataIndex: "lt",
      key: "lt",
      render: (lt: number) => <span className="text-slate-200">{formatCurrency(lt)}</span>,
      sorter: (a, b) => (a.lt || 0) - (b.lt || 0),
      sortDirections: ["ascend", "descend"],
    },
    {
      title: "总市值",
      dataIndex: "zsz",
      key: "zsz",
      render: (zsz: number) => <span className="text-slate-200">{formatCurrency(zsz)}</span>,
      sorter: (a, b) => (a.zsz || 0) - (b.zsz || 0),
      sortDirections: ["ascend", "descend"],
    },
    {
      title: "涨停统计",
      dataIndex: "tj",
      key: "tj",
      render: (tj: string) => <span className="text-slate-200">{tj}</span>,
      sorter: (a, b) => {
        // 解析tj字段，提取涨停板数量，格式为"x天/y板"
        const getLimitUpCount = (tj: string): number => {
          const match = tj.match(/(\d+)板$/)
          return match ? parseInt(match[1], 10) : 0
        }
        return getLimitUpCount(a.tj || "") - getLimitUpCount(b.tj || "")
      },
      sortDirections: ["ascend", "descend"],
    },
    {
      title: "概念",
      key: "idea",
      render: (_: unknown, item: StrongStockItem) => {
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
  ]

  return (
    <div className="bg-[var(--bg-container-50)] backdrop-blur-sm rounded-xl border border-[var(--border)] overflow-hidden">
      <div className="flex items-center justify-between px-6 py-4 border-b border-[var(--border)]">
        <div>
          <h3 className="text-lg font-semibold text-white">{title || "强势股池"}</h3>
          <p className="text-xs text-slate-400">{date ? `日期：${date}` : ""}</p>
        </div>
        {onRefresh && (
          <Button onClick={onRefresh} disabled={!!loading} size="small" type="primary">
            刷新
          </Button>
        )}
      </div>

      <Table
        dataSource={data}
        columns={columns}
        rowKey={(item) => `${item.dm}`}
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

      {/* 公司详情弹窗 */}
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
          </div>
        )}
      </Modal>
    </div>
  )
}
