import dayjs from 'dayjs'

export const isWeekend = (date: string | dayjs.Dayjs): boolean => {
  const d = dayjs(date)
  const day = d.day()
  return day === 0 || day === 6 // 0 is Sunday, 6 is Saturday
}

export const getLatestTradingDay = (): string => {
  let d = dayjs()
  // If it's Saturday (6), subtract 1 day to Friday
  if (d.day() === 6) {
    d = d.subtract(1, 'day')
  }
  // If it's Sunday (0), subtract 2 days to Friday
  else if (d.day() === 0) {
    d = d.subtract(2, 'day')
  }
  // If it's before 9:30 AM on a Monday, maybe we should show Friday?
  // But usually "today" is fine even if empty. 
  // The user requirement "default select nearest trading day" usually implies "today if trading day, else previous trading day".
  // Note: This simple logic doesn't handle holidays.
  
  return d.format('YYYY-MM-DD')
}
