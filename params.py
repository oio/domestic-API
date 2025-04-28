from pydantic import BaseModel, Field
from typing import Optional

class HaikuRequest(BaseModel):
	about: str = Field(default="the moon", description="Topic for the haiku")

class EmptyRequest(BaseModel):
	pass

class PromptRequest(BaseModel):
	prompt: str = Field(..., description="Message for Roby")

class ThrowRequest(BaseModel):
	faces: int = Field(default=6, description="Number of faces on the dice", ge=2)

class RemoveBgRequest(BaseModel):
	image_url: Optional[str] = Field(..., description="URL of the image to process")