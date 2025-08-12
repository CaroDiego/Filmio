import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()  

def get_supabase():
	url: str = os.getenv("SUPABASE_URL")
	key: str = os.getenv("SUPABASE_KEY")

	if not url or not key:
		raise EnvironmentError("SUPABASE_URL and/or SUPABASE_KEY environment variables are not set.")
	return create_client(url, key)
