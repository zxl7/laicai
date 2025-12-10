import { useEffect, useState } from "react"
import { Store, CompanyRecord } from "../services/companyStore"
import { formatCurrency, formatPercent } from "../api/utils"
import { CompanyProfileCard } from "../components/CompanyProfileCard"
import type { CompanyProfile } from "../api/types"
import { fetchCompanyProfile } from "../api/company"
import { fetchStockPool } from "../api/stockPool"
import { Tag, Table, Modal, Button, Tooltip, Spin, message, Card } from "antd"
import type { TableColumnsType } from "antd"
import { resolveTagColor } from "../lib/tagColors"

export function Company() {
  const [pool, setPool] = useState<Store>({})
  const [detailOpen, setDetailOpen] = useState(false)
  const [detailRec, setDetailRec] = useState<CompanyRecord | null>(null)
  const [detailProfile, setDetailProfile] = useState<CompanyProfile | null>(null)
  const [loading, setLoading] = useState(false)
  const [poolLoading, setPoolLoading] = useState(true)

  useEffect(() => {
    fetchAllStockPoolData()
  }, [])

  /**
   * 从接口获取全部股票总池数据
   */
  const fetchAllStockPoolData = async () => {
    setPoolLoading(true)

    try {
      const stockPoolData = await fetchStockPool(true)
      // 将StrongStockItem数组转换为Store格式
      const newPool: Store = {}
      const arr = Object.values(stockPoolData)
      console.log("%c Line:36 🥪 arr", "color:#3f7cff", arr)
      arr.forEach((item) => {
        // 为每个股票创建CompanyRecord对象（允许数据不存在）
        const dm = item.dm || '' // 获取股票代码，默认为空字符串
        
        // 确保代码不为空才创建记录
        if (dm) {
          newPool[dm] = {
            code: dm,
            dm: dm,
            mc: item.mc || '', // 股票名称，默认为空
            p: item.p?.toString() || '', // 价格，可能不存在
            zf: item.zf?.toString() || '', // 涨幅，可能不存在
            cje: item.cje?.toString() || '', // 成交额，可能不存在
            // 映射LimitUpItem需要的属性，所有属性都提供默认值
            list: {
              dm: dm,
              mc: item.mc || '',
              p: item.p || 0, // 价格，默认为0
              zf: item.zf || 0, // 涨幅，默认为0
              cje: item.cje || 0, // 成交额，默认为0
              lt: item.lt || 0, // 流通市值，默认为0
              zsz: item.zsz || 0, // 总市值，默认为0
              hs: item.hs || 0, // 换手率，默认为0
              lbc: 0, // 默认为0
              fbt: "", // 默认为空
              lbt: "", // 默认为空
              zj: 0, // 默认为0
              zbc: 0, // 默认为0
              tj: item.tj || '', // 涨停统计，默认为空
            },
            lastUpdated: new Date().toISOString(),
          }
        }
      })

      setPool(newPool)
      message.success("股票总池数据加载成功")
    } catch (error) {
      console.error("获取股票总池数据失败:", error)
      message.error("获取股票总池数据失败")
    } finally {
      setPoolLoading(false)
    }
  }

  /**
   * 处理查看详情按钮点击事件
   * @param code 股票代码
   * @param rec 本地缓存的公司记录
   */
  const handleViewDetail = async (code: string, rec: CompanyRecord) => {
    setDetailRec(rec)
    setDetailOpen(true)
    setLoading(true)

    try {
      const profiles = await fetchCompanyProfile(code)
      if (profiles && profiles.length > 0) {
        setDetailProfile(profiles[0])
        message.success("详情加载成功")
      } else {
        message.info("未获取到最新详情，显示本地缓存数据")
      }
    } catch (error) {
      console.error("获取公司详情失败:", error)
      message.error("获取公司详情失败，显示本地缓存数据")
    } finally {
      setLoading(false)
    }
  }

  const entries = Object.entries(pool)
  const dataSource = entries.map(([code, rec]) => ({ code, rec }))

  return (
    <div className="min-h-screen bg-[var(--bg-base)] text-white p-6">
      <div className="max-w-7xl mx-auto">
        <div>
          <h1 className="text-3xl font-bold">股票总池</h1>
          <p className="text-slate-400">显示本地股票池缓存的最新数据</p>
        </div>

        <Card className="bg-[var(--bg-container-50)] backdrop-blur-sm rounded-xl border border-[var(--border)] overflow-hidden">
          <div className="px-6 py-4 border-b border-[var(--border)] flex items-center justify-between">
            <div className="text-sm text-slate-400">共 {entries.length} 条</div>
          </div>
          <Spin spinning={poolLoading} tip="加载中...">
            <Table
              dataSource={dataSource}
              rowKey={(row) => row.code}
              pagination={false}
              scroll={{ x: "max-content" }}
              sticky
              locale={{ emptyText: "暂无股票池数据" }}
              columns={
                [
                  { title: "代码", key: "code", dataIndex: "code", render: (code: string) => <span className="font-mono text-white">{code}</span> },
                  { title: "名称", key: "name", render: (_, { rec }) => <span className="text-slate-200">{rec.list?.mc || rec.name || "-"}</span> },
                  {
                    title: "涨幅",
                    key: "zf",
                    render: (_, { rec }) => (
                      <span className={`font-medium ${rec.list?.zf && rec.list.zf >= 0 ? "text-red-400" : "text-green-400"}`}>{rec.list?.zf != null ? formatPercent(rec.list.zf) : "-"}</span>
                    ),
                  },
                  { title: "价格", key: "p", render: (_, { rec }) => <span className="text-slate-200">{rec.list?.p != null ? rec.list.p.toFixed(2) : "-"}</span> },
                  { title: "成交额", key: "cje", render: (_, { rec }) => <span className="text-slate-200">{rec.list?.cje != null ? formatCurrency(rec.list.cje) : "-"}</span> },
                  {
                    title: "最近更新",
                    key: "lastUpdated",
                    render: (_, { rec }) => <span className="text-slate-400 text-xs">{rec.lastUpdated ? new Date(rec.lastUpdated).toLocaleString("zh-CN") : "-"}</span>,
                  },
                  { title: "详情状态", key: "status", render: (_, { rec }) => <span className="text-slate-200">{rec.name ? "已补全" : "缺失"}</span> },
                  {
                    title: "概念",
                    key: "idea",
                    render: (_, { rec }) => {
                      const tags = (rec.idea || "")
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
                  {
                    title: "详情",
                    key: "action",
                    fixed: "right",
                    width: 120,
                    render: (_, { code, rec }) => (
                      <Button size="small" onClick={() => handleViewDetail(code, rec)}>
                        查看详情
                      </Button>
                    ),
                  },
                ] as TableColumnsType<any>
              }
            />
          </Spin>
        </Card>
        <Modal
          title="公司详情"
          open={detailOpen && !!detailRec}
          onCancel={() => {
            setDetailOpen(false)
            setDetailRec(null)
            setDetailProfile(null)
          }}
          footer={null}
          width={800}>
          {detailRec && (
            <div className="space-y-4">
              <Spin spinning={loading} tip="加载详情中...">
                {detailProfile ? (
                  <CompanyProfileCard profile={detailProfile} />
                ) : detailRec.name ? (
                  <CompanyProfileCard profile={detailRec as unknown as CompanyProfile} />
                ) : (
                  <div className="text-slate-400 text-sm">该公司详情尚未补全</div>
                )}
              </Spin>
            </div>
          )}
        </Modal>
      </div>
    </div>
  )
}
