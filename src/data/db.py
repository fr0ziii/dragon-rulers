import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

project_id: str = os.environ.get("SUPABASE_PROJECT_ID")
url: str = f"https://{project_id}.supabase.co"
key: str = os.environ.get("SUPABASE_SERVICE_ROLE_KEY") # Using service role key

supabase: Client = create_client(url, key)

def get_db_connection():
    return supabase