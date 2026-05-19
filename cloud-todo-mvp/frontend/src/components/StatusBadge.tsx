import type { TaskPriority, TaskStatus } from '../types/task';

interface Props {
  value: TaskStatus | TaskPriority;
  type: 'status' | 'priority';
}

export function StatusBadge({ value, type }: Props) {
  return <span className={`badge badge-${type}`}>{value}</span>;
}
