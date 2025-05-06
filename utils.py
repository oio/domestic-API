import aiohttp
from dotenv import load_dotenv
import logging
import ollama
from ollama import chat
import os
from operations_queue import queue_llm, queue_image
import tools

load_dotenv()

logger = logging.getLogger(__name__)
ollama_client = ollama.AsyncClient("http://0.0.0.0:11434")

"""
LLM / GENERATIVE AI
"""

#async def query_llm(prompt, system_prompt=None, model="llama3.2:3b"):
async def query_llm(prompt, system_prompt=None):
	model = os.environ["OLLAMA_MODEL"]
	response = await ollama_client.generate(model=model, prompt=prompt, system=system_prompt)
	logger.info(f"Response: {response}")
	return response.get("response")

#async def query_llm_structured(prompt, schema, system_prompt=None, model="llama3.2:3b"):
async def query_llm_structured(prompt, schema, system_prompt=None):
	model = os.environ["OLLAMA_MODEL"]
	async def _execute_llm_structured(prompt, schema, system_prompt, model):
		response = chat(
			model=model,
			format=schema.model_json_schema(),
			messages=[
				{
					"role": "system",
					"content": system_prompt
				},
				{
					"role": "user",
					"content": prompt
				}
			], 
			tools = [tools.now, tools.iso_to_datetime, tools.datetime_to_iso],
		)
		parsed_response = schema.model_validate_json(response.message.content)
		logger.info(f"Parsed response: {parsed_response}")
		return parsed_response
		
	# Queue the structured LLM request
	return await queue_llm(_execute_llm_structured, prompt, schema, system_prompt, model)

async def generate_image(prompt, width=512, height=512):
	async def _execute_image_gen(prompt, width, height):
		url = "http://0.0.0.0:8042/generate"
		payload = {
			"prompt": prompt,
			"width": width,
			"height": height,
			"source": "discord"
		}
		async with aiohttp.ClientSession() as session:
			async with session.post(url, json=payload) as response:
				data = await response.json()
				# Log all data except image_base64 to avoid cluttering logs
				log_data = {k: v for k, v in data.items() if k != 'image_base64'}
				logger.info(f"Image generation response: {log_data}")
				b64 = data.get("image_base64", "")
				generation_time = data.get("generation_time_s", 0)
				total_energy_nespresso = data.get("total_energy_nespresso", 0)
				return {"b64": b64, "generation_time": generation_time, "total_energy_nespresso": total_energy_nespresso}
	
	# Queue the image generation request
	return await queue_image(_execute_image_gen, prompt, width, height)

async def remove_background(image_url):
	"""
	Remove background from image at given URL
	
	Args:
		image_url: URL of the image to process
		
	Returns:
		Dict with base64 encoded image without background
	"""
	url = "http://0.0.0.0:8008/rembg"
	payload = {
		"image_url": image_url
	}
	async with aiohttp.ClientSession() as session:
		async with session.post(url, json=payload) as response:
			data = await response.json()
			return data.get("image_base64")

"""
OTHER
"""

feedback = [
	"that sucks",
	"it's great!",
	"good idea!",
	"i'm not sure",
	"i wouldn't be so enthusiastic about it",  
	"forget it",
	"it's the best thing i've ever seen",
	"sick",
	"no",
	"what?",
	"i can't think",
	'more "tangible" '
]