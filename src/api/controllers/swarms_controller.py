from fastapi import APIRouter, HTTPException
from typing import List
from src.api.models.swarm import Swarm, SwarmCreate, ID, USER_ID, NAME, DESCRIPTION, ARCHITECTURE, CONFIGURATION, STATUS
from src.data.db import supabase
import logging
from uuid import UUID

SWARMS_TABLE = "swarms"

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/swarms",
    tags=["swarms"],
)

@router.post("", response_model=Swarm)
async def create_swarm(swarm_create: SwarmCreate):
    logger.info(f"POST /swarms - Creating swarm: {swarm_create.name}")
    try:
        data, count = supabase.table(SWARMS_TABLE).insert(swarm_create.dict()).execute()
        swarm_data = data[1][0]
    except Exception as e:
        logger.exception(f"Unexpected error creating swarm: {e}")
        raise
    if swarm_data:
        return Swarm(**swarm_data)
    else:
        raise HTTPException(status_code=500, detail="Failed to create swarm")

@router.get("", response_model=List[Swarm])
async def list_swarms():
    logger.info("GET /swarms - Listing swarms")
    try:
        data, count = supabase.table(SWARMS_TABLE).select("*").execute()
        swarms_data = data[1]
    except Exception as e:
        logger.exception(f"Unexpected error listing swarms: {e}")
        raise
    swarms = [Swarm(**swarm_data) for swarm_data in swarms_data]
    return swarms

@router.get("/{swarm_id}", response_model=Swarm)
async def get_swarm(swarm_id: UUID):
    logger.info(f"GET /swarms/{swarm_id} - Getting swarm")
    try:
        data, count = supabase.table(SWARMS_TABLE).select("*").eq("id", str(swarm_id)).execute()
        swarm_data = data[1][0] if data[1] else None
    except Exception as e:
        logger.exception(f"Unexpected error getting swarm {swarm_id}: {e}")
        raise
    if swarm_data:
        return Swarm(**swarm_data)
    else:
        raise HTTPException(status_code=404, detail="Swarm not found")

@router.put("/{swarm_id}", response_model=Swarm)
async def update_swarm(swarm_id: UUID, swarm_create: SwarmCreate):
    logger.info(f"PUT /swarms/{swarm_id} - Updating swarm: {swarm_create.name}")
    try:
        data, count = supabase.table(SWARMS_TABLE).update(swarm_create.dict()).eq("id", str(swarm_id)).execute()
        swarm_data = data[1][0]
    except Exception as e:
        logger.exception(f"Unexpected error updating swarm {swarm_id}: {e}")
        raise
    if swarm_data:
        return Swarm(**swarm_data)
    else:
        raise HTTPException(status_code=404, detail="Swarm not found")

@router.delete("/{swarm_id}")
async def delete_swarm(swarm_id: UUID):
    logger.info(f"DELETE /swarms/{swarm_id} - Deleting swarm")
    try:
        data, count = supabase.table(SWARMS_TABLE).delete().eq("id", str(swarm_id)).execute()
    except Exception as e:
        logger.exception(f"Unexpected error deleting swarm {swarm_id}: {e}")
        raise
    return {"message": "Swarm deleted"}