import engine
import telebot
import logging
from bot_token import TOKEN
import texts
from exceptions import WrongValue, NetworkException

bot = telebot.TeleBot(TOKEN)
logging.basicConfig(level=logging.INFO, filename="logs\log.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")


@bot.message_handler(commands=['start', 'help'])
def start_and_help(message):
    bot.send_message(message.chat.id, texts.first_message + texts.exchange_message, parse_mode='markdown')
    logging.info(f'{message.from_user.username} send {message.text}')


@bot.message_handler(commands=['values'])
def command_values(message):
    bot.send_message(message.chat.id, texts.value_message + engine.return_dict_values(), parse_mode='markdown')
    logging.info(f'{message.from_user.username} send {message.text}')


@bot.message_handler(commands=['admin'])
def command_values(message):
    if message.from_user.username in texts.admin_list.values():
        bot.send_message(message.chat.id, texts.admin_message)
        logfile = 'logs\log.log'
        bot.send_document(chat_id=message.chat.id, document=open(logfile, 'rb'))
        logging.info(f'{message.from_user.username} send {message.text}')
    else:
        pass


@bot.message_handler(content_types=['text'])
def get_text(message):
    try:
        text = message.text.split(' ')
        if len(text) != 3:
            raise WrongValue(texts.exchange_message)
        base = str.upper(text[0])
        if base not in texts.value_dict:
            raise WrongValue(texts.value_message + engine.return_dict_values())
        into = str.upper(text[1])
        if into not in texts.value_dict:
            raise WrongValue(texts.value_message + engine.return_dict_values())
        amount = text[2]
        if not amount.isdigit():
            raise WrongValue(texts.exchange_message)
        bot.send_message(message.chat.id, f'Результат обмена {base} в {into} равен '
                                          f'{str(engine.result_exchange(amount, count=engine.count_money(base, into)))}'
                                          f'{into}\nКурс обмена равен {engine.count_money(base, into)}')
    except WrongValue:
        bot.send_message(message.chat.id, f'{texts.exception_message}', parse_mode='markdown')
    except NetworkException:
        bot.send_message(message.chat.id, f'{texts.network_exception}')
    logging.info(f'{message.from_user.username} send {message.text}')


bot.infinity_polling()
