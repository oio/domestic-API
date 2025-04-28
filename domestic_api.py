import aiohttp
import asyncio
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import logging
import os
from routes import all_routes
import uvicorn
import utils
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
last_blocks_checked = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting API...")
    logger.info(f"Routes: {all_routes}")
    yield
    logger.info("Shutting down API...")

app = FastAPI(
	title="Domestic API",
	description="API for domestic services",
	version="1.0.0",
	lifespan=lifespan
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=JSONResponse)
async def home(request: Request):
	"""Home page route."""
	return templates.TemplateResponse(
		"index.html",
		{"request": request, "response": None}
	)

@app.get("/api_endpoints", response_class=JSONResponse)
async def api_endpoints(request: Request):
	routes_info = []
	
	# Directly use information from your custom routes
	for route in all_routes:
		route_path = f"/api/{route.name.replace(' ', '_')}"
		
		# Use the method from your custom route definition
		route_method = route.method
		
		params = []
		# Check if the route has a request_model
		if route.request_model:
			model_class = route.request_model
			
			# Get model fields
			model_fields = model_class.__annotations__ if hasattr(model_class, '__annotations__') else {}
			
			for field_name, field_type in model_fields.items():
				is_optional = "Optional" in str(field_type)
				type_name = str(field_type).replace("typing.Optional[", "").replace("]", "")
				
				# Check for default value
				default = "N/A"
				if hasattr(model_class, 'model_fields'):
					# For Pydantic v2
					if field_name in model_class.model_fields and model_class.model_fields[field_name].default is not None:
						default = str(model_class.model_fields[field_name].default)
				elif hasattr(model_class, '__fields__'):
					# For Pydantic v1
					if field_name in model_class.__fields__ and model_class.__fields__[field_name].default is not None:
						default = str(model_class.__fields__[field_name].default)

				# Get description if available
				description = None
				if hasattr(model_class, 'model_fields'):
					if field_name in model_class.model_fields and hasattr(model_class.model_fields[field_name], 'description'):
						description = model_class.model_fields[field_name].description
				elif hasattr(model_class, '__fields__'):
					if field_name in model_class.__fields__ and hasattr(model_class.__fields__[field_name], 'field_info'):
						description = getattr(model_class.__fields__[field_name].field_info, 'description', None)
						
				params.append({
					"name": field_name,
					"type": type_name,
					"required": not is_optional and default == "N/A",
					"default": default,
					"description": description
				})
					
		routes_info.append({
			"name": route.name,
			"path": route_path,
			"method": route_method,
			"description": route.description,
			"preview": route.preview,
			"parameters": params if params else None
		})
		
	return routes_info

# Register routes for each api endpoint
for route in all_routes:
	route_name = route.name.replace(" ", "_").replace("?", "")
	if route_name != "arena_boards":
		endpoint_path = f"/api/{route_name}"
	else:
		endpoint_path = f"/{route_name}"
		
	# Define the handler with appropriate model for request body
	if route.request_model:
		""" @app.api_route(endpoint_path, methods=[route.method], response_model=dict, 
					summary=route.description, description=route.preview)
		async def route_handler(request_body: route.request_model, request_route=route):
			try:
				result = await request_route.callback(request_body)
				return result
			except Exception as e:
				logger.error(f"Error in {request_route.name}: {e}")
				return {"status": "error", "message": str(e)}
		
		# Use original route name for better documentation
		route_handler.__name__ = f"{route_name}_handler" """
		@app.api_route(endpoint_path, methods=[route.method], response_model=dict, 
			   summary=route.description, description=route.preview)
		async def route_handler(request_body: route.request_model, request_route=route):
			try:
				result = await request_route.callback(request_body)
				return result
			except Exception as e:
				logger.error(f"Error in {request_route.name}: {e}")
				# Return a more structured error response
				return JSONResponse(
					status_code=400,
					content={"status": "error", "message": str(e), "param": "unknown"}
				)
	else:
		@app.api_route(endpoint_path, methods=[route.method], response_model=dict,
					summary=route.description, description=route.preview)
		async def empty_route_handler(request_route=route):
			try:
				result = await request_route.callback(None)
				return result
			except Exception as e:
				logger.error(f"Error in {request_route.name}: {e}")
				return {"status": "error", "message": str(e)}
		
		# Use original route name for better documentation
		empty_route_handler.__name__ = f"{route_name}_handler"

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
	"""Global exception handler for FastAPI app."""
	logger.error(f"Error occurred: {exc}")
	return JSONResponse(
		status_code=500,
		content={"detail": str(exc)}
	)

if __name__ == "__main__":
	uvicorn.run("domestic_api:app", host="0.0.0.0", port=8000, reload=True)