from dotenv import load_dotenv
from src.data.db import supabase

load_dotenv()

async def create_agent(agent_data: dict):
    """Creates a new agent in the database."""
    try:
        data, count = supabase.table("agents").insert(agent_data).execute()
        return data
    except Exception as e:
        print(f"Error creating agent: {e}")
        return None

async def update_agent(agent_id: int, agent_data: dict):
    """Updates an existing agent in the database."""
    try:
        data, count = supabase.table("agents").update(agent_data).eq("id", agent_id).execute()
        return data
    except Exception as e:
        print(f"Error updating agent: {e}")
        return None

async def delete_agent(agent_id: int):
    """Deletes an agent from the database."""
    try:
        data, count = supabase.table("agents").delete().eq("id", agent_id).execute()
        return data
    except Exception as e:
        print(f"Error deleting agent: {e}")
        return None