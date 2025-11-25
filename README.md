# nlb-mcp

Unofficial FastMCP server for NLB Singapore Library Catalogue (availability + title search), implemented in Python.

## What’s inside
- Language: Python 3.11+
- Framework: FastMCP (Python), httpx (HTTP), pydantic-settings (env), tenacity (retry)
- Tools (MCP):
  - `health_check` – validate env + startup readiness.
  - `search_titles` – keyword search over BRN/ISBN/Title/Author/Subject.
  - `search_titles_advanced` – fielded search with pagination/sorting.
  - `availability_by_title` – branch-level availability for a title/ISBN/BID.

## Project layout
```
nlb_mcp/
  config.py          # env validation (API keys, base URL, timeout)
  http_client.py     # httpx helper with retry/timeout
  nlb_client.py      # thin NLB REST client wrappers
  models.py          # lightweight normalized response shapes
  server.py          # FastMCP server + tool registration (with basic logging)
help/
  nlb-swagger.json   # upstream API spec for reference
```

## Setup
1) Create a virtualenv and install deps:
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
2) Environment:
```
NLB_API_KEY=your_api_key
NLB_APP_CODE=your_app_code
# optional
NLB_API_BASE=https://openweb.nlb.gov.sg/api/v2/Catalogue
REQUEST_TIMEOUT_MS=10000
```
3) Run locally:
```
fastmcp run nlb_mcp/server.py:create_server
```

## FastMCP Cloud entrypoint
- Preferred: `nlb_mcp/server.py:create_server`
- Direct object exports: `nlb_mcp/server.py:server` (aliases `mcp`, `app`)
FastMCP Cloud can point at `nlb_mcp/server.py:create_server`; it will handle OAuth2 for users. This server only uses NLB `X-Api-Key`/`X-App-Code` from env.

## Auth model
- Client/user auth is handled by FastMCP’s built-in OAuth2 provider; this server does **not** add another layer of user auth.
- NLB API authentication uses env-provided keys only; never accept them from user input or log them.
- For per-user quotas/auditing, rely on FastMCP identity context when available.

## Notes / TODO
- If you want stricter schemas, consider pydantic models for tool inputs/outputs.
- Add caching/rate limits if upstream limits are tight; httpx + tenacity already retry transient errors.
- Logging uses stdlib `logging` (logger name `nlb_mcp`) with secret redaction; extend as needed for metrics or structured logs.
