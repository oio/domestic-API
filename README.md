# Domestic API
The API interface for all the [Domestic AI](https://github.com/oio/domestic-ai) tools. 

## Setup
```
uv sync
```

### .env file
```
ARENA_TOKEN = arena_api_token
ARENA2DISCORD_URL = link_to_the_arena_to_discord_spreadsheet
FIREBASE_SERVICE_ACCOUNT = b64_service_account
```

## Run
```
uv run uvicorn domestic_api:app --host 0.0.0.0 --port 8000
```