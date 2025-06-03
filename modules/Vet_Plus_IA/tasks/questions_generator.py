import google.generativeai as genai
import os

from utils import save_list_to_txt

API_KEY = 'SUA_CHAVE'

from datetime import datetime

def generate_question(task_todo):

    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-2.0-flash')
        # model = genai.GenerativeModel('gemini-2.5-pro')

        chat = model.start_chat()
        response = chat.send_message(task_todo[0])

        print(response.text)
        # save_list_to_txt(list_resp, "list_resp.txt")

        clean_list = clean_question(response.text)
        save_list_to_txt(clean_list, "clean_list.txt")

        save_quention_db(clean_list, task_todo[1], task_todo[2])
    except Exception as e:
        print(str(e))

def clean_question(answered_question):
    clean_one = answered_question.replace("\n\n", "\n")
    return clean_one.split("\n")

def save_quention_db(question_list, id_subject_objective, id_classification):
    creation_date = datetime.now()
    print("START SAVING")

    save_list_to_txt(question_list, "questions.txt")

    print("DB COMMIT - " + str(question_list))