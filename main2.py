import telebot
from telebot import types
from text import HELLO

token = "6477369209:AAELdd8Lt8cj8m0bbMHewGLgDF9CpSVlYqs"
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = types.InlineKeyboardMarkup(row_width=4)
    keyboard.add(types.InlineKeyboardButton(text="Начать",
                                          callback_data="callback_start_anketa"))
    bot.send_message(message.chat.id, HELLO, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "callback_start_anketa":
        keyboard = types.InlineKeyboardMarkup(row_width=4)
        keyboard.add(types.InlineKeyboardButton(text="26.09",
                                                callback_data="callback_date"),
                     types.InlineKeyboardButton(text="27.09",
                                                callback_data="callback_date"),
                     types.InlineKeyboardButton(text="28.09",
                                                callback_data="callback_date"),
                     types.InlineKeyboardButton(text="29.09",
                                                callback_data="callback_date")
                     )
        bot.send_message(call.message.chat.id, "Дата заполнения анкеты", reply_markup=keyboard)
    elif call.data == "callback_date":
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(types.InlineKeyboardButton(text="Менеджер",
                                                callback_data="callback_manager"),
                     types.InlineKeyboardButton(text="Клиент",
                                                callback_data="callback_client"))
        bot.send_message(call.message.chat.id, "Вы менеджер или клиент?", reply_markup=keyboard)

    elif call.data == "callback_manager":
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        keyboard.add(types.InlineKeyboardButton(text="ДСП",
                                                callback_data="callback_podrazdel"),
                     types.InlineKeyboardButton(text="ДРП",
                                                callback_data="callback_podrazdel"),
                     types.InlineKeyboardButton(text="Меж.деп",
                                                callback_data="callback_podrazdel"),
                     types.InlineKeyboardButton(text="Другое",
                                                callback_data="callback_podrazdel_drugoe")
                     )
        bot.send_message(call.message.chat.id, "Выберите подразделение:", reply_markup=keyboard)

    elif call.data == "callback_client":
        bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Ваше ФИО"), fio_klienta)

    elif call.data == "callback_manager":
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        keyboard.add(types.InlineKeyboardButton(text="ДСП",
                                                callback_data="callback_podrazdel"),
                     types.InlineKeyboardButton(text="ДРП",
                                                callback_data="callback_podrazdel"),
                     types.InlineKeyboardButton(text="Меж.деп",
                                                callback_data="callback_podrazdel"),
                     types.InlineKeyboardButton(text="Другое",
                                                callback_data="callback_podrazdel_drugoe")
                     )
        bot.send_message(call.message.chat.id, "Выберите подразделение:", reply_markup=keyboard)
    elif call.data == "callback_podrazdel_drugoe":
        bot.register_next_step_handler(bot.send_message(call.message.chat.id,"Уточните данные"), podrazdel_drugoe)

    elif call.data == "callback_sotrudnich_drugoe":
        bot.register_next_step_handler(bot.send_message(call.message.chat.id,"Уточните данные"), sotrudnich_drugoe)

    elif call.data == "callback_sotrud_drugoe":
        bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Уточните данные"), sotrud_drugoe)

    elif call.data == "callback_doljnost_drugoe":
        bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Уточните данные"), doljnost_drugoe)


@bot.message_handler(content_types='text')
def podrazdel_drugoe(message):
    bot.register_next_step_handler(bot.send_message(message.chat.id, "Ваше ФИО"), manager_fio)


@bot.message_handler(content_types='text')
def manager_fio(message):
    bot.register_next_step_handler(bot.send_message(message.chat.id, "ФИО Клиента"), fio_klienta)


@bot.message_handler(content_types='text')
def sotrud_drugoe(message):
    bot.register_next_step_handler(bot.send_message(message.chat.id, ("Город офиса клиента. "
                                                                     "Если несколько – напишите через пробел")), region_prodazh)


@bot.message_handler(content_types='text')
def region_prodazh(message):
    bot.register_next_step_handler(bot.send_message(message.chat.id, ("Регионы продаж клиента. "
                                                                      "Если несколько – напишите через пробел")), telefon)

@bot.message_handler(content_types='text')
def telefon(message):
    bot.register_next_step_handler(bot.send_message(message.chat.id, ("Номер телефона клиента ")), email)
@bot.message_handler(content_types='text')
def email(message):
    bot.register_next_step_handler(bot.send_message(message.chat.id, ("e-mail клиента")), doljnost_klienta)


def fio_klienta(message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text="Да",
                                            callback_data="callback_sotrud"),
                 types.InlineKeyboardButton(text="Нет",
                                            callback_data="callback_sotrud"),
                 types.InlineKeyboardButton(text="Работали ранее, но прекратили",
                                            callback_data="callback_sotrud"),
                 types.InlineKeyboardButton(text="Другое",
                                            callback_data="callback_sotrud_drugoe")
                 )
    bot.send_message(message.chat.id, "Ранее было сотрудничество с «Офис Премьер»?", reply_markup=keyboard)

def doljnost_klienta(message):
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(types.InlineKeyboardButton(text="Директор",
                                            callback_data="callback_"),
                 types.InlineKeyboardButton(text="Специалист по закупкам",
                                            callback_data="callback_"),
                 types.InlineKeyboardButton(text="Собственник",
                                            callback_data="callback_"),
                 types.InlineKeyboardButton(text="Директор по оптовому каналу",
                                            callback_data="callback_"),
                 types.InlineKeyboardButton(text="Директор по розничному каналу",
                                            callback_data="callback_"),
                 types.InlineKeyboardButton(text="Другое",
                                            callback_data="callback_doljnost_drugoe")
                 )
    bot.send_message(message.chat.id, "Должность клиента. Если несколько, то дополните позже", reply_markup=keyboard)


@bot.message_handler(content_types='text')
def sotrudnich_drugoe(message):
    bot.register_next_step_handler(bot.send_message(message.chat.id, "Город офиса клиента. Если несколько – напишите через пробел"), start_message)

@bot.message_handler(content_types='text')
def gorod_klienta(message):
    bot.register_next_step_handler(bot.send_message(message.chat.id, "Город офиса клиента. Если несколько – напишите через пробел"), start_message)

@bot.message_handler(content_types='text')
def doljnost_drugoe(message):
    bot.register_next_step_handler(bot.send_message(message.chat.id, "Уточните данные"), start_message)


@bot.message_handler(commands=['button'])
def button_message(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Кнопка")
    item2 = types.KeyboardButton("Тык")
    markup.add(item1, item2)
    bot.send_message(message.chat.id,'Выберите что вам надо',reply_markup=markup)

@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text=="Кнопка":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton("Кнопка 2")
        markup.add(item1)
        bot.send_message(message.chat.id,'Выберите что вам надо',reply_markup=markup)
    elif message.text=="Кнопка 2":
        bot.send_message(message.chat.id,'Спасибо за прочтение статьи!')

bot.infinity_polling()