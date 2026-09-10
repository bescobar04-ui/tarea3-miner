from typing import List, Optional
from pydantic import BaseModel, Field

class Finding(BaseModel):
    rule_id: str
    severity: Optional[str] = None
    message: str
    file: str
    start_line: int

class Repository(BaseModel):
    name: str
    url: str
    status: str  # Ej: "analyzed", "failed", "unsupported", "clone_error"
    languages: List[str] = Field(default_factory=list)
    findings: List[Finding] = Field(default_factory=list)

class Summary(BaseModel):
    repositories: int = 0
    analyzed: int = 0
    failed: int = 0
    unsupported: int = 0
    findings: int = 0

class OrganizationResult(BaseModel):
    organization: str
    summary: Summary
    repositories: List[Repository] = Field(default_factory=list)