from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List

app = FastAPI()

# --- Data Models ---
class Agent(BaseModel):
    id: int
    name: str
    role: str

class AgentCreate(BaseModel):
    name: str
    role: str

# --- In-memory storage (replace with database later) ---
agents: Dict[int, Agent] = {}
next_agent_id = 1

# --- API Endpoints ---
@app.get("/")
async def root():
    return {"message": "Welcome to the Trading Bot API"}

@app.post("/agents", response_model=Agent)
async def create_agent(agent_create: AgentCreate):
    global next_agent_id
    agent = Agent(id=next_agent_id, **agent_create.dict())
    agents[agent.id] = agent
    next_agent_id += 1
    return agent

@app.get("/agents", response_model=List[Agent])
async def list_agents():
    return list(agents.values())

@app.get("/agents/{agent_id}", response_model=Agent)
async def get_agent(agent_id: int):
    if agent_id not in agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agents[agent_id]

@app.put("/agents/{agent_id}", response_model=Agent)
async def update_agent(agent_id: int, agent_create: AgentCreate):
    if agent_id not in agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    agent = agents[agent_id]
    agent.name = agent_create.name
    agent.role = agent_create.role
    return agent

@app.delete("/agents/{agent_id}")
async def delete_agent(agent_id: int):
    if agent_id not in agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    del agents[agent_id]
    return {"message": "Agent deleted"}