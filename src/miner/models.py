from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

# 1. Estado de la generación del SBOM
class SbomStatus(str, Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

# 2. Metadatos del SBOM para el JSON general
class SbomMetadata(BaseModel):
    full_name: str
    commit_hash: str
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    syft_version: str
    status: SbomStatus
    component_count: int = 0
    sbom_path: Optional[str] = None
    error_message: Optional[str] = None

# 3. Modelo del repositorio con SBOM integrado
class RepositoryResult(BaseModel):
    name: str
    full_name: str
    commit_hash: Optional[str] = None
    sbom_info: Optional[SbomMetadata] = None