from fastapi import APIRouter, HTTPException
from typing import List
from src.api.models.agent import Agent, AgentCreate
from src.data.db import supabase
import logging
from uuid import UUID, uuid4
import datetime
from src.api.services.common import publish_event, KafkaPublishError

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/agents",
    tags=["agents"],
)

@router.post("", response_model=Agent)
async def create_agent(agent_create: AgentCreate):
    logger.info(f"POST /agents - Creating agent: {agent_create}")
    try:
        # Use the Supabase client to insert data
        agent_data = agent_create.dict()
        if "id" not in agent_data or agent_data["id"] is None:
          agent_data["id"] = str(uuid4())
        agent_data["created_at"] = str(datetime.datetime.now())
        data, count = supabase.table("trading_agents").insert(agent_data).execute()
        logger.info(data)
        agent_data = data[1][0]  # Assuming the first item in the list is the result

    except Exception as e:
        logger.exception(f"Unexpected error creating agent: {e}")
        raise

    if agent_data:
        agent = Agent(**agent_data)
        # Publish agent.created event
        try:
            publish_event("agents", "agent.created", agent.dict())
        except KafkaPublishError as e:
            logger.error(f"Failed to publish agent.created event: {e}")
            # Decide how to handle this - retry, dead-letter queue, etc.
            # For now, just log and continue
        logger.info(f"Agent created: {agent}")
        return agent
    else:
        logger.error("Failed to create agent: No data returned from database")
        raise HTTPException(status_code=500, detail="Failed to create agent")

@router.get("", response_model=List[Agent])
async def list_agents():
    logger.info("GET /agents - Listing agents")
    try:
      data, count = supabase.table("trading_agents").select("*").execute()
      agents_data = data[1]
    except Exception as e:
        logger.exception(f"Unexpected error listing agents: {e}")
        raise

    agents = [Agent(**agent_data) for agent_data in agents_data]
    logger.info(f"Found {len(agents)} agents")
    return agents

@router.get("/{agent_id}", response_model=Agent)
async def get_agent(agent_id: UUID):
    logger.info(f"GET /agents/{agent_id} - Getting agent")
    try:
        data, count = supabase.table("trading_agents").select("*").eq("id", str(agent_id)).execute()
        agent_data = data[1][0]  if data[1] else None
    except Exception as e:
        logger.exception(f"Unexpected error getting agent {agent_id}: {e}")
        raise

    if agent_data:
        agent = Agent(**agent_data)
        logger.info(f"Found agent: {agent}")
        return agent
    else:
        logger.warning(f"Agent not found: {agent_id}")
        raise HTTPException(status_code=404, detail="Agent not found")

@router.put("/{agent_id}", response_model=Agent)
async def update_agent(agent_id: UUID, agent_create: AgentCreate):
    logger.info(f"PUT /agents/{agent_id} - Updating agent: {agent_create}")
    try:
        data, count = supabase.table("trading_agents").update(agent_create.dict()).eq("id", str(agent_id)).execute()
        agent_data = data[1][0]

    except Exception as e:
        logger.exception(f"Unexpected error updating agent {agent_id}: {e}")
        raise

    if agent_data:
        agent = Agent(**agent_data)        
        # Publish agent.updated event
        try:
            publish_event("agents", "agent.updated", agent.dict())
        except KafkaPublishError as e:
            logger.error(f"Failed to publish agent.updated event: {e}")
            # Decide how to handle this - retry, dead-letter queue, etc.
        logger.info(f"Agent updated: {agent}")
        return agent

    else:
        logger.warning(f"Agent not found for update: {agent_id}")
        raise HTTPException(status_code=404, detail="Agent not found")

@router.delete("/{agent_id}")
async def delete_agent(agent_id: UUID):
    logger.info(f"DELETE /agents/{agent_id} - Deleting agent")
    try:
        data, count = supabase.table("trading_agents").delete().eq("id", str(agent_id)).execute()

    except Exception as e:
        logger.exception(f"Unexpected error deleting agent {agent_id}: {e}")
        raise
    
    logger.info(f"Agent deleted: {agent_id}")
    return {"message": "Agent deleted"}