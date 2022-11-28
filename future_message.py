from telebot import TeleBot
from datetime import datetime
from time import sleep
from threading import Thread
from telebot import types

token = '5462470014:AAHGUVZNObWn3In9Oe6F1ooZ3mffD58n-IU'
channel = '@bot_testt'
bot = TeleBot(token)

future_text = ''
future_date = ''

@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/message':
        bot.send_message(message.from_user.id, "Напиши текст будущего сообщения")
        bot.register_next_step_handler(message, get_text)
    else:
        bot.send_message(message.from_user.id, 'Напиши /message')

def get_text(message):
    global future_text
    future_text = message.text
    bot.send_message(message.from_user.id, 'Напиши желаемую дату отправки сообщения')
    bot.register_next_step_handler(message, get_date)

def get_date(message):
    global future_date
    old_future_date = future_date
    while future_date == old_future_date:
        try:
            future_date = [int(i) for i in message.text.split('-')]
            future_date = datetime(year=future_date[0], month=future_date[1], day=future_date[2], hour=future_date[3], minute=future_date[4])

            keyboard = types.InlineKeyboardMarkup()
            key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
            keyboard.add(key_yes)
            key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
            keyboard.add(key_no)
            question = f"Сообщение ''{future_text}'' будет отправлено в {future_date}"
            bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


        except Exception:
            bot.send_message(message.from_user.id, 'Напиши дату в формате год-месяц-день-часы-минуты')
            bot.register_next_step_handler(message, get_date)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        go = Thread(target=sleep_poster, args=[future_date, [channel, future_date]])
        go.run()
    elif call.data == "no":
        old_future_date = '.'
        bot.send_message(call.message.chat.id, 'Напиши /message для рестарта')
        start(call.message)

def sleep_poster(date_post, message):
    while True:
        if date_post < datetime.now():
            print('Отправили сообщение!')

            bot.send_message(channel, future_text)

            return
        else:
            sleep(60)

bot.polling(none_stop=True, interval=0)




