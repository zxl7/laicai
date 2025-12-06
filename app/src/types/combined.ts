import type { LimitUpItem, CompanyProfile } from '../api/types'

export interface CombinedStockData {
  code: string
  list: LimitUpItem
  profile: CompanyProfile
}
