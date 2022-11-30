# импорт нужных библиотек
import telebot
import pickle
import threading
from threading import Thread
import schedule
import time
import GoogleForms_connector as google
import vk_post as vk


# класс с описанием основных функций бота
class BotLogic:
    # конструктор класса
    def __init__(self, bot_, gtgid, gvkid, password):
        self.bot = bot_
        self.group_tg_id = gtgid
        self.group_vk_id = gvkid
        self.password = password

    # функция входа для организатора
    def login(self, message):
        self.convert_from_u()
        self.convert_from_t()
        if message.from_user.id in self.users:
            bot.send_message(message.from_user.id, "Ты уже зашел в аккаунт организатора")
        elif message.from_user.id not in self.tries:
            bot.send_message(message.from_user.id, 'Привет! Введи пароль')
            self.tries[message.from_user.id] = 0
            bot.register_next_step_handler(message, self.get_password)
        elif self.tries[message.from_user.id] < 3:
            bot.register_next_step_handler(message, self.get_password)
        else:
            self.looser(message)

    def get_password(self, message):
        if message.text == self.password:
            if message.from_user.id not in self.users:
                self.users.append(message.from_user.id)
            bot.send_message(message.from_user.id, f"Успешный вход. Добро пожаловать!")
            self.convert_to_u()
        else:
            self.tries[message.from_user.id] += 1
            self.convert_to_t()
            if self.tries[message.from_user.id] == 3:
                self.looser(message)
            else:
                bot.send_message(message.from_user.id,
                                 f"У тебя осталось {3 - self.tries[message.from_user.id]} "
                                 f"{ending[3 - self.tries[message.from_user.id]]}")
                bot.register_next_step_handler(message, self.get_password)

    def looser(self, message):
        bot.send_message(message.from_user.id, "Не пытайся взломать наш бот, мошенник!")

    def convert_from_u(self):
        with open('users.txt', 'rb') as file:
            u = file.read()
            if len(u) == 0:
                self.users = []
            else:
                self.users = pickle.loads(u)

    def convert_to_u(self):
        with open('users.txt', 'wb') as file:
            pickled_obj = pickle.dumps(self.users)
            file.write(pickled_obj)
        file.close()

    def convert_from_t(self):
        with open('tries.txt', 'rb') as file:
            t = file.read()
            if len(t) == 0:
                self.tries = dict()
            else:
                self.tries = pickle.loads(t)

    def convert_to_t(self):
        with open('tries.txt', 'wb') as file:
            pickled_obj = pickle.dumps(self.tries)
            file.write(pickled_obj)
        file.close()

    def func_Masha(self):
        row_form = google.get_relevant_forms(1)
        return row_form

    def func_Vlad(self):
        row_post = vk.GET_RELEVANT_POST(self.group_vk_id)
        if len(row_post) > 0:
            return row_post
        else:
            return [0]

    def func_Maxim(self):
        pass

    def send_to_org(self):
        self.convert_from_u()
        for user in self.users:
            bot.send_message(user, self.func_Masha())

    def send_to_group(self):
        post = self.func_Vlad()
        if post[0] != 0:
            for i in post:
                if 'photo' in i:
                    bot.send_photo(self.group_tg_id, i['photo'], caption=i['text'])
                else:
                    bot.send_message(self.group_tg_id, i['text'])


bot = telebot.TeleBot('5698700350:AAHHkBTJBTnCYLxIBjYCLU54VMH27YPvcJQ')
bot_obj = BotLogic(bot, '-621054336', -200843593, 'Сезам откройся!')
ending = ['', 'попытка', 'попытки']


@bot.message_handler(commands=['start'])
def start_message(message):
    bot_obj.login(message)


def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(1)


schedule.every(5).seconds.do(bot_obj.send_to_group)
schedule.every(3).seconds.do(bot_obj.send_to_org)


Thread(target=schedule_checker).start()
bot.polling(none_stop=True, interval=0)
