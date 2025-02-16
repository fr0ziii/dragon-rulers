from pydantic import BaseModel
from typing import Dict, Optional
from uuid import UUID

ID = "id"
USER_ID = "user_id"
NAME = "name"
DESCRIPTION = "description"
ARCHITECTURE = "architecture"
CONFIGURATION = "configuration"
STATUS = "status"

class Swarm(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    description: Optional[str] = None
    architecture: str
    configuration: Optional[Dict] = None
    status: str

    def dict(self, *args, **kwargs):
        data = super().dict(*args, **kwargs)
        if USER_ID in data:
            data[USER_ID] = str(data[USER_ID])
        if ID in data:
            data[ID] = str(data[ID])
        return data

class SwarmCreate(BaseModel):
    user_id: UUID
    name: str
    description: Optional[str] = None
    architecture: str
    configuration: Optional[Dict] = None
    status: str

    def dict(self, *args, **kwargs):
        data = super().dict(*args, **kwargs)
        if USER_ID in data:
            data[USER_ID] = str(data[USER_ID])
        return data