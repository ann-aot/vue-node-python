import threading
import uuid
from pathlib import Path

from SpiffWorkflow.bpmn.parser import BpmnParser
from SpiffWorkflow.bpmn.workflow import BpmnWorkflow
from SpiffWorkflow.task import Task, TaskState


class WorkflowInstance:
    def __init__(self, instance_id: str, name: str, workflow: BpmnWorkflow):
        self.instance_id = instance_id
        self.name = name
        self.workflow = workflow

    def to_dict(self) -> dict:
        return {
            "id": self.instance_id,
            "name": self.name,
            "status": self._status(),
            "ready_user_tasks": [
                {
                    "id": str(task.id),
                    "name": task.task_spec.name,
                    "spec_name": task.task_spec.name,
                }
                for task in WorkflowService.get_ready_user_tasks(self.workflow)
            ],
        }

    def _status(self) -> str:
        if self.workflow.is_completed():
            return "COMPLETED"
        # SpiffWorkflow 3.x uses American spelling
        is_canceled = getattr(self.workflow, "is_canceled", None)
        if callable(is_canceled) and is_canceled():
            return "CANCELLED"
        return "RUNNING"


class WorkflowService:
    _lock = threading.Lock()
    _instances: dict[str, WorkflowInstance] = {}
    _parser: BpmnParser | None = None
    _spec_cache: dict[str, object] = {}

    @staticmethod
    def _get_parser() -> BpmnParser:
        if WorkflowService._parser is None:
            WorkflowService._parser = BpmnParser()
        return WorkflowService._parser

    @staticmethod
    def _get_bpmn_path(filename: str) -> Path:
        base = Path(__file__).resolve().parent.parent / "workflows"
        return base / filename

    @staticmethod
    def load_spec(bpmn_filename: str, process_id: str):
        cache_key = f"{bpmn_filename}::{process_id}"
        # Return from cache if present
        if cache_key in WorkflowService._spec_cache:
            return WorkflowService._spec_cache[cache_key]
        parser = WorkflowService._get_parser()
        path = WorkflowService._get_bpmn_path(bpmn_filename)
        # First try to fetch an existing spec in the parser
        try:
            spec = parser.get_spec(process_id)
        except Exception:
            # Not loaded yet: register BPMN file, then get spec by process id
            parser.add_bpmn_file(str(path))
            spec = parser.get_spec(process_id)
        WorkflowService._spec_cache[cache_key] = spec
        return spec

    @staticmethod
    def start_workflow(
        name: str,
        bpmn_filename: str,
        process_id: str,
    ) -> dict:
        spec = WorkflowService.load_spec(bpmn_filename, process_id)
        workflow = BpmnWorkflow(spec)
        workflow.do_engine_steps()
        instance_id = str(uuid.uuid4())
        instance = WorkflowInstance(instance_id, name, workflow)
        with WorkflowService._lock:
            WorkflowService._instances[instance_id] = instance
        return instance.to_dict()

    @staticmethod
    def list_workflows() -> list[dict]:
        with WorkflowService._lock:
            return [
                instance.to_dict()
                for instance in WorkflowService._instances.values()
            ]

    @staticmethod
    def get_instance(instance_id: str) -> WorkflowInstance:
        with WorkflowService._lock:
            instance = WorkflowService._instances.get(instance_id)
        if instance is None:
            raise KeyError("Workflow instance not found")
        return instance

    @staticmethod
    def get_ready_user_tasks(workflow: BpmnWorkflow) -> list[Task]:
        # Ensure waiting tasks are refreshed before we query states
        if hasattr(workflow, "refresh_waiting_tasks"):
            workflow.refresh_waiting_tasks()
        if hasattr(workflow, "update_waiting_tasks"):
            workflow.update_waiting_tasks()
        # Include tasks that are waiting or ready for user action
        tasks_ready: list[Task] = workflow.get_tasks(state=TaskState.READY)
        tasks_waiting: list[Task] = workflow.get_tasks(state=TaskState.WAITING)
        tasks: list[Task] = tasks_ready + [
            t for t in tasks_waiting if t not in tasks_ready
        ]
        # Identify BPMN User Tasks by bpmn_name or class name heuristic
        def is_user_task(t: Task) -> bool:
            name = getattr(t.task_spec, "bpmn_name", "")
            if isinstance(name, str) and name.lower() == "usertask":
                return True
            return "usertask" in t.task_spec.__class__.__name__.lower()
        return [t for t in tasks if is_user_task(t)]

    @staticmethod
    def complete_user_task(instance_id: str, task_id: str, data: dict) -> dict:
        instance = WorkflowService.get_instance(instance_id)
        workflow = instance.workflow
        # Locate task: prefer direct lookup by id, fallback to string match
        task: Task | None = None
        try:
            task = workflow.get_task_from_id(int(task_id))
        except Exception:
            task = next(
                (t for t in workflow.get_tasks() if str(t.id) == str(task_id)),
                None,
            )
        if task is None:
            raise KeyError("Task not found")
        if task.state != TaskState.READY:
            # Attempt to move the task to READY state, then re-check
            try:
                workflow.run_task_from_id(task.id)
                # Some engines require refreshing waiting tasks
                if hasattr(workflow, "refresh_waiting_tasks"):
                    workflow.refresh_waiting_tasks()
            except Exception:
                pass
            # Re-fetch task and verify state
            try:
                task = workflow.get_task_from_id(task.id)
            except Exception:
                pass
            if task.state != TaskState.READY:
                raise ValueError("Task is not ready")
        task.data.update(data or {})
        # Ensure gateway conditions can see the variables
        workflow.data.update(data or {})
        task.complete()
        workflow.do_engine_steps()
        return instance.to_dict()

