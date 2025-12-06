import type { LimitUpItem } from './biying'
import type { CompanyProfile } from './company'

export interface CombinedStockData {
  code: string
  date: string
  list: LimitUpItem
  profile: CompanyProfile
}

