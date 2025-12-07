import { get } from './client'
import { StrongStockItem } from './types'

// 假设API密钥存储在环境变量中
const LICENCE_KEY = import.meta.env.VITE_BIYINGAPI_LICENCE_KEY

/**
 * 获取强势股数据
 * @param date 日期，格式为yyyy-MM-dd
 * @param bypassCache 是否绕过缓存，默认为false
 * @returns 强势股票列表
 */
export async function fetchStrongStocks(date: string, bypassCache: boolean = false): Promise<StrongStockItem[]> {
  console.log('fetchStrongStocks called with date:', date, 'bypassCache:', bypassCache)
  
  // 验证日期格式
  const dateRegex = /^\d{4}-\d{2}-\d{2}$/
  if (!dateRegex.test(date)) {
    throw new Error('日期格式不正确，请使用yyyy-MM-dd格式')
  }

  if (!LICENCE_KEY) {
    console.error('API key not found:', LICENCE_KEY)
    throw new Error('未配置API密钥，请在环境变量中设置VITE_BIYINGAPI_LICENCE_KEY')
  }

  const url = `http://api.biyingapi.com/hslt/qsgc/${date}/${LICENCE_KEY}`
  console.log('API URL:', url)
  
  try {
    const result = await get<StrongStockItem[]>(url, { bypassCache })
    console.log('API response received:', result)
    return result
  } catch (error) {
    console.error('API request failed:', error)
    throw error
  }
}
