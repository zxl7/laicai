import axios, { AxiosRequestConfig } from 'axios'

export const http = axios.create({
  timeout: 15000
})

export async function get<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
  const res = await http.get<T>(url, config)
  return res.data as T
}

export async function post<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
  const res = await http.post<T>(url, data, config)
  return res.data as T
}

