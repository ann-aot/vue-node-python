from pydantic import BaseModel, Field


class StartWorkflowRequest(BaseModel):
    name: str = Field(default="Simple Approval")
    bpmn_filename: str = Field(default="simple_approval.bpmn")
    process_id: str = Field(default="SimpleApproval")


class CompleteTaskRequest(BaseModel):
    class ApprovalData(BaseModel):
        approved: bool

    data: ApprovalData

