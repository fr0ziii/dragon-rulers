from dotenv import load_dotenv
from src.data.db import supabase
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

async def create_agent(agent_data: dict):
    """Creates a new agent in the database."""
    logger.info(f"Creating agent: {agent_data}")
    try:
        data, count = supabase.table("agents").insert(agent_data).execute()
        logger.info(f"Agent created successfully: {data}")
        return data
    except Exception as e:
        logger.error(f"Error creating agent: {e}")
        return None

async def update_agent(agent_id: int, agent_data: dict):
    """Updates an existing agent in the database."""
    logger.info(f"Updating agent with ID {agent_id}: {agent_data}")
    try:
        data, count = supabase.table("agents").update(agent_data).eq("id", agent_id).execute()
        logger.info(f"Agent updated successfully: {data}")
        return data
    except Exception as e:
        logger.error(f"Error updating agent: {e}")
        return None

async def delete_agent(agent_id: int):
    """Deletes an agent from the database."""
    logger.info(f"Deleting agent with ID {agent_id}")
    try:
        data, count = supabase.table("agents").delete().eq("id", agent_id).execute()
        logger.info(f"Agent deleted successfully: {data}")
        return data
    except Exception as e:
        logger.error(f"Error deleting agent: {e}")
        return None