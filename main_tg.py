import os
import json
import logging

from dotenv import load_dotenv
from telegram import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.error import TelegramError

from tg_logging import create_logger
from dialogflow_tools import get_answer

DELAY_DF = 60
FALLBACK = 'do_not_understand'


def poll_tg_bot(token):
    updater = Updater(token)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler((Filters.text | Filters.command), send_tg_msg))
    updater.start_polling()
    logger.info('TG Bot was run.')


def send_tg_msg(bot, update):
    chat_id = update.message.chat_id
    text = update.message.text
    answer = get_answer(chat_id, text)

    try:
        if answer == FALLBACK:
            # Bot keep silence, but you can add action for fallback case
            pass
        else:
            bot.send_message(chat_id=chat_id, text=answer)

    except TelegramError as err:
        logging.exception(err)


if __name__ == '__main__':
    load_dotenv()
    TOKEN_TG = os.getenv('TOKEN_TG')
    logger = create_logger(Bot(token=TOKEN_TG), os.getenv('CHAT_ID_TG_ADMIN'))
    poll_tg_bot(TOKEN_TG)
