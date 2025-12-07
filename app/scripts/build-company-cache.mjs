import fs from 'node:fs/promises'
import path from 'node:path'

const UNIFIED_DATE = '2025-12-05'
const ARG_DATE = process.argv[2]
const TARGET_DATE = ARG_DATE || UNIFIED_DATE
const API_BASE = process.env.VITE_BIYING_API_BASE ?? 'https://api.biyingapi.com'
const LICENSE = process.env.VITE_BIYING_LICENSE || process.env.BIYING_LICENSE

if (!LICENSE) {
  console.error('Missing VITE_BIYING_LICENSE environment variable')
  process.exit(1)
}

async function sleep(ms) { return new Promise(r => setTimeout(r, ms)) }
async function fetchJson(url, attempts = 3, delayMs = 2000) {
  for (let i = 0; i < attempts; i++) {
    const res = await fetch(url)
    if (res.ok) return res.json()
    if (res.status === 429 && i < attempts - 1) {
      console.warn('Rate limited, retrying...', { attempt: i + 1 })
      await sleep(delayMs)
      continue
    }
    throw new Error(`Request failed ${res.status} ${url}`)
  }
}

async function main() {
  console.log('Building company cache for date', TARGET_DATE)
  const limitUrl = `${API_BASE}/hslt/ztgc/${TARGET_DATE}/${LICENSE}`
  const list = await fetchJson(limitUrl)
  const items = Array.isArray(list) ? list : []
  console.log('Limit-up items:', items.length)

  const store = {}
  for (const item of items) {
    const code = item.dm
    store[code] = store[code] || { code }
    store[code].list = item
    // 平铺 list 字段到外层，方便读取
    for (const [k, v] of Object.entries(item)) {
      if (store[code][k] === undefined) store[code][k] = v
    }
  }

  // Fetch company profiles sequentially to be gentle with the API
  for (const code of Object.keys(store)) {
    const url = `${API_BASE}/hscp/gsjj/${code}/${LICENSE}`
    const prof = await fetchJson(url)
    if (Array.isArray(prof) && prof[0]) {
      store[code].profile = prof[0]
    }
  }

  const outPath = path.join(process.cwd(), 'public', 'company-cache.json')
  await fs.writeFile(outPath, JSON.stringify(store, null, 2), 'utf-8')
  console.log('Written cache to', outPath)
}

main().catch((e) => {
  console.error(e)
  process.exit(1)
})
