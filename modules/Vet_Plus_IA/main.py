import time

import google.generativeai as genai
import os

from tasks.worker import enqueue_tasks, get_progress
from utils import save_list_to_txt, read_file_to_vector

API_KEY = 'SUA_CHAVE'

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-2.0-flash')
# model = genai.GenerativeModel('gemini-2.5-pro')
chat = model.start_chat()

# ask = input("O que gostaria de perguntar? \n: ")
# ask = "Crie 2 perguntas sobre Memória para a disciplina de Sistemas Operacionais. A pergunta tem de ser objetiva com 5 opçõese apenas uma correta. Devolva a resposta no seguinte formato \"**PERGUNTA##RESPOSTA CORRETA##RESPOSTA ERRADA##RESPOSTA ERRADA##RESPOSTA ERRADA##RESPOSTA ERRADA\""

# ask = ("Crie 15 perguntas de nível Fácil sobre utilização das ferramentas dos sistemas operacionais mais importantes do mercado para a disciplina de  Sistema Operacional. Cada pergunta tem de ser objetiva com 5 opções e apenas uma correta. Devolva a resposta no seguinte formato \"PERGUNTA##RESPOSTA CORRETA##RESPOSTA ERRADA##RESPOSTA ERRADA##RESPOSTA ERRADA##RESPOSTA ERRADA\". Remova qualquer outro texto adicional, não adicione nenhum tipo de indice, como \"PERGUNTA 1\", \"PERGUNTA 2\", etc. Não adicione A), B), C), D) e E)")

ask = "Você é um professor universitário do curso de engenharia de software e está elaborando questões para avaliação. Crie 5 perguntas de 
nível Fácil sobre compreensão da necessidade e do funcionamento dos sistemas operacionais para a disciplina de Sistema Operacional.
A pergunta tem de ser objetiva com 5 opçõese apenas uma correta. Devolva a resposta no seguinte formato 
\"(PERGUNTA)##(RESPOSTA CORRETA)##(RESPOSTA ERRADA)##(RESPOSTA ERRADA)##(RESPOSTA ERRADA)##(RESPOSTA ERRADA)\". Remova qualquer outro texto adicional, não adicione nenhum tipo de indice e não inclua o pareteses na hora de fazer a questão"

response = chat.send_message(ask)

rs = response.text
save_list_to_txt(rs, "response.text.txt")
response_text = response.text.strip()
save_list_to_txt(response_text, "response_strip.txt")

aaa1 = response.text.replace("\n","++")
print(aaa1)
# aaa2 = response_text.text.replace("\n","++")
aux1 = response.text.split("\n")
print(aux1)
# aux2 = response_text.text.split("\n")

print(response.text)

# if __name__ == "__main__":
#        enqueue_tasks("Você é um professor universitário do curso de engenharia de software e está elaborando questões para avaliação. Crie 5 perguntas de nível Fácil sobre compreensão da necessidade e do funcionamento dos sistemas operacionais para a disciplina de "
#                      "Sistema Operacional. A pergunta tem de ser objetiva com 5 opçõese apenas uma correta. Devolva a resposta no seguinte formato "
#                      "\"(PERGUNTA)##(RESPOSTA CORRETA)##(RESPOSTA ERRADA)##(RESPOSTA ERRADA)##(RESPOSTA ERRADA)##(RESPOSTA ERRADA)\". Remova qualquer "
#                      "outro texto adicional, não adicione nenhum tipo de indice e não inclua o pareteses na hora de fazer a questão", "SO", "Assunto 1")
#        print(get_progress())

#        enqueue_tasks("Você é um professor universitário do curso de engenharia de software e está elaborando questões para avaliação. Crie 5 perguntas de nível Médio sobre gerenciamento de processos no sistemas operacionais para a disciplina de Sistema Operacional. "
#                      "A pergunta tem de ser objetiva com 5 opçõese apenas uma correta. Devolva a resposta no seguinte formato \"(PERGUNTA)##(RESPOSTA "
#                      "CORRETA)##(RESPOSTA ERRADA)##(RESPOSTA ERRADA)##(RESPOSTA ERRADA)##(RESPOSTA ERRADA)\". Remova qualquer outro texto adicional, não "
#                      "adicione nenhum tipo de indice e não inclua o pareteses na hora de fazer a questão", "SO", "Assunto 2")
#        print(get_progress())

#        enqueue_tasks("Você é um professor universitário do curso de engenharia de software e está elaborando questões para avaliação. Crie 5 perguntas de nível Difícil sobre gerenciamento de memória para a disciplina de Sistema Operacional. A pergunta tem de ser objetiva "
#                      "com 5 opçõese apenas uma correta. Devolva a resposta no seguinte formato \"(PERGUNTA)##(RESPOSTA CORRETA)##(RESPOSTA ERRADA)##(RESPOSTA "
#                      "ERRADA)##(RESPOSTA ERRADA)##(RESPOSTA ERRADA)\". Remova qualquer outro texto adicional, não adicione nenhum tipo de indice e não "
#                      "inclua o pareteses na hora de fazer a questão", "SO", "Assunto 3")
#        print(get_progress())


#        status = ""
#        while status != "Done":
#            print(get_progress())
#            status = get_progress()['status']
#            time.sleep(1)

