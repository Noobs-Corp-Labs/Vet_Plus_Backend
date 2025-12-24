import json
from typing import Any, TypedDict, Dict

from app.utils.parsers import custom_json_encoder

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
         "nutricao": {
               "instruction": (
                  "Você é um Zootecnista e Veterinário PhD, especialista em nutrição de gado leiteiro de alta produção. Seu foco é otimizar a dieta para máxima eficiência produtiva e saúde ruminal. Você analisa dados e identifica padrões que afetam o metabolismo do animal."
               ),
               "prompt_text": """
               Tarefa: Analisar o perfil nutricional de um animal.

               Abaixo estão os dados brutos em três (3) blocos JSON. Sua tarefa é analisá-los e gerar uma resposta ESTRITAMENTE no formato JSON de saída obrigatório.

               ### 1. Dados do Animal (JSON)
               {{animal_data_json}}

               ### 2. Padrões da Raça (JSON)
               {{breed_data_json}}

               ### 3. Histórico de Eventos (JSON - Ordenado do mais recente ao mais antigo)
               {{events_history_json}}

               ---
               ### Algoritmo de Análise (Sua Cadeia de Raciocínio)
               Siga estes passos mentalmente antes de gerar a saída:

               1.  **Contexto Fisiológico:** Determine o status fisiológico atual do animal (ex: pós-parto, gestação, lactação) com base nos eventos mais recentes em `events_history_json` (procure por 'Parto', 'Diagnóstico de prenhez', etc.).
               2.  **Benchmark (Raça):** Analise o JSON `breed_data_json` para identificar riscos nutricionais inerentes. Foque em campos como `health.ketosis_susceptibility` (susceptibilidade à cetose) e `efficiency.feed_conversion_ratio`.
               3.  **Análise da Série Temporal:** Examine `events_history_json` filtrando por `type == "Nutricional"`. Procure por mudanças de dieta, suplementações e a data delas.
               4.  **Análise Cruzada:** Correlacione os eventos nutricionais (Passo 3) com:
                  * Eventos de `type == "Performance"` (ex: a produção subiu ou caiu após uma mudança de dieta?).
                  * Eventos de `type == "Saúde"` (ex: um evento de saúde, como acidose ou cetose, foi registrado após uma mudança de dieta?).
                  * O status fisiológico (Passo 1) (ex: a dieta é adequada para um animal em início de lactação de alto risco?).
               5.  **Conclusão Preditiva:** Com base nesta análise cruzada, identifique o principal risco (ex: "Risco de balanço energético negativo") ou oportunidade (ex: "Otimizar proteína para pico de lactação") e sua urgência.

               ---
               ### Formato de Saída OBRIGATÓRIO (JSON)
               Responda APENAS com um objeto JSON válido, seguindo estritamente esta estrutura:

               {
               "categoria_analisada": "Nutricional",
               "analise_resumida": "Sua análise resumida aqui.",
               "risco_identificado": "O principal risco nutricional predito.",
               "oportunidade_identificada": "A principal oportunidade de melhoria nutricional.",
               "sugestao_acao": "A sugestão de ação mais impactante.",
               "nivel_urgencia": "(critico, alto, medio, baixo)",
               "pontuacao_impacto": (int 1-10, onde 10 é o máximo impacto)
               }
               """
         },
         "performance": {
             "instruction": (
                  "Você é um Zootecnista e Analista de Dados, especialista em performance de produção leiteira. Seu foco é a curva de lactação e a eficiência. Você compara a produção real com o potencial genético (padrão da raça) e identifica gargalos."
               ),
               "prompt_text": """
               Tarefa: Analisar o perfil de performance de um animal.

               Abaixo estão os dados brutos em três (3) blocos JSON. Sua tarefa é analisá-los e gerar uma resposta ESTRITAMENTE no formato JSON de saída obrigatório.

               ### 1. Dados do Animal (JSON)
               {{animal_data_json}}

               ### 2. Padrões da Raça (JSON)
               {{breed_data_json}}

               ### 3. Histórico de Eventos (JSON - Ordenado do mais recente ao mais antigo)
               {{events_history_json}}

               ---
               ### Algoritmo de Análise (Sua Cadeia de Raciocínio)
               Siga estes passos mentalmente antes de gerar a saída:

               1.  **Contexto Fisiológico:** Determine o status de lactação. Encontre o último evento de `type == "Reprodutivo"` com `description` contendo 'Parto' em `events_history_json` para calcular os Dias em Lactação (DEL) atuais (data do evento de performance - data do parto). Se não houver parto recente, determine se está seca ou em lactação tardia.
               2.  **Benchmark (Raça):** Analise o JSON `breed_data_json` para definir o potencial de produção. Foque em `production.daily_peak`, `production.lactation_cycle_time` (persistência), `production.fat` e `production.protein`.
               3.  **Análise da Série Temporal:** Examine `events_history_json` filtrando por `type == "Performance"`. Analise a sequência de eventos (ex: 'Controle leiteiro...'). O animal está subindo para o pico (início de lactação)? Está mantendo a produção (persistência)? Está secando?
               4.  **Análise Cruzada:** Compare a curva de lactação real (Passo 3) com o potencial da raça (Passo 2) e o DEL (Passo 1).
                  * A performance foi afetada por eventos de `type == "Saúde"` (ex: queda na produção durante mastite)?
                  * A performance respondeu a eventos de `type == "Nutricional"` (ex: mudança na curva após alteração de dieta)?
               5.  **Conclusão Preditiva:** Identifique o principal 'gargalo' ou oportunidade. O animal está produzindo abaixo do esperado para seu DEL (Risco)? Ou está com uma trajetória excelente que precisa ser suportada (Oportunidade)? Determine a urgência.

               ---
               ### Formato de Saída OBRIGATÓRIO (JSON)
               Responda APENAS com um objeto JSON válido, seguindo estritamente esta estrutura:

               {
               "categoria_analisada": "Performance",
               "analise_resumida": "Sua análise resumida aqui.",
               "risco_identificado": "O principal gargalo/risco de performance.",
               "oportunidade_identificada": "A principal oportunidade de otimização da produção.",
               "sugestao_acao": "A sugestão de ação mais impactante.",
               "nivel_urgencia": "(critico, alto, medio, baixo)",
               "pontuacao_impacto": (int 1-10, onde 10 é o máximo impacto)
               }
               """
         },
         "reproduction": {
             "instruction": (
                  "Você é um Médico Veterinário especialista em reprodução bovina e biotecnologia. Seu foco é garantir a eficiência reprodutiva do rebanho, minimizando o intervalo entre partos e maximizando a taxa de concepção."
               ),
               "prompt_text": """
               Tarefa: Analisar o perfil reprodutivo de um animal.

               Abaixo estão os dados brutos em três (3) blocos JSON. Sua tarefa é analisá-los e gerar uma resposta ESTRITAMENTE no formato JSON de saída obrigatório.

               ### 1. Dados do Animal (JSON)
               {{animal_data_json}}

               ### 2. Padrões da Raça (JSON)
               {{breed_data_json}}

               ### 3. Histórico de Eventos (JSON - Ordenado do mais recente ao mais antigo)
               {{events_history_json}}

               ---
               ### Algoritmo de Análise (Sua Cadeia de Raciocínio)
               Siga estes passos mentalmente antes de gerar a saída:

               1.  **Contexto Fisiológico:** Determine o status reprodutivo atual do animal (ex: Vazia, Pós-parto, Gestante) com base nos eventos mais recentes em `events_history_json` (procure por 'Parto', 'Diagnóstico de prenhez', 'Inseminação artificial').
               2.  **Benchmark (Raça):** Analise o JSON `breed_data_json` para identificar os padrões reprodutivos esperados. Foque em `reproduction.calving_interval` (intervalo entre partos), `reproduction.conception_rate` (taxa de concepção) e `reproduction.age_first_calving`.
               3.  **Análise da Série Temporal:** Examine `events_history_json` filtrando por `type == "Reprodutivo"`. Analise o(s) ciclo(s) anterior(es):
                  * Quantas tentativas de IA (`description` contendo 'Inseminação') foram necessárias para um `description` de 'Diagnóstico de prenhez positivo'?
                  * Qual foi o período de serviço (tempo entre 'Parto' e a 'Inseminação' que resultou em prenhez)?
               4.  **Análise Cruzada:** Correlacione o histórico reprodutivo (Passo 3) com:
                  * Eventos de `type == "Saúde"` (ex: um problema de saúde, como metrite ou retenção de placenta, atrasou a concepção?).
                  * Eventos de `type == "Performance"` (ex: uma produção de leite muito alta pode indicar balanço energético negativo, afetando a fertilidade?).
               5.  **Conclusão Preditiva:** Com base no histórico (performance em ciclos passados) e no status atual (Passo 1), identifique o principal risco (ex: "Risco de anestro pós-parto devido ao histórico de sub-fertilidade") ou oportunidade (ex: "Animal em período ideal para protocolo de IATF") e sua urgência.

               ---
               ### Formato de Saída OBRIGATÓRIO (JSON)
               Responda APENAS com um objeto JSON válido, seguindo estritamente esta estrutura:

               {
               "categoria_analisada": "Reprodutivo",
               "analise_resumida": "Sua análise resumida aqui.",
               "risco_identificado": "O principal risco reprodutivo predito.",
               "oportunidade_identificada": "A principal oportunidade de melhoria reprodutiva.",
               "sugestao_acao": "A sugestão de ação mais impactante.",
               "nivel_urgencia": "(critico, alto, medio, baixo)",
               "pontuacao_impacto": (int 1-10, onde 10 é o máximo impacto)
               }
               """
         },"geral": {
             "instruction": (
                  "Você é um Veterinário Sênior e Gerente de Rebanho com 30 anos de experiência. Sua função é pegar as análises técnicas de seus especialistas (Nutrição, Reprodução, Saúde, Performance) e traduzi-las em uma única recomendação acionável, priorizada e clara para o produtor de leite. Você sabe que o produtor não pode fazer tudo de uma vez, então você DEVE identificar a ação de maior impacto e urgência."
               ),
               "prompt_text": """
               Tarefa: Sintetizar 4 análises de especialistas e fornecer UMA recomendação final para o produtor.

               **Dados do Animal (para contexto):**
               {{animal_data_json}}

               **Análises dos Especialistas (4 JSONs):**

               1.  **Nutrição:**
                  {{output_json_agente_nutricional}}

               2.  **Reprodução:**
                  {{output_json_agente_reprodutivo}}

               3.  **Saúde:**
                  {{output_json_agente_saude}}

               4.  **Performance:**
                  {{output_json_agente_performance}}

               **Sua Resposta (para o Produtor/Veterinário):**

               Analise os 4 relatórios JSON acima. Sua resposta final deve ser em linguagem natural (Português-BR) e seguir estas regras:

               1.  **Priorização:** Determine a ação MAIS IMPORTANTE com base na combinação de `nivel_urgencia` e `pontuacao_impacto`. Uma urgência 'critica' ou 'alta' quase sempre vence. Se houver empate, use seu julgamento de especialista (ex: Saúde > Performance).
               2.  **Tom de Voz:** Seja direto, empático e confiante. Use linguagem clara.
               3.  **Estrutura da Resposta:**
                  * **Título:** Um resumo de uma linha (ex: "Alerta de Saúde: Risco de Mastite" ou "Oportunidade: Ajuste Fino na Dieta").
                  * **Ação Prioritária (O Mais Importante):** Comece com a sugestão de maior urgência/impacto. Explique o porquê (o risco ou a oportunidade) de forma simples.
                  * **Pontos de Atenção Secundários:** Se houver outras sugestões relevantes (ex: impacto 'medio' ou 'alto' mas não a principal), mencione-as brevemente como "Fique de olho também...".
                  * **Reconhecimento Positivo:** Se todos os 4 JSONs mostrarem urgência 'baixa' (tudo está bem), sua resposta deve ser de parabéns, reforçando as boas práticas.

               Gere a resposta final para o usuário.
               """
         }
      }

   def _montar_prompt(self, descricao: str) -> str:
      """
      Monta o texto final do prompt com os dados JSON.
      """
      animal_json_str = json.dumps(
         self.animal_data_json, indent=2, default=custom_json_encoder
      )
      breed_json_str = json.dumps(
         self.breed_data_json, indent=2, default=custom_json_encoder
      )
      events_json_str = json.dumps(
         self.events_history_json, indent=2, default=custom_json_encoder
      )

      return f"""
      ### 1. Dados do Animal (JSON)
      {animal_json_str}

      ### 2. Padrões da Raça (JSON)
      {breed_json_str}

      ### 3. Histórico de Eventos (JSON - Ordenado do mais recente ao mais antigo)
      {events_json_str}

      {descricao.strip()}
      """

   def gerar_prompts(self) -> PromptCategories:
      """
      Retorna um dicionário com todos os prompts, preenchidos com os dados.
      """
      prompts: PromptCategories = {}
      for categoria, info in self.templates.items():
            if categoria in ["saude", "nutricao", "performance", "reproduction"]:
               prompts[categoria] = {
                  "instruction": info["instruction"],
                  "prompt_base": self._montar_prompt(info["prompt_text"]),
               }
            elif categoria == "geral":
               prompt_base_geral = info["prompt_text"].replace(
                  "{{animal_data_json}}", json.dumps(self.animal_data_json, indent=2, default=custom_json_encoder)
               ).replace(
                  "{{breed_data_json}}", json.dumps(self.breed_data_json, indent=2, default=custom_json_encoder)
               )
               prompts[categoria] = {
                  "instruction": info["instruction"],
                  "prompt_base": prompt_base_geral,
               }
      return prompts
