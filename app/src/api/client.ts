import axios, { AxiosRequestConfig } from 'axios'

export const http = axios.create({ timeout: 15000 })

const inFlight = new Map<string, Promise<any>>()
const lastResult = new Map<string, { time: number; data: any }>()
const THROTTLE_MS = Number(import.meta.env.VITE_API_DEDUP_THROTTLE_MS ?? 5000)

function buildKey(method: string, url: string, config?: AxiosRequestConfig, data?: any) {
  const paramsStr = config?.params ? JSON.stringify(config.params) : ''
  const dataStr = data !== undefined ? JSON.stringify(data) : ''
  return `${method}|${url}|p:${paramsStr}|d:${dataStr}`
}

async function dedup<T>(method: 'GET' | 'POST', url: string, exec: () => Promise<any>, config?: AxiosRequestConfig, data?: any): Promise<T> {
  const k = buildKey(method, url, config, data)
  const now = Date.now()
  const last = lastResult.get(k)
  if (last && now - last.time < THROTTLE_MS) {
    return last.data as T
  }
  const pending = inFlight.get(k)
  if (pending) return pending as Promise<T>
  const p = exec()
  inFlight.set(k, p)
  try {
    const res = await p
    lastResult.set(k, { time: Date.now(), data: res.data })
    return res.data as T
  } finally {
    inFlight.delete(k)
  }
}

export function get<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
  return dedup<T>('GET', url, () => http.get<T>(url, config), config)
}

export function post<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
  return dedup<T>('POST', url, () => http.post<T>(url, data, config), config, data)
}
