import fs from 'node:fs/promises'
import path from 'node:path'

async function main() {
  const filePath = path.join(process.cwd(), 'public', 'company-cache.json')
  const raw = await fs.readFile(filePath, 'utf-8')
  const data = JSON.parse(raw)
  const normalized = {}
  for (const [code, rec] of Object.entries(data)) {
    const next = { code }
    if (rec.list) next.list = rec.list
    if (rec.profile) next.profile = rec.profile
    if (rec.trades) next.trades = rec.trades
    if (rec.lastUpdated) next.lastUpdated = rec.lastUpdated
    // 兼容旧结构
    if (!next.list && rec.dates && typeof rec.dates === 'object') {
      const dates = Object.keys(rec.dates)
      dates.sort()
      const latest = dates[dates.length - 1]
      const latestEntry = latest ? rec.dates[latest] : null
      if (latestEntry && latestEntry.list) next.list = latestEntry.list
    }
    // 将 list 字段平铺到外层，便于直接读取（不覆盖已有同名属性）
    if (next.list && typeof next.list === 'object') {
      for (const [k, v] of Object.entries(next.list)) {
        if (next[k] === undefined) next[k] = v
      }
    }
    // 保留原对象除 dates 外的所有顶层属性（不覆盖已存在字段）
    for (const [k, v] of Object.entries(rec)) {
      if (k === 'dates') continue
      if (next[k] === undefined) next[k] = v
    }
    normalized[code] = next
  }
  await fs.writeFile(filePath, JSON.stringify(normalized, null, 2), 'utf-8')
  console.log('Normalized and wrote flattened cache to', filePath)
}

main().catch(e => { console.error(e); process.exit(1) })
