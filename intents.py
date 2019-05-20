import os
import json

from dotenv import load_dotenv
import requests


def add_intent(intent):
    token = os.getenv('TOKEN_DF_DEV')
    url = 'https://api.dialogflow.com/v1/intents'
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }
    resp = requests.post(url, headers=headers, data=json.dumps(intent))


def get_intent(filepath):
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
        yield intent


if __name__ == '__main__':
    load_dotenv()
    for intent in get_intent('questions.json'):
        add_intent(intent)
