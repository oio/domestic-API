from pydantic import BaseModel, Field
from typing import Optional

class HaikuRequest(BaseModel):
	about: str = Field(default="the moon", description="Topic for the haiku")

class EmptyRequest(BaseModel):
	pass

class ImageRequest(BaseModel):
	prompt: Optional[str] = Field(default="A shiba inu", description="The image to generate")

class PromptRequest(BaseModel):
	prompt: str = Field(default="What's up?", description="Message for Roby")

class ThrowRequest(BaseModel):
	faces: int = Field(default=6, description="Number of faces on the dice", ge=2)

class RemoveBgRequest(BaseModel):
	image_url: Optional[str] = Field(default="https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/Octopus2.jpg/1920px-Octopus2.jpg", description="URL of the image to process")