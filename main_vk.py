import os
import json
import random

from dotenv import load_dotenv
import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.exceptions import SecurityCheck, ApiError, ApiHttpError

from tg_logging import create_logger

load_dotenv()
TOKEN_TG = os.getenv('TOKEN_TG')
CHAT_ID_TG_ADMIN = os.getenv('CHAT_ID_TG_ADMIN')
TOKEN_VK = os.getenv('TOKEN_VK')
TOKEN_DF = os.getenv('TOKEN_DF')
URL_DF = 'https://api.dialogflow.com/v1/query'
FALLBACK = 'do_not_understand'


def poll_vk_bot(token):
    try:
        session = vk_api.VkApi(token=token)
        api = session.get_api()
        longpoll = VkLongPoll(session)
        logger.info('VK Bot was run.')
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                send_vk_msg(event, api)
    except (SecurityCheck, ApiError, ApiHttpError) as err:
        logger.warning(err, exc_info=True)


def send_vk_msg(event, api):
    try:
        id = event.user_id
        text = event.text
        answer = get_df_answer(id, text)
        if answer == FALLBACK:
            # Bot keep silence, but you can add action for fallback case
            pass
        else:
            api.messages.send(
                user_id=id,
                message=answer,
                random_id=random.randint(1, 1000)
            )
    except (SecurityCheck, ApiError, ApiHttpError) as err:
        logger.warning(err, exc_info=True)


def get_df_answer(id, query):
    headers = {'Authorization': 'Bearer ' + TOKEN_DF}
    params = {'v': '20150910', 'lang': 'ru', 'query': query, 'sessionId': id}

    try:
        resp = requests.get(URL_DF, headers=headers, params=params)
        return resp.json()['result']['fulfillment']['speech']

    except requests.exceptions.Timeout as err:
        logger.warning(err, exc_info=True)

    except requests.exceptions.HTTPError as err:
        logger.critical(err, exc_info=True)

    except requests.exceptions.ConnectionError as err:
        time.sleep(DELAY_DF)
        logger.warning(err, exc_info=True)


if __name__ == "__main__":
    logger = create_logger(TOKEN_TG, CHAT_ID_TG_ADMIN)
    poll_vk_bot(TOKEN_VK)
