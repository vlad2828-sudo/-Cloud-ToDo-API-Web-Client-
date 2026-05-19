import { apiRequest } from './client';
import type { CreateTaskPayload, Task, TaskFilters, TaskListResponse, TaskPriority, TaskStatus } from '../types/task';

export async function getTasks(filters: TaskFilters): Promise<TaskListResponse> {
  const params = new URLSearchParams();
  params.set('limit', '50');
  params.set('offset', '0');

  if (filters.status) params.set('status', filters.status);
  if (filters.priority) params.set('priority', filters.priority);

  return apiRequest<TaskListResponse>(`/api/tasks?${params.toString()}`);
}

export async function createTask(payload: CreateTaskPayload): Promise<Task> {
  return apiRequest<Task>('/api/tasks', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export async function updateTaskStatus(id: string, status: TaskStatus): Promise<Task> {
  return apiRequest<Task>(`/api/tasks/${id}`, {
    method: 'PATCH',
    body: JSON.stringify({ status }),
  });
}

export async function updateTaskPriority(id: string, priority: TaskPriority): Promise<Task> {
  return apiRequest<Task>(`/api/tasks/${id}`, {
    method: 'PATCH',
    body: JSON.stringify({ priority }),
  });
}

export async function deleteTask(id: string): Promise<void> {
  return apiRequest<void>(`/api/tasks/${id}`, {
    method: 'DELETE',
  });
}
