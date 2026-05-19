import { useEffect, useState } from 'react';
import { createTask, deleteTask, getTasks, updateTaskPriority, updateTaskStatus } from '../api/tasks';
import { TaskFilters } from '../components/TaskFilters';
import { TaskForm } from '../components/TaskForm';
import { TaskList } from '../components/TaskList';
import type { ApiError, CreateTaskPayload, Task, TaskFilters as TaskFiltersType, TaskPriority, TaskStatus } from '../types/task';

export function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [total, setTotal] = useState(0);
  const [filters, setFilters] = useState<TaskFiltersType>({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function loadTasks(nextFilters = filters) {
    setLoading(true);
    setError(null);
    try {
      const result = await getTasks(nextFilters);
      setTasks(result.items);
      setTotal(result.total);
    } catch (unknownError) {
      const apiError = unknownError as ApiError;
      setError(`${apiError.code}: ${apiError.message}`);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void loadTasks(filters);
  }, []);

  async function handleFiltersChange(nextFilters: TaskFiltersType) {
    setFilters(nextFilters);
    await loadTasks(nextFilters);
  }

  async function handleCreate(payload: CreateTaskPayload) {
    setLoading(true);
    try {
      await createTask(payload);
      await loadTasks();
    } catch (unknownError) {
      const apiError = unknownError as ApiError;
      setError(`${apiError.code}: ${apiError.message}`);
    } finally {
      setLoading(false);
    }
  }

  async function handleStatusChange(id: string, status: TaskStatus) {
    await updateTaskStatus(id, status);
    await loadTasks();
  }

  async function handlePriorityChange(id: string, priority: TaskPriority) {
    await updateTaskPriority(id, priority);
    await loadTasks();
  }

  async function handleDelete(id: string) {
    await deleteTask(id);
    await loadTasks();
  }

  return (
    <main className="page">
      <header className="hero">
        <div>
          <p className="eyebrow">Cloud MVP</p>
          <h1>ToDo Dashboard</h1>
          <p>FastAPI + PostgreSQL API, React frontend, Docker-ready cloud architecture.</p>
        </div>
        <div className="counter">
          <span>{total}</span>
          <small>tasks</small>
        </div>
      </header>

      {error ? <div className="error-panel">{error}</div> : null}

      <TaskForm onSubmit={handleCreate} disabled={loading} />
      <TaskFilters filters={filters} onChange={handleFiltersChange} />
      {loading ? <div className="panel">Loading...</div> : null}
      <TaskList
        tasks={tasks}
        disabled={loading}
        onStatusChange={handleStatusChange}
        onPriorityChange={handlePriorityChange}
        onDelete={handleDelete}
      />
    </main>
  );
}
