import type { Task, TaskPriority, TaskStatus } from '../types/task';
import { StatusBadge } from './StatusBadge';

interface Props {
  tasks: Task[];
  onStatusChange: (id: string, status: TaskStatus) => Promise<void>;
  onPriorityChange: (id: string, priority: TaskPriority) => Promise<void>;
  onDelete: (id: string) => Promise<void>;
  disabled?: boolean;
}

const statuses: TaskStatus[] = ['NEW', 'IN_PROGRESS', 'DONE'];
const priorities: TaskPriority[] = ['LOW', 'MEDIUM', 'HIGH'];

export function TaskList({ tasks, onStatusChange, onPriorityChange, onDelete, disabled }: Props) {
  if (tasks.length === 0) {
    return <div className="panel empty-state">No tasks found.</div>;
  }

  return (
    <section className="task-list">
      {tasks.map((task) => (
        <article className="panel task-card" key={task.id}>
          <div className="task-card-header">
            <div>
              <h2>{task.title}</h2>
              {task.description ? <p>{task.description}</p> : null}
            </div>
            <button className="danger" disabled={disabled} onClick={() => onDelete(task.id)}>
              Delete
            </button>
          </div>

          <div className="meta-row">
            <StatusBadge value={task.status} type="status" />
            <StatusBadge value={task.priority} type="priority" />
            {task.dueDate ? <span className="muted">Due: {task.dueDate}</span> : null}
          </div>

          <div className="actions-row">
            <label>
              Status
              <select
                value={task.status}
                disabled={disabled}
                onChange={(event) => onStatusChange(task.id, event.target.value as TaskStatus)}
              >
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
                value={task.priority}
                disabled={disabled}
                onChange={(event) => onPriorityChange(task.id, event.target.value as TaskPriority)}
              >
                {priorities.map((priority) => (
                  <option key={priority} value={priority}>
                    {priority}
                  </option>
                ))}
              </select>
            </label>
          </div>
        </article>
      ))}
    </section>
  );
}
