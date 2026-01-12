import { DatePicker } from "antd"
import dayjs from "dayjs"
import { isWeekend } from "../utils/date"

export type DateSelectorProps = {
  value: string
  onChange: (value: string) => void
  min?: string
  max?: string
  className?: string
  placeholder?: string
}

export function DateSelector({ value, onChange, min, max, className, placeholder }: DateSelectorProps) {
  const disabledDate = (current: dayjs.Dayjs) => {
    if (!current) return false
    
    // Disable weekends
    if (isWeekend(current)) return true
    
    // Disable out of range
    if (min && current.isBefore(dayjs(min), 'day')) return true
    if (max && current.isAfter(dayjs(max), 'day')) return true
    
    return false
  }

  return (
    <DatePicker
      value={value ? dayjs(value) : undefined}
      format="YYYY-MM-DD"
      allowClear={false}
      placeholder={placeholder || "选择日期"}
      disabledDate={disabledDate}
      onChange={(d) => onChange(d?.format("YYYY-MM-DD") || "")}
      className={className}
    />
  )
}
