from typing import List, Optional

from pydantic import BaseModel

from ecommerce_api.models.repair_job import RepairJobStatus


class RepairJobCreate(BaseModel):
    employee_id: int
    issue_description: str
    status: RepairJobStatus
    cost_estimate: Optional[float] = float | None
    machine_model: str


class RepairJobPublic(BaseModel):
    id: int
    employee_id: int
    issue_description: str
    status: RepairJobStatus
    cost_estimate: Optional[float] = float | None
    machine_model: str


class RepairJobUpdate(BaseModel):
    employee_id: int
    issue_description: str
    status: RepairJobStatus
    cost_estimate: Optional[float] = float | None
    machine_model: str


class RepairJobList(BaseModel):
    repair_jobs: List[RepairJobPublic]
