import type { TaskFilters as TaskFiltersType, TaskPriority, TaskStatus } from '../types/task';

interface Props {
  filters: TaskFiltersType;
  onChange: (filters: TaskFiltersType) => void;
}

const statuses: TaskStatus[] = ['NEW', 'IN_PROGRESS', 'DONE'];
const priorities: TaskPriority[] = ['LOW', 'MEDIUM', 'HIGH'];

export function TaskFilters({ filters, onChange }: Props) {
  return (
    <section className="panel filters">
      <label>
        Status
        <select
          value={filters.status ?? ''}
          onChange={(event) => onChange({ ...filters, status: event.target.value as TaskStatus | '' })}
        >
          <option value="">All</option>
          {statuses.map((status) => (
            <option key={status} value={status}>
              {status}
            </option>
          ))}
        </select>
      </label>

      <label>
        Priority
        <select
          value={filters.priority ?? ''}
          onChange={(event) => onChange({ ...filters, priority: event.target.value as TaskPriority | '' })}
        >
          <option value="">All</option>
          {priorities.map((priority) => (
            <option key={priority} value={priority}>
              {priority}
            </option>
          ))}
        </select>
      </label>
    </section>
  );
}
