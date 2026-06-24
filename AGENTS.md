# AGENTS.md

## Project

Simulador de bolão da Copa do Mundo 2026 — educational Python + Streamlit app.

## Run

```bash
streamlit run app.py
```

No tests, linting, or CI configured.

## Tech

- **Python 3.13+** + **Streamlit** (multi-page app)
- Database: **Supabase** (PostgreSQL) — schema in `database/schema.sql`
- Env vars: `SUPABASE_URL`, `SUPABASE_KEY` — copy `.env.example` to `.env` and fill
- `.env` is loaded via `python-dotenv` in `database/connection.py:17`; hardcoded defaults at lines 18–19
- `.streamlit/config.toml` sets `headless = true` (server starts without browser) + custom theme (light/dark)
- `supabase/` contains migrations (managed via Supabase CLI)

## Security

- `.gitignore` covers `.env`, `opencode.json`, `.mcp.json`, `.streamlit/secrets.toml` — still double-check `git add` since secrets exist in these files.

## Supabase CLI

```bash
export SUPABASE_HOME="C:\Users\alexandre.fidalgo\simuladorCopa2026\.supabase"
supabase login --token <ACCESS_TOKEN>
supabase link --project-ref aoscrsfqhtobvbdywqcl
supabase db push
```

- **Windows permission issue**: `~/.supabase/` cannot be created (corporate AD). Workaround: set `SUPABASE_HOME` to `.supabase/` inside the project dir.
- New migration: `supabase migration new <name>` then edit the file in `supabase/migrations/`.
- RLS policies are permissive (educational project).

**Project ref mismatch**: `.env.example` uses `aoscrsfqhtobvbdywqcl`, while `connection.py:18` defaults to `wljpvxicodobqlejffmy`. The `opencode.json` MCP server and CLI command above both reference `aoscrsfqhtobvbdywqcl`. Check which project is live before running CLI commands.

## Architecture

- `app.py` — home page (requires login, shows navigation + logout)
- `pages/0_login.py` — login + registration (two tabs: Entrar / Cadastrar)
- `pages/1_cadastro.py` — profile page (edit name, team, password)
- `pages/2_selecao.py` — group standings (1st/2nd per group) + terceiros draw + group match predictions organized by **3 date tabs** (Rodada 1–3)
- `pages/3_resultado.py` — group predictions display (read-only, date tabs) + knockout bracket picks organized by **5 date tabs** (R32 → Oitavas → Quartas → Semis → Final)
- `pages/4_palpites.py` — comparative table of all participants' picks, organized by date tabs (group + knockout)
- `pages/5_ranking.py` — admin page: enter real match results, live group standings, best third-placed calculation, per-match scoring comparison + participant ranking
- `pages/6_admin.py` — admin panel: view/edit participant palpites (restricted to `admin` flag in session)
- `data/grupos.py` — hardcoded 12 groups A–L (48 teams) + `GRUPOS` dict + `FLAGS` dict
- `data/jogos.py` — match schedule: `GRUPO_RODADAS` (3 rounds × 24 matches), `GRUPO_DATAS`, `GRUPO_JOGOS_DATAS` (per-match datetime BRT), `MATA_MATA_RODADAS` (R32 → Final with per-match dates), `ORDEM_RODADAS_MATA_MATA`
- `utils/auth.py` — `hash_senha()` / `verificar_senha()` (SHA-256, educational only)
- `utils/logic.py` — `montar_bracket()`, `sortear_terceiros()`, `classificar_grupo()`
- `utils/ui_components.py` — reusable Streamlit components (`render_grupo_simples`, etc.)
- `utils/api.py` — external API client for live match data (`worldcup26.ir`, `wheniskickoff.com`) with team name mapping
- `database/connection.py` — Supabase client init
- `database/schema.sql` — full DDL. Tables: `participantes` (has `senha_hash`), `selecoes`, `melhores_terceiros`, `palpites_bracket`, `palpites_grupos` (has `rodada` column), `resultados` (real match scores; `fase` IN grupo/R32/Oitavas/Quartas/Semis/Terceiro/Final).

## Scope

- Educational project (simplified architecture).
- Design reference: `picture/printSimulador.png` (mockup), `picture/grupos.png` (group layout), `picture/classificacao.png` (standings UI).

## Key details

- **Bracket logic**: `montar_bracket()` generates 16 matches when `terceiros` is provided (8 best third-placed vs group winners + cross-pair second-placed). Without third-placed, generates 12 matches (original format).
- **Session state**: `participante_id`, `nome`, and `admin` carry across pages. Pages 2 and 3 require registration first.
- **Date-based tabs**: All match predictions (group + knockout) use Streamlit `st.tabs()` organized by official FIFA dates. Group: 3 Rodadas (Jun 11–27). Knockout: 6 rounds (R32 → Final, Jun 28 – Jul 19).
- **Display names**: UI uses `"🇧🇷 Brasil"` format (flag + name). `render_confronto()` and `_extract_clean_name()` split on first space to extract the clean team name for DB lookups.
- **Shared CSS**: every page loads `assets/styles.css` via `Path.read_text()` at the top of the file. Add new styles there, not inline.
- **MCP servers**: Supabase and Composio MCP configured in `opencode.json` (contains bearer tokens — never commit). There's also a `.mcp.json` in the root for Supabase MCP.
- **External APIs**: `utils/api.py` fetches live match data from `worldcup26.ir` and `wheniskickoff.com` with a `TEAM_MAP` translating FIFA codes and English names to Portuguese.
