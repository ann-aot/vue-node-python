from fastapi import APIRouter
from app.schemas.workflow import StartWorkflowRequest, CompleteTaskRequest


router = APIRouter()


@router.post("/start", summary="Start a workflow")
async def start_workflow(request: StartWorkflowRequest):
    name = request.name or "Simple Approval"
    bpmn_filename = request.bpmn_filename or "simple_approval.bpmn"
    process_id = request.process_id or "SimpleApproval"
    # Replace the return with actual workflow start logic as needed
    return {
        "name": name,
        "bpmn_filename": bpmn_filename,
        "process_id": process_id,
    }


@router.post("/tasks/complete", summary="Complete a task")
async def complete_task(request: CompleteTaskRequest):
    # Replace with actual task completion logic as needed
    return {
        "approved": request.data.approved,
    }

