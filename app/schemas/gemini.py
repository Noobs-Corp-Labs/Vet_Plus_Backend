from pydantic import BaseModel

class PromptRequest(BaseModel):
   prompt: str

class PromptReturn(BaseModel):
   response: str