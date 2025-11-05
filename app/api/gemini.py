from fastapi import APIRouter,  status

from app.schemas.gemini import PromptRequest, PromptReturn
from app.services.gemini import create_prompt

router = APIRouter()

@router.post("/", 
    response_model=PromptReturn,
    status_code=status.HTTP_201_CREATED,
)
async def handle_prompt(request: PromptRequest):
   prompt_response_str = await create_prompt(request.prompt)
   return PromptReturn(response=prompt_response_str)
