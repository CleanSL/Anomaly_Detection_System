import os
from supabase import create_client, Client

SUPABASE_URL = "https://stpfrtvhfwlpdlmgmhbo.supabase.co"
SUPABASE_ANON_KEY = "sb_publishable_ChBz3flKPHZRVL0jR2mQqg_e6FrkAYM"

if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    raise ValueError("Missing SUPABASE_URL or SUPABASE_ANON_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

print("Connected to Supabase successfully!")