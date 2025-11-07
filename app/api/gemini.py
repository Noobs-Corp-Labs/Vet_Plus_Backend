from typing import Annotated
from fastapi import APIRouter, HTTPException, Path,  status

from app.services.gemini import PromptFactory
from app.crud.events import find_by_animal_identifier
from app.crud.animals import find_one_animal
from app.schemas.gemini import PromptReturn
from app.crud.gemini import create_prompt

router = APIRouter()

@router.post("/{animal_identifier}", 
    response_model=PromptReturn,
    status_code=status.HTTP_201_CREATED,
)
async def handle_prompt(
   animal_identifier: Annotated[
        str,
        Path(
            description="Id of the animal to retrieve events",
            example="String"
        )
    ]
):
    try:
        animal_data = await find_one_animal(animal_identifier)
        if animal_data is None:
            raise HTTPException(status_code=404, detail='Animal not found')

        events_data = await find_by_animal_identifier(animal_identifier)
        if events_data is None:
            raise HTTPException(status_code=404, detail='Events are empty, cant analise')

        prompt_factory = PromptFactory(animal_data, animal_data["breed"], events_data)
        prompt = prompt_factory.gerar_prompts()

        prompt_response_str = await create_prompt(prompt)
        return PromptReturn(response=prompt_response_str)

    except HTTPException:
        raise
    except Exception as e:
        print(f"Erro ao gerar o prompt: {e}")
        raise HTTPException(
            status_code=500,
            detail="Erro interno ao gerar o prompt e/ou analisar."
        )