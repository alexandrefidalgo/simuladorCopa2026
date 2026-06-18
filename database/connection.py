import os
from pathlib import Path

from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://aoscrsfqhtobvbdywqcl.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "sb_publishable_OfQiv_FmMkyhdrt3pY-7ag_IiTZp0Fd")


def get_supabase() -> Client:
    if not SUPABASE_KEY or SUPABASE_KEY == "YOUR_SERVICE_ROLE_KEY_HERE":
        raise RuntimeError(
            "SUPABASE_KEY não configurada. Copie .env.example para .env e preencha "
            "com a chave do projeto em Supabase → Settings → API."
        )
    return create_client(SUPABASE_URL, SUPABASE_KEY)
