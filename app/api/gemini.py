import json
from typing import Annotated, Any, Dict
from fastapi import APIRouter, HTTPException, Path,  status

from app.utils.parsers import custom_json_encoder, extrair_e_parsear_json
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
        prompts = prompt_factory.gerar_prompts()

        respostas_especialistas: Dict[str, Any] = {}

        categorias_especialistas = ["saude", "nutricao", "performance", "reproduction"]

        for categoria in categorias_especialistas:
            prompt_data = prompts.get(categoria)

            if prompt_data:
                print(f"-> Enviando prompt para a categoria: {categoria}")
                prompt_response_str = await create_prompt(instruction=prompt_data["instruction"], prompt_base=prompt_data["prompt_base"])

                try:
                    json_resposta = extrair_e_parsear_json(prompt_response_str)
                    respostas_especialistas[categoria] = json_resposta
                    print(f"<- Resposta JSON salva para {categoria}.")
                except json.JSONDecodeError as e:
                    # Tratar erro de JSON inválido, se necessário
                    print(f"Erro ao parsear JSON de {categoria}: {e}")
                    respostas_especialistas[categoria] = {"erro": str(e), "resposta_bruta": prompt_response_str}
        saude_json = json.dumps(respostas_especialistas.get("saude", {}), ensure_ascii=False, indent=2, default=custom_json_encoder)
        nutricao_json = json.dumps(respostas_especialistas.get("nutricao", {}), ensure_ascii=False, indent=2, default=custom_json_encoder)
        performance_json = json.dumps(respostas_especialistas.get("performance", {}), ensure_ascii=False, indent=2, default=custom_json_encoder)
        reproduction_json = json.dumps(respostas_especialistas.get("reproduction", {}), ensure_ascii=False, indent=2, default=custom_json_encoder)

        prompt_geral_data = prompts["geral"]

        prompt_final_geral = prompt_geral_data["prompt_base"].replace(
            "{{output_json_agente_nutricional}}", nutricao_json
        ).replace(
            "{{output_json_agente_reprodutivo}}", reproduction_json
        ).replace(
            "{{output_json_agente_saude}}", saude_json
        ).replace(
            "{{output_json_agente_performance}}", performance_json
        )
        
        print("-> Enviando prompt para o Agente Geral (Síntese)")

        resposta_final_str = await create_prompt(
            instruction=prompt_geral_data["instruction"], 
            prompt_base=prompt_final_geral
        )
        return PromptReturn(response=resposta_final_str)

    except HTTPException:
        raise
    except Exception as e:
        print(f"Erro ao gerar o prompt: {e}")
        raise HTTPException(
            status_code=500,
            detail="Erro interno ao gerar o prompt e/ou analisar."
        )