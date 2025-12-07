export interface LimitUpItem {
  dm: string
  mc: string
  p: number
  zf: number
  cje: number
  lt: number
  zsz: number
  hs: number
  lbc: number
  fbt: string
  lbt: string
  zj: number
  zbc: number
  tj: string
}

/**
 * 强势股数据项
 */
export interface StrongStockItem {
  dm: string        // 代码
  mc: string        // 名称
  p: number         // 价格（元）
  ztp: number       // 涨停价（元）
  zf: number        // 涨幅（%）
  cje: number       // 成交额（元）
  lt: number        // 流通市值（元）
  zsz: number       // 总市值（元）
  zs: number        // 涨速（%）
  nh: number        // 是否新高（0：否，1：是）
  lb: number        // 量比
  hs: number        // 换手率（%）
  tj: string        // 涨停统计（x天/y板）
}

export interface LimitDownItem {
  dm: string
  mc: string
  p: number
  zf: number
  cje: number
  lt: number
  zsz: number
  pe: number
  hs: number
  lbc: number
  lbt: string
  zj: number
  fba: number
  zbc: number
}

export interface CompanyProfile {
  name: string
  ename: string
  market: string
  idea: string
  ldate: string
  sprice: string
  principal: string
  rdate: string
  rprice: string
  instype: string
  organ: string
  secre: string
  phone: string
  sphone: string
  fax: string
  sfax: string
  email: string
  semail: string
  site: string
  post: string
  infosite: string
  oname: string
  addr: string
  oaddr: string
  desc: string
  bscope: string
  printype: string
  referrer: string
  putype: string
  pe: string
  firgu: string
  lastgu: string
  realgu: string
  planm: string
  realm: string
  pubfee: string
  collect: string
  signfee: string
  pdate: string
  dm: string
  mc: string
  zf: string
  p: string
  cje: string
  lt: string
  zsz: string
  hs: string
  zj: string
  fbt: string
  lbt: string
  zbc: string
  tj: string
  lbc: string
  hy: string
}
