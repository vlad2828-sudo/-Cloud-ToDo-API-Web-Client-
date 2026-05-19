import { FormEvent, useState } from 'react';
import type { CreateTaskPayload, TaskPriority } from '../types/task';

interface Props {
  onSubmit: (payload: CreateTaskPayload) => Promise<void>;
  disabled?: boolean;
}

const priorities: TaskPriority[] = ['LOW', 'MEDIUM', 'HIGH'];

export function TaskForm({ onSubmit, disabled }: Props) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState<TaskPriority>('MEDIUM');
  const [dueDate, setDueDate] = useState('');

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    await onSubmit({
      title,
      description: description || undefined,
      priority,
      dueDate: dueDate || undefined,
    });

    setTitle('');
    setDescription('');
    setPriority('MEDIUM');
    setDueDate('');
  }

  return (
    <form className="panel task-form" onSubmit={handleSubmit}>
      <div className="form-grid">
        <label>
          Title
          <input
            value={title}
            onChange={(event) => setTitle(event.target.value)}
            minLength={3}
            maxLength={120}
            required
            placeholder="Наприклад: Підготувати демо"
          />
        </label>

        <label>
          Priority
          <select value={priority} onChange={(event) => setPriority(event.target.value as TaskPriority)}>
            {priorities.map((item) => (
              <option key={item} value={item}>
                {item}
              </option>
            ))}
          </select>
        </label>

        <label>
          Due date
          <input type="date" value={dueDate} onChange={(event) => setDueDate(event.target.value)} />
        </label>
      </div>

      <label>
        Description
        <textarea
          value={description}
          onChange={(event) => setDescription(event.target.value)}
          maxLength={500}
          placeholder="Опціональний опис задачі"
        />
      </label>

      <button type="submit" disabled={disabled}>
        Add task
      </button>
    </form>
  );
}
