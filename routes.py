import os
import callbacks
from typing import Callable, Type
from pydantic import BaseModel
from dotenv import load_dotenv
from params import (
    HaikuRequest, PromptRequest, RemoveBgRequest, ThrowRequest
)

load_dotenv()

prefix = os.getenv("PREFIX")

class Route:
    def __init__(
        self, 
        name: str, 
        method: str, 
        callback: Callable, 
        request_model: Type[BaseModel] = None,
        **kwargs
    ):
        self.name = name
        self.path = f"/{name}"
        self.method = method
        self.callback = callback
        self.request_model = request_model
        self.description = kwargs.get("description", None)
        self.preview = kwargs.get("preview", None)
        self.params = kwargs.get("params", None)
        self.is_slash_command = kwargs.get("is_slash_command", True)
        self.representation = f"{self.path} ({self.method})"
    
    def __repr__(self):
        return self.representation
    
    def __str__(self):
        return self.representation

all_routes = [
    Route("are_you_real", "POST", callbacks.are_you_real, None, description="🤖 Are you real?", preview="🤖 /are_you_real"),
    Route("beep", "POST", callbacks.beep, None),
    Route("bop", "POST", callbacks.error, None),
    Route("btc", "POST", callbacks.btc, None, description="💰 Bitcoin value in USD", preview="💰 /btc"),
    Route("commands", "POST", callbacks.commands, None),
    Route("eth", "POST", callbacks.eth, None, description="💰 Ethereum value in USD", preview="💰 /eth"),
    Route("flip", "POST", callbacks.flip, None, description="🪙 Flip a coin", preview="🪙 /flip"),
    Route("haiku", "POST", callbacks.haiku, HaikuRequest, description="🌸 Create a haiku", preview="🌸 /haiku"),
    Route("help", "POST", callbacks.help, None, description="🛟 All commands", preview="🛟 /help"),
    Route("image", "POST", callbacks.image, PromptRequest, description="🖼️ Generate an image", preview="🖼️ /image"),
    Route("joke", "POST", callbacks.joke, None, description="🤡 Tell me a joke", preview="🤡 /joke"),
    Route("ping", "POST", callbacks.ping, None, description="Ping"),
    Route("pong", "POST", callbacks.error, None, description="Pong"),
    Route(f"{prefix.strip()}", "POST", callbacks.roby, PromptRequest, description="💬 Ask roby", preview=f"💬 /{prefix.strip()}"),
    Route("rembg", "POST", callbacks.rembg, RemoveBgRequest, description="🖼️ Remove background", preview="🖼️ /removebg"),
    Route(f"thanks {prefix.strip()}", "POST", callbacks.thanks, None, description="Thanks", preview="🙏 Thanks", is_slash_command=False),
    Route(f"thank you {prefix.strip()}", "POST", callbacks.thanks, None, description="Thanks", preview="🙏 Thanks", is_slash_command=False),
    Route("throw", "POST", callbacks.throw, ThrowRequest, description="🎲 Dice throw", preview="🎲 /throw"),
    Route("wdyt", "POST", callbacks.wdyt, None, description="What do you think?", preview="🤔 What do you think?"),
    Route("wisdom", "POST", callbacks.wisdom, None, description="🧙 Ask roby for wisdom", preview="🧙 Ask roby for wisdom")
]