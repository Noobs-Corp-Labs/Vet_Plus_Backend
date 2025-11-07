import re
import json

def extrair_e_parsear_json(response_str: str) -> dict | None:
    """
    Extrai e parseia um JSON de uma string de resposta de LLM 
    de forma robusta.
    
    Lida com:
    1. Blocos de código Markdown (```json...```)
    2. JSON "nu" (apenas {...})
    3. JSON "nu" cercado por texto (ex: "Aqui está: {...} Boa sorte!")
    """
    
    json_string_candidata = None

    # Abordagem 1: O método com Regex (o seu método)
    # É o mais confiável se o LLM usar markdown
    match = re.search(r"```(?:json)?\s*([\s\S]*?)```", response_str)
    if match:
        json_string_candidata = match.group(1).strip()
    else:
        # Abordagem 2: Fallback para JSON "nu"
        # Tenta encontrar o primeiro '{' e o último '}'
        start_index = response_str.find('{')
        end_index = response_str.rfind('}')
        
        if start_index != -1 and end_index != -1 and end_index > start_index:
            # Extrai o texto entre as chaves
            json_string_candidata = response_str[start_index : end_index + 1].strip()
        else:
            # Último recurso: talvez a string inteira seja o JSON
            # (ou talvez seja uma mensagem de erro)
            json_string_candidata = response_str.strip()

    # Etapa Final e CRÍTICA: O Parse com try...except
    # Não importa qual string encontramos, ela PODE ser inválida.
    try:
        data = json.loads(json_string_candidata)
        return data
    except json.JSONDecodeError:
        print(f"Erro: Não foi possível fazer o parse do JSON.")
        print(f"String que falhou: {json_string_candidata}")
        return None
