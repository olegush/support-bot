import os

import requests


def get_answer(sess_id, query):
    token = os.getenv('TOKEN_DF')
    url = 'https://api.dialogflow.com/v1/query'
    headers = {'Authorization': 'Bearer ' + token}
    params = {'v': '20150910', 'lang': 'ru', 'query': query, 'sessionId': sess_id}

    try:
        resp = requests.get(url, headers=headers, params=params)
        return resp.json()['result']['fulfillment']['speech']

    except requests.exceptions.Timeout as err:
        logging.exception(err)

    except requests.exceptions.ConnectionError as err:
        time.sleep(DELAY_DF)
        logging.exception(err)
