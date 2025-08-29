from pydantic import BaseModel, Field
from typing import Optional


class StartWorkflowRequest(BaseModel):
    name: Optional[str] = Field(default=None)
    bpmn_filename: Optional[str] = Field(default=None)
    process_id: Optional[str] = Field(default=None)


class CompleteTaskRequest(BaseModel):
    class ApprovalData(BaseModel):
        approved: bool

    data: ApprovalData

