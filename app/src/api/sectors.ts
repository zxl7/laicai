import { get } from './client'
import { Sector } from '../types'

/**
 * 获取板块数据
 * @param bypassCache 是否绕过缓存，默认为false
 * @returns 板块列表
 */
export async function fetchSectors(bypassCache: boolean = false): Promise<Sector[]> {
  const url = '/api/quote/sectors'
  console.log('Sectors API URL:', url)

  try {
    const result = await get<Sector[]>(url, { bypassCache })
    // 确保返回的是数组，避免组件处理时出错
    return Array.isArray(result) ? result : []
  } catch (error) {
    console.error('Failed to fetch sectors:', error)
    return []
  }
}
