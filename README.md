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

### Install and run Ollama
You need to have Ollama installed on your machine to run AI functions.
```
brew install ollama
```
Install the required models.
```
ollama pull llama3.2:3b
```
You can change the model by editing `utils.py` and installing a different one.

## Run
```
uv run uvicorn domestic_api:app --host 0.0.0.0 --port 8000
```

## Endpoints documentation
The endpoints are documented with Swagger. You can access the documentation at `http://0.0.0.0:8000/docs`.

## Implement new endpoints
Update `all_routes` in routes.py
```python

all_routes = [
    Route("endpoint_name", "POST", callbacks.name_of_callback, None, description="🤖 endpoint description (for documentation)", preview="🤖 /endpoint_name (for documentation)"), # Leave None for endpoints without parameter or implement a parameter type under params.py 
	# ...
]
```
Create a callback in callbacks.py. Callbacks' outputs must be objects `{"result": value}`.
```python 
	async def basic_callback(request):
	return {"result": "some response"}

	async def callback_with_input_params(request): 
	parameter = request.parameter
	return {"result": random.randint(1, parameter)}
```
If needed, also set a request class for those that need input parameters.
```python
class NumberRequest(BaseModel):
	prompt: int = Field(..., description="a int")
```