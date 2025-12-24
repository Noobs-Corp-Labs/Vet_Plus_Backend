from google import genai
from google.genai import types
from app.config import settings
from app.services.gemini import PromptCategories

client = genai.Client(api_key=settings.gemini_api_key)

async def create_prompt(instruction: str, prompt_base: str):

   response = client.models.generate_content(
      model=settings.gemini_model,
      contents=[prompt_base],
      config=types.GenerateContentConfig(
         system_instruction=instruction
      ),
   )

   return response.text