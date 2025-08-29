import { http } from './http';
import type { WorkflowInstance } from '../types/workflow';

export async function startWorkflow(name = 'Simple Approval'): Promise<WorkflowInstance> {
  return http<WorkflowInstance>('/workflows/start', { method: 'POST', body: { name } });
}

export async function listWorkflows(): Promise<WorkflowInstance[]> {
  return http<WorkflowInstance[]>('/workflows/');
}

export async function completeUserTask(
  instanceId: string,
  taskId: string,
  data: Record<string, unknown>,
): Promise<WorkflowInstance> {
  return http<WorkflowInstance>(`/workflows/${instanceId}/tasks/${taskId}/complete`, {
    method: 'POST',
    body: { data },
  });
}
