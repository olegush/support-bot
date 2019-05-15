import os
import json

from dotenv import load_dotenv
import requests
from telegram import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.error import TelegramError

from tg_logging import create_logger


load_dotenv()
TOKEN_TG = os.getenv('TOKEN_TG')
CHAT_ID_TG_ADMIN = os.getenv('CHAT_ID_TG_ADMIN')
TOKEN_DF = os.getenv('TOKEN_DF')
URL_DF = 'https://api.dialogflow.com/v1/query'
DELAY_DF = 60
FALLBACK = 'do_not_understand'


def poll_tg_bot(token):
    try:
        updater = Updater(token)
        dp = updater.dispatcher
        dp.add_handler(MessageHandler((Filters.text | Filters.command), send_tg_msg))
        updater.start_polling()
        logger.info('TG Bot was run.')
    except TelegramError as err:
        logger.warning(err, exc_info=True)


def send_tg_msg(bot, update):
    id = update.message.chat_id
    text = update.message.text
    answer = get_df_answer(id, text)

    try:
        if answer == FALLBACK:
            # Bot keep silence, but you can add action for fallback case
            pass
        else:
            bot.send_message(chat_id=id, text=answer)

    except TelegramError as err:
        logger.warning(err)


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


if __name__ == '__main__':
    logger = create_logger(TOKEN_TG, CHAT_ID_TG_ADMIN)
    poll_tg_bot(TOKEN_TG)
