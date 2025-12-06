import type { LimitUpItem, CompanyProfile } from '../api/types'

export interface CombinedStockData {
  code: string
  date: string
  list: LimitUpItem
  profile: CompanyProfile
}
