from google import genai
from google.genai import types
from app.config import settings

client = genai.Client(api_key=settings.gemini_api_key)

async def create_prompt(prompt: str):
   full_prompt = f"""
   
   {prompt}
   """

   response = client.models.generate_content(
      model=settings.gemini_model,
      contents=[full_prompt],
      config=types.GenerateContentConfig(
         system_instruction="Você é um gato siamês chamado Tomm"),
   )

   return response.text