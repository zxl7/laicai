import { cn } from '@/lib/utils'

/**
 * 空状态占位组件
 * 用途：在无数据或未选择条件时显示占位内容
 */
export default function Empty() {
  return (
    <div className={cn('flex h-full items-center justify-center')}>Empty</div>
  )
}
