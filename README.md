# Domestic API
The API interface for all the [Domestic AI](https://github.com/oio/domestic-ai) tools. 

## Setup
```
uv sync
```

### .env file
```
PREFIX = roby # or whatever name for your bot
```

## Run
```
uv run uvicorn domestic_api:app --host 0.0.0.0 --port 8000
```