from pydantic import BaseModel
from typing import Dict, Optional
from uuid import UUID

ID = "id"
USER_ID = "user_id"
NAME = "name"
DESCRIPTION = "description"
STRATEGY_ID = "strategy_id"
CONFIGURATION = "configuration"
STATUS = "status"

class Agent(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    description: Optional[str] = None
    strategy_id: UUID
    configuration: Optional[Dict] = None
    status: str

    def dict(self, *args, **kwargs):
        data = super().dict(*args, **kwargs)
        if USER_ID in data:
            data[USER_ID] = str(data[USER_ID])
        if STRATEGY_ID in data:
            data[STRATEGY_ID] = str(data[STRATEGY_ID])
        if ID in data:
            data[ID] = str(data[ID])
        return data

class AgentCreate(BaseModel):
    user_id: UUID
    name: str
    description: Optional[str] = None
    strategy_id: UUID
    configuration: Optional[Dict] = None
    status: str

    def dict(self, *args, **kwargs):
        data = super().dict(*args, **kwargs)
        if "user_id" in data:
            data["user_id"] = str(data["user_id"])
        if "strategy_id" in data:
            data["strategy_id"] = str(data["strategy_id"])
        return data