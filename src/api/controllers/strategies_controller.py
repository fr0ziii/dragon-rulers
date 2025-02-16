from fastapi import APIRouter, HTTPException
from typing import List
from src.api.models.strategy import Strategy, StrategyCreate
from src.data.db import supabase
import logging
from uuid import UUID

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/strategies",
    tags=["strategies"],
)

@router.post("", response_model=Strategy)
async def create_strategy(strategy_create: StrategyCreate):
    logger.info(f"POST /strategies - Creating strategy: {strategy_create.name}")
    try:
        data, count = supabase.table("strategies").insert(strategy_create.dict()).execute()
        strategy_data = data[1][0]
    except Exception as e:
        logger.exception(f"Unexpected error creating strategy: {e}")
        raise

    if strategy_data:
        return Strategy(**strategy_data)
    else:
        raise HTTPException(status_code=500, detail="Failed to create strategy")

@router.get("", response_model=List[Strategy])
async def list_strategies():
    logger.info("GET /strategies - Listing strategies")
    try:
        data, count = supabase.table("strategies").select("*").execute()
        strategies_data = data[1]
    except Exception as e:
        logger.exception(f"Unexpected error listing strategies: {e}")
        raise
    strategies = [Strategy(**strategy_data) for strategy_data in strategies_data]
    return strategies

@router.get("/{strategy_id}", response_model=Strategy)
async def get_strategy(strategy_id: UUID):
    logger.info(f"GET /strategies/{strategy_id} - Getting strategy")
    try:
        data, count = supabase.table("strategies").select("*").eq("id", str(strategy_id)).execute()
        strategy_data = data[1][0] if data[1] else None
    except Exception as e:
        logger.exception(f"Unexpected error getting strategy {strategy_id}: {e}")
        raise
    if strategy_data:
        return Strategy(**strategy_data)
    else:
        raise HTTPException(status_code=404, detail="Strategy not found")

@router.put("/{strategy_id}", response_model=Strategy)
async def update_strategy(strategy_id: UUID, strategy_create: StrategyCreate):
    logger.info(f"PUT /strategies/{strategy_id} - Updating strategy: {strategy_create.name}")
    try:
        data, count = supabase.table("strategies").update(strategy_create.dict()).eq("id", str(strategy_id)).execute()
        strategy_data = data[1][0]
    except Exception as e:
        logger.exception(f"Unexpected error updating strategy {strategy_id}: {e}")
        raise
    if strategy_data:
        return Strategy(**strategy_data)
    else:
        raise HTTPException(status_code=404, detail="Strategy not found")

@router.delete("/{strategy_id}")
async def delete_strategy(strategy_id: UUID):
    logger.info(f"DELETE /strategies/{strategy_id} - Deleting strategy")
    try:
        data, count = supabase.table("strategies").delete().eq("id", str(strategy_id)).execute()
    except Exception as e:
        logger.exception(f"Unexpected error deleting strategy {strategy_id}: {e}")
        raise
    return {"message": "Strategy deleted"}