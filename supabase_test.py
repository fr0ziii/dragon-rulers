import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

project_id: str = os.environ.get("SUPABASE_PROJECT_ID")
url: str = f"https://{project_id}.supabase.co"
key: str = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

print(f"URL: {url}")
print(f"Key: {key}")

try:
    supabase: Client = create_client(url, key)
    print("Supabase client created successfully!")
except Exception as e:
    print(f"Error creating Supabase client: {e}")