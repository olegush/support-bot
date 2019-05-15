import os
import json

from dotenv import load_dotenv
import requests


load_dotenv()
TOKEN_DF_DEV = os.getenv('TOKEN_DF_DEV')
URL_DF = 'https://api.dialogflow.com/v1/intents'
QUESTIONS_PATH = 'questions.json'


def add_intent(intent):
    headers = {
        'Authorization': 'Bearer ' + TOKEN_DF_DEV,
        'Content-Type': 'application/json'
    }
    resp = requests.post(URL_DF, headers=headers, data=json.dumps(intent))


def get_questions(filepath):
    with open(filepath) as file:
        data = json.loads(file.read())
    intent = {}
    for topic, questions in data.items():
        intent['name'] = topic
        intent['responses'] = [{
            'messages': [{
                'speech': questions['answer'],
                'type': 0
            }]
        }]
        intent['userSays'] = []
        for question in questions['questions']:
            intent['userSays'].append({
                'data': [{
                    'text': question
                }]
            })
        add_intent(intent)


if __name__ == '__main__':
    get_questions(QUESTIONS_PATH)
