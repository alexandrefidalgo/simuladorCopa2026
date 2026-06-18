import os
from pathlib import Path

from supabase import Client, create_client

# Local: .env via dotenv | Cloud: st.secrets
try:
    import streamlit as st
    _url = st.secrets.get("SUPABASE_URL", "")
    _key = st.secrets.get("SUPABASE_KEY", "")
except Exception:
    _url = ""
    _key = ""

if not _url or not _key:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
    _url = os.getenv("SUPABASE_URL", "https://wljpvxicodobqlejffmy.supabase.co")
    _key = os.getenv("SUPABASE_KEY", "")

SUPABASE_URL = _url
SUPABASE_KEY = _key


def get_supabase() -> Client:
    if not SUPABASE_KEY or SUPABASE_KEY == "YOUR_SERVICE_ROLE_KEY_HERE":
        raise RuntimeError(
            "SUPABASE_KEY não configurada. Copie .env.example para .env e preencha "
            "com a chave do projeto em Supabase → Settings → API."
        )
    return create_client(SUPABASE_URL, SUPABASE_KEY)
