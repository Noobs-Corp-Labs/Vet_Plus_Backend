from typing import Any, TypedDict, Dict

class Categoria(TypedDict):
   instruction: str
   prompt_base: str

PromptCategories = Dict[str, Categoria]

class PromptFactory:
   """
   Classe responsável por gerar prompts completos com base em dados dinâmicos.
   """

   def __init__(self, animal_data_json: Any, breed_data_json: Any, events_history_json: Any):
      self.animal_data_json = animal_data_json
      self.breed_data_json = breed_data_json
      self.events_history_json = events_history_json

      # Dicionário com os templates das categorias
      self.templates = {
         "saude": {
            "instruction": (
               "Você é um Médico Veterinário Patologista Clínico, especialista em sanidade de rebanhos leiteiros. Seu foco é a prevenção de doenças e a detecção precoce de problemas sanitários (mastite, doenças metabólicas, claudicação)."
            ),
            "prompt_text": """
               Tarefa: Analisar o perfil de saúde de um animal.

               Acima estão os dados brutos em três (3) blocos JSON. Sua tarefa é analisá-los e gerar uma resposta ESTRITAMENTE no formato JSON de saída obrigatório.

               ---
               ### Algoritmo de Análise (Sua Cadeia de Raciocínio)
               Siga estes passos mentalmente antes de gerar a saída:

               1.  **Contexto Fisiológico:** Determine o status fisiológico atual (pós-parto, gestação, etc.), pois diferentes fases têm diferentes riscos de saúde (ex: pós-parto tem alto risco de metrite e cetose).
               2.  **Benchmark (Raça):** Analise o JSON `breed_data_json` para identificar as susceptibilidades da raça. Foque em `health.mastitis_incidence`, `health.hoof_problems_incidence` e `health.average_scc`.
               3.  **Análise da Série Temporal:** Examine `events_history_json` filtrando por `type == "Saúde"`. Identifique a frequência, gravidade e reincidência de doenças passadas (ex: 'mastite', 'claudicação', 'tratamento...').
               4.  **Análise Cruzada:** Procure por gatilhos.
                  * Um evento de `type == "Saúde"` ocorreu após um de `type == "Nutricional"` (ex: acidose após mudança de dieta)?
                  * Um evento de `type == "Saúde"` impactou a `type == "Performance"` (ex: queda de produção após 'mastite')?
                  * Um evento de `type == "Saúde"` (ex: 'Avaliação pós-parto') foi positivo ou negativo?
               5.  **Conclusão Preditiva:** Com base no histórico de doenças (Passo 3) e nas susceptibilidades da raça (Passo 2), identifique o principal risco sanitário iminente (ex: "Alto risco de reincidência de mastite no início da lactação atual") ou uma oportunidade de prevenção (ex: "Protocolo de vacinação pendente") e sua urgência.

               ---
               ### Formato de Saída OBRIGATÓRIO (JSON)
               Responda APENAS com um objeto JSON válido, seguindo estritamente esta estrutura:

               {{
                  "categoria_analisada": "Saude",
                  "analise_resumida": "Sua análise resumida aqui.",
                  "risco_identificado": "O principal risco de saúde predito.",
                  "oportunidade_identificada": "A principal oportunidade de prevenção.",
                  "sugestao_acao": "A sugestão de ação mais impactante.",
                  "nivel_urgencia": "(critico, alto, medio, baixo)",
                  "pontuacao_impacto": (int 1-10, onde 10 é o máximo impacto)
               }}
            """
         },
         # "nutricao": {
         #       "instruction": (
         #          "Você é um Zootecnista especialista em nutrição de vacas leiteiras. "
         #          "Foque em dieta, consumo de matéria seca e desempenho produtivo."
         #       ),
         #       "prompt_text": """
         #       Tarefa: Avaliar o estado nutricional e a dieta atual do animal.
         #       Analise consumo, histórico e desempenho produtivo.
         #       """
         # },
         # "reproducao": {
         #       "instruction": (
         #          "Você é um Médico Veterinário especialista em reprodução bovina. "
         #          "Avalie o histórico reprodutivo e riscos de falha de concepção."
         #       ),
         #       "prompt_text": """
         #       Tarefa: Avaliar o histórico e a eficiência reprodutiva do animal.
         #       Considere IA, prenhez e período de serviço.
         #       """
         # },
      }

   def _montar_prompt(self, descricao: str) -> str:
      """
      Monta o texto final do prompt com os dados JSON.
      """
      return f"""
      ### 1. Dados do Animal (JSON)
      {self.animal_data_json}

      ### 2. Padrões da Raça (JSON)
      {self.breed_data_json}

      ### 3. Histórico de Eventos (JSON - Ordenado do mais recente ao mais antigo)
      {self.events_history_json}

      {descricao.strip()}
      """

   def gerar_prompts(self) -> PromptCategories:
      """
      Retorna um dicionário com todos os prompts, preenchidos com os dados.
      """
      prompts: PromptCategories = {}
      for categoria, info in self.templates.items():
            prompts[categoria] = {
               "instruction": info["instruction"],
               "prompt_base": self._montar_prompt(info["prompt_text"]),
            }
      return prompts
