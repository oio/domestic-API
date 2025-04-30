import aiohttp
import dotenv
import logging
from pydantic import BaseModel
import random
import utils

dotenv.load_dotenv()

logger = logging.getLogger(__name__)

async def are_you_real(request):
	return {"result": "idk, are you real?"}

async def beep(request):
	return {"result": "bop"}

async def btc(request):
	async with aiohttp.ClientSession() as session:
		url = "https://api.coinpaprika.com/v1/tickers/btc-bitcoin"
		async with session.get(url) as response:
			data = await response.json()
			price = int(data['quotes']['USD']['price'])
			return {"result": price}

async def commands(request):
	from routes import all_routes
	
	commands_list = []
	for route in all_routes:
		if route.description:
			commands_list.append(f"{route.preview} - {route.description}")
		
	return {"result" : sorted(commands_list)}

async def error(request):
	return {"result" : "```fatal error: rebooting…```"}

async def eth(request):
	async with aiohttp.ClientSession() as session:
		url = "https://api.coinpaprika.com/v1/tickers/eth-ethereum"
		async with session.get(url) as response:
			data = await response.json()
			price = int(data['quotes']['USD']['price'])  # Round to nearest dollar
			return {"result": price}

async def flip(request):
	result = random.choice(['heads', 'tails'])
	return {"result": result}

async def haiku(request):
	if not request.about:
		return {"status": "error", "message": "Please provide a topic for the haiku"} # TODO this is not blocking
	about = request.about
	prompt = f"write a haiku about {about}. An haiku is a 3-line poem with 5-7-5 syllables."
	response = await utils.query_llm(prompt)
	return {"result": response}

async def help(request): 
	return {"result": "Not implemented"}
	system_prompt = "You are a icebreaker bot helping people to break the ice in a conversation. You'll be asked to generate a question the user can answer with a single word or phrase. Just reply with the question. EXAMPLES 'What is your favorite movie?', 'What's your favorite flower?' 'Dog or cat?'. Ask very unusual and funny questions (AVOID TRAVEL DESTINATIONS AND SERIOUS TOPICS)"
	answer_system_prompt = "You are a icebreaker bot. You just asked a question to break the ice. You also need to answer the question with a single word or phrase to give an example. USE FORMULAS LIKE 'mine is ...', 'for me it's ...', 'i personally prefer ...'"
	result = await utils.query_llm(prompt, system_prompt=system_prompt)
	answer_prompt = f"You generated the following icebreak question: {result}. Now also provide your personal answer. Don't repeat the question, just answer using a formula like 'mine is ...', 'for me it's ...', 'i prefer ...'"
	answer = await utils.query_llm(answer_prompt, system_prompt=answer_system_prompt)
	return {"result": result + "\n\n" + answer}

async def image(request):
	prompt = request.prompt
	response = await utils.generate_image(prompt)
	return {"result": response}

async def joke(request):
	class CustomButton(BaseModel):
		label: str
		callback_message: str
	custom_button = await utils.query_llm_structured(prompt="You are an agent creating funny buttons for discord chats. Return a button with a riddle or a joke. Just return the button, no other text. The label is the question, the callback_message is the answer. e. g. label: 'What do you call a magic dog?', callback_message: 'A labracadabrador.'", schema=CustomButton, system_prompt="You are an agent creating a custom button for a discord message. Just return the button.")
	return {"result": {"question": custom_button.label, "answer": custom_button.callback_message}}

async def ping(request):
	return {"result": "pong"}

async def rembg(request): 
	image_url = request.image_url
	image_base64 = await utils.remove_background(image_url)
	return {"result": image_base64}

async def roby(request): 
	prompt = request.prompt
	answer = await utils.query_llm(prompt, system_prompt="You are a discord bot that always provides a 1 sentence answer")
	return {"result": answer}

async def thanks(request):
	return {"result": "you are welcome"}

async def throw(request): 
	faces = request.faces
	return {"result": random.randint(1, faces)}

async def wdyt(request):
	feedbacks = utils.feedback
	feedback = random.choice(feedbacks)
	return {"result": feedback}

async def wisdom(request):
	wisdom = await utils.query_llm(prompt="write a wisdom", system_prompt="You are a mysterious horacle. Return the wisdom, no other text. Just one very short whimsical sentence.")
	return {"result": f"🧙 {wisdom}"}
