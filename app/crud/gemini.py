from google import genai
from google.genai import types
from app.config import settings
from app.services.gemini import PromptCategories

client = genai.Client(api_key=settings.gemini_api_key)

async def create_prompt(prompt: PromptCategories):

   response = client.models.generate_content(
      model=settings.gemini_model,
      contents=[prompt["saude"]["prompt_base"]],
      config=types.GenerateContentConfig(
         system_instruction=prompt["saude"]["instruction"]),
   )

   return response.text