from pydantic import BaseModel

class PromptReturn(BaseModel):
   response: str