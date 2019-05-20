import os
import json
import random
import logging

from dotenv import load_dotenv
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.exceptions import SecurityCheck, ApiError, ApiHttpError
from telegram import Bot

from tg_logging import create_logger
from dialogflow_tools import get_answer


FALLBACK = 'do_not_understand'


def poll_vk_bot(token):
    session = vk_api.VkApi(token=token)
    api = session.get_api()
    longpoll = VkLongPoll(session)
    logger.info('VK Bot was run.')
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            send_vk_msg(event, api)


def send_vk_msg(event, api):
    try:
        user_id = event.user_id
        text = event.text
        answer = get_answer(user_id, text)
        if answer == FALLBACK:
            # Bot keep silence, but you can add action for fallback case
            pass
        else:
            api.messages.send(
                user_id=user_id,
                message=answer,
                random_id=random.randint(1, 1000)
            )
    except (SecurityCheck, ApiError, ApiHttpError) as err:
        logging.exception(err)


if __name__ == "__main__":
    load_dotenv()
    TOKEN_VK = os.getenv('TOKEN_VK')
    logger = create_logger(Bot(token=os.getenv('TOKEN_TG')), os.getenv('CHAT_ID_TG_ADMIN'))
    poll_vk_bot(TOKEN_VK)
