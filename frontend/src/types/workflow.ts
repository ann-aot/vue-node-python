export type TaskSummary = {
  id: string;
  name: string;
  spec_name: string;
};

export type WorkflowInstance = {
  id: string;
  name: string;
  status: string;
  ready_user_tasks: TaskSummary[];
};
