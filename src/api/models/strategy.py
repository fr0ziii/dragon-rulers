from pydantic import BaseModel
from typing import Dict, Optional
from uuid import UUID

ID = "id"
NAME = "name"
DESCRIPTION = "description"
CODE = "code"
PARAMETERS_SCHEMA = "parameters_schema"

class Strategy(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    code: str
    parameters_schema: Optional[Dict] = None

    def dict(self, *args, **kwargs):
        data = super().dict(*args, **kwargs)
        if ID in data:
            data[ID] = str(data[ID])
        return data

class StrategyCreate(BaseModel):
    name: str
    description: Optional[str] = None
    code: str
    parameters_schema: Optional[Dict] = None