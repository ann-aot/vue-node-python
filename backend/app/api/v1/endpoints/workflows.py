from fastapi import APIRouter, HTTPException

from app.services.workflow_service import WorkflowService
from app.schemas.workflow import StartWorkflowRequest, CompleteTaskRequest


router = APIRouter()


 


@router.post("/start", summary="Start a new workflow instance")
async def start_workflow(payload: StartWorkflowRequest):
    try:
        return WorkflowService.start_workflow(
            name=payload.name,
            bpmn_filename=payload.bpmn_filename,
            process_id=payload.process_id,
        )
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="BPMN file not found")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/", summary="List workflow instances")
async def list_workflows():
    return WorkflowService.list_workflows()


@router.post(
    "/{instance_id}/tasks/{task_id}/complete",
    summary="Complete a user task",
)
async def complete_task(
    instance_id: str,
    task_id: str,
    payload: CompleteTaskRequest,
):
    try:
        return WorkflowService.complete_user_task(
            instance_id,
            task_id,
            payload.data.model_dump(),
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
