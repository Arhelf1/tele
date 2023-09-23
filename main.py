import telebot
from telebot import types
from text import HELLO
from db import init_db, add_message, add_excel, update_message, id_search, get_db, get_max_id
import random
import re

token = "6380116131:AAEcboCnRR8Inldj914AKc2oBRRG429jZZY"
# token = "6477369209:AAELdd8Lt8cj8m0bbMHewGLgDF9CpSVlYqs"
# token = "6283254956:AAH3Nxld442j6t9WEj6x7cFghcxNavhbFKQ"
bot = telebot.TeleBot(token)
iid = {0: 1}


@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = types.InlineKeyboardMarkup(row_width=4)
    keyboard.add(types.InlineKeyboardButton(text="Начать",
                                            callback_data="callback_start_anketa"))
    bot.send_message(message.chat.id, HELLO, reply_markup=keyboard,parse_mode='Markdown')
    init_db()
    # get_exel()
    print(message.chat.id)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "callback_start_anketa":
        result = {a: '' for a in range(19)}
        result[18] = call.message.chat.id
        add_message(data=result)
        update_message(id_=id_search(user_id=call.message.chat.id), field='user_id', mean=call.message.chat.id)
        keyboard = types.InlineKeyboardMarkup(row_width=4)
        keyboard.add(types.InlineKeyboardButton(text="26.09",
                                                callback_data="callback_date_26.09"),
                     types.InlineKeyboardButton(text="27.09",
                                                callback_data="callback_date_27.09"),
                     types.InlineKeyboardButton(text="28.09",
                                                callback_data="callback_date_28.09"),
                     types.InlineKeyboardButton(text="29.09",
                                                callback_data="callback_date_29.09")
                     )
        bot.send_message(call.message.chat.id, "Дата заполнения анкеты", reply_markup=keyboard)

    elif "callback_date" in call.data:
        # results[0] = call.data.strip("callback_date")
        if call.data.strip("callback_date") != '':
            update_message(id_=id_search(user_id=call.message.chat.id), field='data',
                           mean=call.data.strip("callback_date"))
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(types.InlineKeyboardButton(text="Менеджер",
                                                callback_data="callback_role_m"),
                     types.InlineKeyboardButton(text="Клиент",
                                                callback_data="callback_role_c"))
        bot.send_message(call.message.chat.id, "Вы менеджер или клиент?", reply_markup=keyboard)

    elif "callback_role_m" == call.data:
        # results[0] = call.data.strip("callback_date")
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(types.InlineKeyboardButton(text="Верно",
                                                callback_data="callback_manager"),
                     types.InlineKeyboardButton(text="Назад",
                                                callback_data="callback_date"))
        bot.send_message(call.message.chat.id, "Вы выбрали менеджер", reply_markup=keyboard)

    elif call.data == "callback_manager":
        # results[1] = call.data.strip("callback_")
        update_message(id_=id_search(user_id=call.message.chat.id), field='role',
                       mean=call.data.strip("callback_"))
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        keyboard.add(types.InlineKeyboardButton(text="ДСП",
                                                callback_data="callback_m_division_dsp"),
                     types.InlineKeyboardButton(text="ДРП",
                                                callback_data="callback_m_division_drp"),
                     types.InlineKeyboardButton(text="Меж.деп",
                                                callback_data="callback_m_division_mez"),
                     types.InlineKeyboardButton(text="Другое",
                                                callback_data="callback_m_division_d")
                     )
        bot.send_message(call.message.chat.id, "Выберите подразделение:", reply_markup=keyboard)

    elif call.data == "callback_m_division_d":
        bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Уточните данные"), m_m_fio)

    elif "callback_m_division" in call.data:
        if "dsp" in call.data:
            # results[2] = "ДСП"
            update_message(id_=id_search(user_id=call.message.chat.id), field='division',
                           mean="ДСП")
        elif "drp" in call.data:
            # results[2] = "ДРП"
            update_message(id_=id_search(user_id=call.message.chat.id), field='division',
                           mean="ДРП")
        elif "mez" in call.data:
            # results[2] = "Меж.деп"
            update_message(id_=id_search(user_id=call.message.chat.id), field='division',
                           mean="Меж.деп")
        bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Ваше ФИО"), m_fio)

    elif call.data == "callback_m_coop_d":
        bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Уточните данные"), m_city)

    elif "callback_m_coop" in call.data:
        if "yes" in call.data:
            # results[5] = "Да"
            update_message(id_=id_search(user_id=call.message.chat.id), field='coop',
                           mean="Да")
        elif "no" in call.data:
            # results[5] = "Нет"
            update_message(id_=id_search(user_id=call.message.chat.id), field='coop',
                           mean="Нет")
        elif "worked" in call.data:
            # results[5] = "Работали ранее, но прекратили"
            update_message(id_=id_search(user_id=call.message.chat.id), field='coop',
                           mean="Работали ранее, но прекратили")
        bot.register_next_step_handler(
            bot.send_message(call.message.chat.id, "Город офиса клиента. Если несколько – введите через пробел"),
            m_region)


    elif call.data == "callback_m_post_d":
        bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Уточните данные"), m_point)


    elif "callback_m_post" in call.data:

        print(call.data)

        if "dir" in call.data:

            # results[10] = "Директор"

            update_message(id_=id_search(user_id=call.message.chat.id), field='post',

                           mean="Директор")

            keyboard = types.InlineKeyboardMarkup()

            keyboard.row(types.InlineKeyboardButton(text="Собственник",

                                                    callback_data="callback_m_post_del_Dir_Sob"))

            keyboard.row(types.InlineKeyboardButton(text="Директор по оптовому каналу",

                                                    callback_data="callback_m_post_del_Dir_Opt"))

            keyboard.row(types.InlineKeyboardButton(text="Директор по розничному каналу",

                                                    callback_data="callback_m_post_del_Dir_Roz"))

            keyboard.row(types.InlineKeyboardButton(text="Специалист по закупкам",

                                                    callback_data="callback_m_post_del_Dir_Zak"))

            keyboard.row(types.InlineKeyboardButton(text="Далее",

                                                    callback_data="callback_m_post_dalee"))

            bot.send_message(text="Выбрано: Директор \nДолжность клиента. Если несколько, то дополните позже.",

                             chat_id=call.message.chat.id, reply_markup=keyboard)


        elif "Dir" in call.data and "Sob" in call.data and "Opt" not in call.data and "Roz" not in call.data and "Zak" not in call.data:

            # results[10] = "Директор"

            update_message(id_=id_search(user_id=call.message.chat.id), field='post',

                           mean="Директор, Собственник")

            keyboard = types.InlineKeyboardMarkup()

            keyboard.row(types.InlineKeyboardButton(text="Директор по оптовому каналу",

                                                    callback_data="callback_m_post_del_Dir_Sob_Opt"))

            keyboard.row(types.InlineKeyboardButton(text="Директор по розничному каналу",

                                                    callback_data="callback_m_post_del_Dir_Sob_Roz"))

            keyboard.row(types.InlineKeyboardButton(text="Специалист по закупкам",

                                                    callback_data="callback_m_post_del_Dir_Sob_Zak"))

            keyboard.row(types.InlineKeyboardButton(text="Далее",

                                                    callback_data="callback_m_post_dalee"))

            bot.send_message(
                text="Выбрано: Директор, Собственник \nДолжность клиента. Если несколько, то дополните позже.",

                chat_id=call.message.chat.id, reply_markup=keyboard)


        elif "Dir" in call.data and "Sob" not in call.data and "Opt" in call.data and "Roz" not in call.data and "Zak" not in call.data:

            # results[10] = "Директор"

            update_message(id_=id_search(user_id=call.message.chat.id), field='post',

                           mean="Директор, Директор по оптовому каналу")

            keyboard = types.InlineKeyboardMarkup()

            keyboard.row(types.InlineKeyboardButton(text="Собственник",

                                                    callback_data="callback_m_post_del_Dir_Opt_Sob"))

            keyboard.row(types.InlineKeyboardButton(text="Директор по розничному каналу",

                                                    callback_data="callback_m_post_del_Dir_Opt_Roz"))

            keyboard.row(types.InlineKeyboardButton(text="Специалист по закупкам",

                                                    callback_data="callback_m_post_del_Dir_Opt_Zak"))

            keyboard.row(types.InlineKeyboardButton(text="Далее",

                                                    callback_data="callback_m_post_dalee"))

            bot.send_message(
                text="Выбрано: Директор, Директор по оптовому каналу \nДолжность клиента. Если несколько, то дополните позже.",

                chat_id=call.message.chat.id, reply_markup=keyboard)


        elif "Dir" in call.data and "Sob" not in call.data and "Opt" not in call.data and "Roz" in call.data and "Zak" not in call.data:

            # results[10] = "Директор"

            update_message(id_=id_search(user_id=call.message.chat.id), field='post',

                           mean="Директор, Директор по розничному каналу")

            keyboard = types.InlineKeyboardMarkup()

            keyboard.row(types.InlineKeyboardButton(text="Собственник",

                                                    callback_data="callback_m_post_del_Dir_Roz_Sob"))

            keyboard.row(types.InlineKeyboardButton(text="Директор по оптовому каналу",

                                                    callback_data="callback_m_post_del_Dir_Roz_Opt"))

            keyboard.row(types.InlineKeyboardButton(text="Специалист по закупкам",

                                                    callback_data="callback_m_post_del_Dir_Roz_Zak"))

            keyboard.row(types.InlineKeyboardButton(text="Далее",

                                                    callback_data="callback_m_post_dalee"))

            bot.send_message(
                text="Выбрано: Директор, Директор по розничному каналу \nДолжность клиента. Если несколько, то дополните позже.",

                chat_id=call.message.chat.id, reply_markup=keyboard)


        elif "Dir" in call.data and "Sob" not in call.data and "Opt" not in call.data and "Roz" not in call.data and "Zak" in call.data:

            # results[10] = "Директор"

            update_message(id_=id_search(user_id=call.message.chat.id), field='post',

                           mean="Директор, Специалист по закупкам")

            keyboard = types.InlineKeyboardMarkup()

            keyboard.row(types.InlineKeyboardButton(text="Собственник",

                                                    callback_data="callback_m_post_del_Dir_Zak_Sob"))

            keyboard.row(types.InlineKeyboardButton(text="Директор по оптовому каналу",

                                                    callback_data="callback_m_post_del_Dir_Zak_Opt"))

            keyboard.row(types.InlineKeyboardButton(text="Директор по розничному каналу",

                                                    callback_data="callback_m_post_del_Dir_Zak_Roz"))

            keyboard.row(types.InlineKeyboardButton(text="Далее",

                                                    callback_data="callback_m_post_dalee"))

            bot.send_message(

                text="Выбрано: Директор, Специалист по закупкам \nДолжность клиента. Если несколько, то дополните позже.",

                chat_id=call.message.chat.id, reply_markup=keyboard)

        elif "Dir" in call.data and "Sob" in call.data and "Opt" in call.data and "Roz" not in call.data and "Zak" not in call.data:

            # results[10] = "Директор"

            print('qwe')

            update_message(id_=id_search(user_id=call.message.chat.id), field='post',

                           mean="Директор, Собственник, Директор по оптовому каналу")

            keyboard = types.InlineKeyboardMarkup()

            keyboard.row(types.InlineKeyboardButton(text="Директор по розничному каналу",

                                                    callback_data="callback_m_post_del_Dir_Sob_Opt_Roz"))

            keyboard.row(types.InlineKeyboardButton(text="Специалист по закупкам",

                                                    callback_data="callback_m_post_del_Dir_Sob_Opt_Zak"))

            keyboard.row(types.InlineKeyboardButton(text="Далее",

                                                    callback_data="callback_m_post_dalee"))

            bot.send_message(

                text="Выбрано: Директор, Собственник, Директор по оптовому каналу \nДолжность клиента. Если несколько, то дополните позже.",

                chat_id=call.message.chat.id, reply_markup=keyboard)


        elif "Dir" in call.data and "Sob" in call.data and "Opt" not in call.data and "Roz" in call.data and not "Zak" in call.data:

            # results[10] = "Директор"

            update_message(id_=id_search(user_id=call.message.chat.id), field='post',

                           mean="Директор, Собственник, Директор по розничному каналу")

            keyboard = types.InlineKeyboardMarkup()

            keyboard.row(types.InlineKeyboardButton(text="Директор по оптовому каналу",

                                                    callback_data="callback_m_post_del_Dir_Sob_Opt"))

            keyboard.row(types.InlineKeyboardButton(text="Специалист по закупкам",

                                                    callback_data="callback_m_post_del_Dir_Sob_Zak"))

            keyboard.row(types.InlineKeyboardButton(text="Далее",

                                                    callback_data="callback_m_post_dalee"))

            bot.send_message(

                text="Выбрано: Директор, Собственник, Директор по розничному каналу \nДолжность клиента. Если несколько, то дополните позже.",

                chat_id=call.message.chat.id, reply_markup=keyboard)


        elif "Dir" in call.data and "Sob" in call.data and "Opt" not in call.data and "Roz" not in call.data and "Zak" in call.data:

            # results[10] = "Директор"

            update_message(id_=id_search(user_id=call.message.chat.id), field='post',

                           mean="Директор, Собственник, Специалист по закупкам")

            keyboard = types.InlineKeyboardMarkup()

            keyboard.row(types.InlineKeyboardButton(text="Директор по оптовому каналу",

                                                    callback_data="callback_m_post_del_Dir_Sob_Opt"))

            keyboard.row(types.InlineKeyboardButton(text="Директор по розничному каналу",

                                                    callback_data="callback_m_post_del_Dir_Sob_Roz"))

            keyboard.row(types.InlineKeyboardButton(text="Далее",

                                                    callback_data="callback_m_post_dalee"))

            bot.send_message(

                text="Выбрано: Директор, Собственник, Специалист по закупкам \nДолжность клиента. Если несколько, то дополните позже.",

                chat_id=call.message.chat.id, reply_markup=keyboard)


        elif "Dir" in call.data and "Sob" in call.data and "Opt" in call.data and "Roz" in call.data and "Zak" not in call.data:

            # results[10] = "Директор"

            update_message(id_=id_search(user_id=call.message.chat.id), field='post',

                           mean="Директор, Собственник, Директор по оптовому каналу, Директор по розничному каналу")

            keyboard = types.InlineKeyboardMarkup()

            keyboard.row(types.InlineKeyboardButton(text="Специалист по закупкам",

                                                    callback_data="callback_m_post_del_Dir_Sob_Opt_Roz_Zak"))

            keyboard.row(types.InlineKeyboardButton(text="Далее",

                                                    callback_data="callback_m_post_dalee"))

            bot.send_message(

                text="Выбрано: Директор, Собственник, Директор по оптовому каналу, Директор по розничному каналу \nДолжность клиента. Если несколько, то дополните позже.",

                chat_id=call.message.chat.id, reply_markup=keyboard)


        elif "Dir" in call.data and "Sob" in call.data and "Opt" in call.data and "Roz" not in call.data and "Zak" in call.data:

            # results[10] = "Директор"

            update_message(id_=id_search(user_id=call.message.chat.id), field='post',

                           mean="Директор, Собственник, Директор по оптовому каналу, Специалист по закупкам")

            keyboard = types.InlineKeyboardMarkup()

            keyboard.row(types.InlineKeyboardButton(text="Директор по розничному каналу",

                                                    callback_data="callback_m_post_del_Dir_Sob_Opt_Roz"))

            keyboard.row(types.InlineKeyboardButton(text="Далее",

                                                    callback_data="callback_m_post_dalee"))

            bot.send_message(

                text="Выбрано: Директор, Собственник, Директор по оптовому каналу, Специалист по закупкам \nДолжность клиента. Если несколько, то дополните позже.",

                chat_id=call.message.chat.id, reply_markup=keyboard)


        elif "Dir" in call.data and "Sob" in call.data and "Opt" in call.data and "Roz" in call.data and "Zak" in call.data:

            # results[10] = "Директор"

            update_message(id_=id_search(user_id=call.message.chat.id), field='post',

                           mean="Директор, Собственник, Директор по оптовому каналу, Специалист по закупкам, Директор по розничному каналу")

            keyboard = types.InlineKeyboardMarkup()

            keyboard.row(types.InlineKeyboardButton(text="Далее",

                                                    callback_data="callback_m_post_dalee"))

            bot.send_message(

                text="Выбрано: Директор, Собственник, Директор по оптовому каналу, Специалист по закупкам, Директор по розничному каналу\nДолжность клиента. Если несколько, то дополните позже.",

                chat_id=call.message.chat.id, reply_markup=keyboard)




        elif "zak" in call.data:

            # results[10] = "Директор"

            update_message(id_=id_search(user_id=call.message.chat.id), field='post',

                           mean="Специалист по закупкам")

            keyboard = types.InlineKeyboardMarkup()

            keyboard.row(types.InlineKeyboardButton(text="Директор",

                                                    callback_data="callback_m_post_del_Zak_Dir"))

            keyboard.row(types.InlineKeyboardButton(text="Собственник",

                                                    callback_data="callback_m_post_del_Zak_Sob"))

            keyboard.row(types.InlineKeyboardButton(text="Директор по оптовому каналу",

                                                    callback_data="callback_m_post_del_Zak_Opt"))

            keyboard.row(types.InlineKeyboardButton(text="Директор по розничному каналу",

                                                    callback_data="callback_m_post_del_Zak_Roz"))

            keyboard.row(types.InlineKeyboardButton(text="Далее",

                                                    callback_data="callback_m_post_dalee"))

            bot.send_message(
                text="Выбрано: Специалист по закупкам \nДолжность клиента. Если несколько, то дополните позже.",

                chat_id=call.message.chat.id, reply_markup=keyboard)


        elif "Dir" not in call.data and "Sob" in call.data and "Opt" not in call.data and "Roz" not in call.data and "Zak" in call.data:

            # results[10] = "Директор"

            update_message(id_=id_search(user_id=call.message.chat.id), field='post',

                           mean="Собственник, Специалист по закупкам")

            keyboard = types.InlineKeyboardMarkup()

            keyboard.row(types.InlineKeyboardButton(text="Директор",

                                                    callback_data="callback_m_post_del_Zak_Sob_Dir"))

            keyboard.row(types.InlineKeyboardButton(text="Директор по оптовому каналу",

                                                    callback_data="callback_m_post_del_Zak_Sob_Opt"))

            keyboard.row(types.InlineKeyboardButton(text="Директор по розничному каналу",

                                                    callback_data="callback_m_post_del_Zak_Sob_Roz"))

            keyboard.row(types.InlineKeyboardButton(text="Далее",

                                                    callback_data="callback_m_post_dalee"))

            bot.send_message(
                text="Выбрано: Собственник, Специалист по закупкам \nДолжность клиента. Если несколько, то дополните позже.",

                chat_id=call.message.chat.id, reply_markup=keyboard)


        elif "Dir" not in call.data and "Sob" not in call.data and "Opt" in call.data and "Roz" not in call.data and "Zak" in call.data:

            # results[10] = "Директор"

            update_message(id_=id_search(user_id=call.message.chat.id), field='post',

                           mean="Директор по оптовому каналу, Специалист по закупкам")

            keyboard = types.InlineKeyboardMarkup()

            keyboard.row(types.InlineKeyboardButton(text="Директор",

                                                    callback_data="callback_m_post_del_Zak_Opt_Dir"))

            keyboard.row(types.InlineKeyboardButton(text="Собственник",

                                                    callback_data="callback_m_post_del_Zak_Opt_Sob"))

            keyboard.row(types.InlineKeyboardButton(text="Директор по розничному каналу",

                                                    callback_data="callback_m_post_del_Zak_Opt_Roz"))

            keyboard.row(types.InlineKeyboardButton(text="Далее",

                                                    callback_data="callback_m_post_dalee"))

            bot.send_message(
                text="Выбрано: Директор по оптовому каналу, Специалист по закупкам \nДолжность клиента. Если несколько, то дополните позже.",

                chat_id=call.message.chat.id, reply_markup=keyboard)




        elif "Dir" not in call.data and "Sob" not in call.data and "Opt" not in call.data and "Roz" in call.data and "Zak" in call.data:

            # results[10] = "Директор"

            update_message(id_=id_search(user_id=call.message.chat.id), field='post',

                           mean="Директор по розничному каналу, Специалист по закупкам")

            keyboard = types.InlineKeyboardMarkup()

            keyboard.row(types.InlineKeyboardButton(text="Директор",

                                                    callback_data="callback_m_post_del_Zak_Roz_Dir"))

            keyboard.row(types.InlineKeyboardButton(text="Собственник",

                                                    callback_data="callback_m_post_del_Zak_Roz_Sob"))

            keyboard.row(types.InlineKeyboardButton(text="Директор по оптовому каналу",

                                                    callback_data="callback_m_post_del_Zak_Roz_Opt"))

            keyboard.row(types.InlineKeyboardButton(text="Далее",

                                                    callback_data="callback_m_post_dalee"))

            bot.send_message(
                text="Выбрано: Директор по розничному каналу, Специалист по закупкам \nДолжность клиента. Если несколько, то дополните позже.",

                chat_id=call.message.chat.id, reply_markup=keyboard)



        elif "Dir" not in call.data and "Sob" in call.data and "Opt" in call.data and "Roz" not in call.data and "Zak" in call.data:

            update_message(id_=id_search(user_id=call.message.chat.id), field='post',

                           mean="Собственник, Специалист по закупкам, Директор по оптовому каналу")

            keyboard = types.InlineKeyboardMarkup()

            keyboard.row(types.InlineKeyboardButton(text="Директор",

                                                    callback_data="callback_m_post_del_Zak_Sob_Opt_Dir"))

            keyboard.row(types.InlineKeyboardButton(text="Директор по розничному каналу",

                                                    callback_data="callback_m_post_del_Zak_Sob_Opt_Roz"))

            keyboard.row(types.InlineKeyboardButton(text="Далее",

                                                    callback_data="callback_m_post_dalee"))

            bot.send_message(

                text="Выбрано: Собственник, Директор по оптовому каналу, Специалист по закупкам \nДолжность клиента. Если несколько, то дополните позже.",

                chat_id=call.message.chat.id, reply_markup=keyboard)


        elif "Dir" not in call.data and "Sob" in call.data and "Opt" not in call.data and "Roz" in call.data and "Zak" in call.data:

            update_message(id_=id_search(user_id=call.message.chat.id), field='post',

                           mean="Собственник, Специалист по закупкам, Директор по розничному каналу")

            keyboard = types.InlineKeyboardMarkup()

            keyboard.row(types.InlineKeyboardButton(text="Директор",

                                                    callback_data="callback_m_post_del_Zak_Sob_Roz_Dir"))

            keyboard.row(types.InlineKeyboardButton(text="Директор по розничному каналу",

                                                    callback_data="callback_m_post_del_Zak_Sob_Roz_Opt"))

            keyboard.row(types.InlineKeyboardButton(text="Далее",

                                                    callback_data="callback_m_post_dalee"))

            bot.send_message(

                text="Выбрано: Собственник, Директор по розничному каналу, Специалист по закупкам \nДолжность клиента. Если несколько, то дополните позже.",

                chat_id=call.message.chat.id, reply_markup=keyboard)


        elif "Dir" not in call.data and "Sob" in call.data and "Opt" in call.data and "Roz" in call.data and "Zak" in call.data:

            update_message(id_=id_search(user_id=call.message.chat.id), field='post',

                           mean="Собственник, Директор по оптовому каналу, Директор по розничному каналу, Специалист по закупкам")

            keyboard = types.InlineKeyboardMarkup()

            keyboard.row(types.InlineKeyboardButton(text="Директор",

                                                    callback_data="callback_m_post_del_Zak_Sob_Roz_Dir_Opt"))

            keyboard.row(types.InlineKeyboardButton(text="Далее",

                                                    callback_data="callback_m_post_dalee"))

            bot.send_message(

                text="Выбрано: Собственник, Директор по оптовому каналу, Директор по розничному каналу, Специалист по закупкам \nДолжность клиента. Если несколько, то дополните позже.",

                chat_id=call.message.chat.id, reply_markup=keyboard)


        elif "sob" in call.data:

            update_message(id_=id_search(user_id=call.message.chat.id), field='post',

                           mean="Собственник")

            keyboard = types.InlineKeyboardMarkup()

            keyboard.row(types.InlineKeyboardButton(text="Директор",

                                                    callback_data="callback_m_post_del_Sob_Dir"))

            keyboard.row(types.InlineKeyboardButton(text="Директор по оптовому каналу",

                                                    callback_data="callback_m_post_del_Sob_Opt"))

            keyboard.row(types.InlineKeyboardButton(text="Директор по розничному каналу",

                                                    callback_data="callback_m_post_del_Sob_Roz"))

            keyboard.row(types.InlineKeyboardButton(text="Специалист по закупкам",

                                                    callback_data="callback_m_post_del_Sob_Zak"))

            keyboard.row(types.InlineKeyboardButton(text="Далее",

                                                    callback_data="callback_m_post_dalee"))

            bot.send_message(

                text="Выбрано: Собственник \nДолжность клиента. Если несколько, то дополните позже.",

                chat_id=call.message.chat.id, reply_markup=keyboard)


        elif "Dir" not in call.data and "Sob" in call.data and "Opt" in call.data and "Roz" not in call.data and "Zak" not in call.data:

            update_message(id_=id_search(user_id=call.message.chat.id), field='post',

                           mean="Собственник, Директор по оптовому каналу")

            keyboard = types.InlineKeyboardMarkup()

            keyboard.row(types.InlineKeyboardButton(text="Директор",

                                                    callback_data="callback_m_post_del_Sob_Opt_Dir"))

            keyboard.row(types.InlineKeyboardButton(text="Директор по розничному каналу",

                                                    callback_data="callback_m_post_del_Sob_Opt_Roz"))

            keyboard.row(types.InlineKeyboardButton(text="Специалист по закупкам",

                                                    callback_data="callback_m_post_del_Sob_Opt_Zak"))

            keyboard.row(types.InlineKeyboardButton(text="Далее",

                                                    callback_data="callback_m_post_dalee"))

            bot.send_message(

                text="Выбрано: Собственник, Директор по оптовому каналу \nДолжность клиента. Если несколько, то дополните позже.",

                chat_id=call.message.chat.id, reply_markup=keyboard)






        elif "Dir" not in call.data and "Sob" in call.data and "Opt" not in call.data and "Roz" in call.data and "Zak" not in call.data:

            update_message(id_=id_search(user_id=call.message.chat.id), field='post',

                           mean="Собственник, Директор по розничному каналу")

            keyboard = types.InlineKeyboardMarkup()

            keyboard.row(types.InlineKeyboardButton(text="Директор",

                                                    callback_data="callback_m_post_del_Sob_Roz_Dir"))

            keyboard.row(types.InlineKeyboardButton(text="Директор по оптовому каналу",

                                                    callback_data="callback_m_post_del_Sob_Roz_Opt"))

            keyboard.row(types.InlineKeyboardButton(text="Специалист по закупкам",

                                                    callback_data="callback_m_post_del_Sob_Roz_Zak"))

            keyboard.row(types.InlineKeyboardButton(text="Далее",

                                                    callback_data="callback_m_post_dalee"))

            bot.send_message(

                text="Выбрано: Собственник, Директор по розничному каналу \nДолжность клиента. Если несколько, то дополните позже.",

                chat_id=call.message.chat.id, reply_markup=keyboard)


        elif "Dir" not in call.data and "Sob" in call.data and "Opt" in call.data and "Roz" in call.data and "Zak" not in call.data:

            update_message(id_=id_search(user_id=call.message.chat.id), field='post',

                           mean="Собственник, Директор по оптовому каналу, Директор по розничному каналу")

            keyboard = types.InlineKeyboardMarkup()

            keyboard.row(types.InlineKeyboardButton(text="Директор",

                                                    callback_data="callback_m_post_del_Sob_Opt_Roz_Dir"))

            keyboard.row(types.InlineKeyboardButton(text="Специалист по закупкам",

                                                    callback_data="callback_m_post_del_Sob_Opt_Roz_Zak"))

            keyboard.row(types.InlineKeyboardButton(text="Далее",

                                                    callback_data="callback_m_post_dalee"))

            bot.send_message(

                text="Выбрано: Собственник, Директор по оптовому каналу, Директор по розничному каналу \nДолжность клиента. Если несколько, то дополните позже.",

                chat_id=call.message.chat.id, reply_markup=keyboard)





        elif "opt" in call.data:

            update_message(id_=id_search(user_id=call.message.chat.id), field='post',

                           mean="Директор по оптовому каналу")

            keyboard = types.InlineKeyboardMarkup()

            keyboard.row(types.InlineKeyboardButton(text="Директор",

                                                    callback_data="callback_m_post_del_Opt_Dir"))

            keyboard.row(types.InlineKeyboardButton(text="Собственник",

                                                    callback_data="callback_m_post_del_Opt_Sob"))

            keyboard.row(types.InlineKeyboardButton(text="Директор по розничному каналу",

                                                    callback_data="callback_m_post_del_Opt_Roz"))

            keyboard.row(types.InlineKeyboardButton(text="Специалист по закупкам",

                                                    callback_data="callback_m_post_del_Opt_Zak"))

            keyboard.row(types.InlineKeyboardButton(text="Далее",

                                                    callback_data="callback_m_post_dalee"))

            bot.send_message(

                text="Выбрано: Директор по оптовому каналу \nДолжность клиента. Если несколько, то дополните позже.",

                chat_id=call.message.chat.id, reply_markup=keyboard)


        elif "Dir" not in call.data and "Sob" not in call.data and "Opt" in call.data and "Roz" in call.data and "Zak" not in call.data:

            update_message(id_=id_search(user_id=call.message.chat.id), field='post',

                           mean="Директор по оптовому каналу, Директор по розничному каналу")

            keyboard = types.InlineKeyboardMarkup()

            keyboard.row(types.InlineKeyboardButton(text="Директор",

                                                    callback_data="callback_m_post_del_Opt_Roz_Dir"))

            keyboard.row(types.InlineKeyboardButton(text="Собственник",

                                                    callback_data="callback_m_post_del_Opt_Roz_Sob"))

            keyboard.row(types.InlineKeyboardButton(text="Специалист по закупкам",

                                                    callback_data="callback_m_post_del_Opt_Roz_Zak"))

            keyboard.row(types.InlineKeyboardButton(text="Далее",

                                                    callback_data="callback_m_post_dalee"))

            bot.send_message(

                text="Выбрано: Директор по оптовому каналу, Директор по розничному каналу \nДолжность клиента. Если несколько, то дополните позже.",

                chat_id=call.message.chat.id, reply_markup=keyboard)

        elif "roz" in call.data:

            update_message(id_=id_search(user_id=call.message.chat.id), field='post',

                           mean="Директор по розничному каналу")

            keyboard = types.InlineKeyboardMarkup()

            keyboard.row(types.InlineKeyboardButton(text="Директор",

                                                    callback_data="callback_m_post_del_Roz_Dir"))

            keyboard.row(types.InlineKeyboardButton(text="Собственник",

                                                    callback_data="callback_m_post_del_Roz_Sob"))

            keyboard.row(types.InlineKeyboardButton(text="Директор по оптовому каналу",

                                                    callback_data="callback_m_post_del_Roz_Opt"))

            keyboard.row(types.InlineKeyboardButton(text="Специалист по закупкам",

                                                    callback_data="callback_m_post_del_Roz_Zak"))

            keyboard.row(types.InlineKeyboardButton(text="Далее",

                                                    callback_data="callback_m_post_dalee"))

            bot.send_message(

                text="Выбрано: Директор по розничному каналу \nДолжность клиента. Если несколько, то дополните позже.",

                chat_id=call.message.chat.id, reply_markup=keyboard)


        # elif "roz" in call.data:

        #     # results[10] = "Директор по розничному каналу"

        #     update_message(id_=id_search(user_id=call.message.chat.id), field='post',

        #                    mean="Директор по розничному каналу")

        elif "dalee" in call.data:

            bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Укажите название торговой точки"),

                                           c_direction)

    elif call.data == "callback_m_dir_d":
        bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Уточните данные"), m_field)

    elif "callback_m_dir" in call.data:
        if "opt" in call.data:
            # results[11] = "Оптовая торговля"
            update_message(id_=id_search(user_id=call.message.chat.id), field='direction',
                           mean="Оптовая торговля")
        elif "rok" in call.data:
            # results[11] = "Корпоративные продажи"
            update_message(id_=id_search(user_id=call.message.chat.id), field='direction',
                           mean="Корпоративные продажи")
        elif "int" in call.data:
            # results[11] = "Интернет"
            update_message(id_=id_search(user_id=call.message.chat.id), field='direction',
                           mean="Интернет")
        elif "roz" in call.data:
            # results[11] = "Розница"
            update_message(id_=id_search(user_id=call.message.chat.id), field='direction',
                           mean="Розница")
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        keyboard.add(types.InlineKeyboardButton(text="Канцелярия",
                                                callback_data="callback_m_field_kan"),
                     types.InlineKeyboardButton(text="Детские товары",
                                                callback_data="callback_m_field_det"),
                     types.InlineKeyboardButton(text="Книги",
                                                callback_data="callback_m_field_kni"),
                     types.InlineKeyboardButton(text="Сумки",
                                                callback_data="callback_m_field_sum"),
                     types.InlineKeyboardButton(text="Сувениры",
                                                callback_data="callback_m_field_suv"),
                     types.InlineKeyboardButton(text="Другое",
                                                callback_data="callback_m_field_d")
                     )
        bot.send_message(call.message.chat.id, "Укажите сферу:", reply_markup=keyboard)

    elif call.data == "callback_m_field_d":
        bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Уточните данные"), m_offline)


    elif "callback_m_field" in call.data:
        if "kan" in call.data:
            # results[12] = "Канцелярия"
            update_message(id_=id_search(user_id=call.message.chat.id), field='field',
                           mean="Канцелярия")
        elif "det" in call.data:
            # results[12] = "Детские товары"
            update_message(id_=id_search(user_id=call.message.chat.id), field='field',
                           mean="Детские товары")
        elif "kni" in call.data:
            # results[12] = "Книги"
            update_message(id_=id_search(user_id=call.message.chat.id), field='field',
                           mean="Книги")
        elif "sum" in call.data:
            # results[12] = "Сумки"
            update_message(id_=id_search(user_id=call.message.chat.id), field='field',
                           mean="Сумки")
        elif "suv" in call.data:
            # results[12] = "Сувениры"
            update_message(id_=id_search(user_id=call.message.chat.id), field='field',
                           mean="Сувениры")
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        keyboard.add(types.InlineKeyboardButton(text="✅Есть",
                                                callback_data="callback_m_offline_yes"),
                     types.InlineKeyboardButton(text="❌Нет",
                                                callback_data="callback_m_offline_no"),
                     )
        bot.send_message(call.message.chat.id, "Наличие оффлайн точек:", reply_markup=keyboard)


    elif call.data == "callback_m_offline_yes":
        # results[13] = "Да"
        update_message(id_=id_search(user_id=call.message.chat.id), field='offline',
                       mean="Да")
        bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Укажите количество"), m_assort)


    elif call.data == "callback_m_offline_no":
        # results[13] = ""
        update_message(id_=id_search(user_id=call.message.chat.id), field='offline',
                       mean="Нет")
        keyboard = types.InlineKeyboardMarkup()
        keyboard.row(types.InlineKeyboardButton(text="Интересна вся продукция",
                                                callback_data="callback_m_assort_prod"))
        keyboard.row(types.InlineKeyboardButton(text="Интересует некоторая продукция",
                                                callback_data="callback_m_assort_some"))
        keyboard.row(types.InlineKeyboardButton(text="Офис",
                                                callback_data="callback_m_assort_ofi"),
                     types.InlineKeyboardButton(text="Пластик",
                                                callback_data="callback_m_assort_spa"),
                     )
        keyboard.row(types.InlineKeyboardButton(text="Сумки-рюкзаки",
                                                callback_data="callback_m_assort_sum"),
                     types.InlineKeyboardButton(text="Творчество",
                                                callback_data="callback_m_assort_two"))
        keyboard.row(types.InlineKeyboardButton(text="Бумажно-беловая",
                                   callback_data="callback_m_assort_bum"))
        bot.send_message(call.message.chat.id, "Укажите интересующий ассортимент.", reply_markup=keyboard)


    elif "callback_m_assort" in call.data:
        if "some" in call.data:
            print("qwe")
            bot.register_next_step_handler(bot.send_message(call.message.chat.id, ("Введите через пробел номер интересующего Вас ассортимента:\n"
                                                    "1. Офис\n"
                                                    "2. Пластик\n"
                                                    "3. Бумажно-беловая прод.\n"
                                                    "4. Сумки-рюкзаки\n"
                                                    "5. Творчество\n")), m_some_assort)
        else:

            if "prod" in call.data:
                # results[15] = "Интересна вся продукция"
                update_message(id_=id_search(user_id=call.message.chat.id), field='interest',
                               mean="Интересна вся продукция")
            elif "ofi" in call.data:
                # results[15] = "Офис"
                update_message(id_=id_search(user_id=call.message.chat.id), field='interest',
                               mean="Офис")
            elif "spa" in call.data:
                # results[15] = "Пластик"
                update_message(id_=id_search(user_id=call.message.chat.id), field='interest',
                               mean="Пластик")
            elif "bum" in call.data:
                # results[15] = "Бумажно-беловая"
                update_message(id_=id_search(user_id=call.message.chat.id), field='interest',
                               mean="Бумажно-беловая")
            elif "sum" in call.data:
                # results[15] = "Сумки-рюкзаки"
                update_message(id_=id_search(user_id=call.message.chat.id), field='interest',
                               mean="Сумки-рюкзаки")
            elif "two" in call.data:
                # results[15] = "Творчество"
                update_message(id_=id_search(user_id=call.message.chat.id), field='interest',
                               mean="Творчество")
            keyboard = types.InlineKeyboardMarkup(row_width=3)
            keyboard.add(types.InlineKeyboardButton(text="✅Да",
                                                    callback_data="callback_m_comment_yes"),
                         types.InlineKeyboardButton(text="❌Нет",
                                                    callback_data="callback_m_comment_no"),
                         )
            bot.send_message(call.message.chat.id, "У вас есть комментарии по заполненной анкете?", reply_markup=keyboard)


    elif call.data == "callback_m_comment_no":
        # results[16] = "Нет"
        update_message(id_=id_search(user_id=call.message.chat.id), field='com',
                       mean="Нет")
        # add_message(user_id=results[18], data=results)
        bot.register_next_step_handler(
            bot.send_message(call.message.chat.id, ("Спасибо за заполнение анкеты, все данные сохранены! 🎉\n"
                                                    f"*Универсальный номер анкеты:{random.randint(10000,90000)}-{iid[0]},*"
                                                    " *по нему клиент может получить подарок.*"),
                             parse_mode='Markdown'), m_pass)
        iid[0] = iid[0] + 1
    elif call.data == "callback_m_comment_yes":
        # results[16] = "Да"
        update_message(id_=id_search(user_id=call.message.chat.id), field='com',
                       mean="Да")
        # print(results)
        bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Укажите Ваш комментарий"), m_finish)


    ######################################################
    elif "callback_role_c" == call.data:
        # results[0] = call.data.strip("callback_date")
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(types.InlineKeyboardButton(text="Верно",
                                                callback_data="callback_client"),
                     types.InlineKeyboardButton(text="Назад",
                                                callback_data="callback_date"))
        bot.send_message(call.message.chat.id, "Вы выбрали клиент", reply_markup=keyboard)

    elif call.data == "callback_client":
        # results[1] = call.data.strip("callback_")
        update_message(id_=id_search(user_id=call.message.chat.id), field='role',
                       mean=call.data[-6:])
        bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Ваше ФИО"), c_coop)


    elif call.data == "callback_c_coop_d":
        bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Уточните данные"), c_city)


    elif "callback_c_coop" in call.data:
        if "yes" in call.data:
            # results[5] = "Да"
            update_message(id_=id_search(user_id=call.message.chat.id), field='coop',
                           mean="Да")
        elif "no" in call.data:
            # results[5] = "Нет"
            update_message(id_=id_search(user_id=call.message.chat.id), field='coop',
                           mean="Нет")
        elif "worked" in call.data:
            # results[5] = "Работали ранее, но прекратили"
            update_message(id_=id_search(user_id=call.message.chat.id), field='coop',
                           mean="Работали ранее, но прекратили")

        bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Город Вашего офиса"), c_region)


    elif call.data == "callback_c_post_d":
        bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Уточните данные"), c_point)


    elif "callback_c_post" in call.data:
        print(call.data)
        if "dir" in call.data:
            # results[10] = "Директор"
            update_message(id_=id_search(user_id=call.message.chat.id), field='post',
                           mean="Директор")

            keyboard = types.InlineKeyboardMarkup()
            keyboard.row(types.InlineKeyboardButton(text="Собственник",
                                                    callback_data="callback_c_post_del_Dir_Sob"))
            keyboard.row(types.InlineKeyboardButton(text="Директор по оптовому каналу",
                                                    callback_data="callback_c_post_del_Dir_Opt"))
            keyboard.row(types.InlineKeyboardButton(text="Директор по розничному каналу",
                                                    callback_data="callback_c_post_del_Dir_Roz"))
            keyboard.row(types.InlineKeyboardButton(text="Специалист по закупкам",
                                                    callback_data="callback_c_post_del_Dir_Zak"))
            keyboard.row(types.InlineKeyboardButton(text="Далее",
                                                    callback_data="callback_c_post_dalee"))
            bot.send_message(text="Выбрано: Директор \nДолжность клиента. Если несколько, то дополните позже.",
                                  chat_id=call.message.chat.id, reply_markup=keyboard)

        elif "Dir" in call.data and "Sob" in call.data and "Opt" not in call.data and "Roz" not in call.data and "Zak" not in call.data:
            # results[10] = "Директор"
            update_message(id_=id_search(user_id=call.message.chat.id), field='post',
                           mean="Директор, Собственник")

            keyboard = types.InlineKeyboardMarkup()
            keyboard.row(types.InlineKeyboardButton(text="Директор по оптовому каналу",
                                                    callback_data="callback_c_post_del_Dir_Sob_Opt"))
            keyboard.row(types.InlineKeyboardButton(text="Директор по розничному каналу",
                                                    callback_data="callback_c_post_del_Dir_Sob_Roz"))
            keyboard.row(types.InlineKeyboardButton(text="Специалист по закупкам",
                                                    callback_data="callback_c_post_del_Dir_Sob_Zak"))
            keyboard.row(types.InlineKeyboardButton(text="Далее",
                                                    callback_data="callback_c_post_dalee"))
            bot.send_message(text="Выбрано: Директор, Собственник \nДолжность клиента. Если несколько, то дополните позже.",
                                  chat_id=call.message.chat.id, reply_markup=keyboard)

        elif "Dir" in call.data and "Sob" not in call.data and "Opt" in call.data and "Roz" not in call.data and "Zak" not in call.data:
            # results[10] = "Директор"
            update_message(id_=id_search(user_id=call.message.chat.id), field='post',
                           mean="Директор, Директор по оптовому каналу")

            keyboard = types.InlineKeyboardMarkup()
            keyboard.row(types.InlineKeyboardButton(text="Собственник",
                                                    callback_data="callback_c_post_del_Dir_Opt_Sob"))
            keyboard.row(types.InlineKeyboardButton(text="Директор по розничному каналу",
                                                    callback_data="callback_c_post_del_Dir_Opt_Roz"))
            keyboard.row(types.InlineKeyboardButton(text="Специалист по закупкам",
                                                    callback_data="callback_c_post_del_Dir_Opt_Zak"))
            keyboard.row(types.InlineKeyboardButton(text="Далее",
                                                    callback_data="callback_c_post_dalee"))
            bot.send_message(text="Выбрано: Директор, Директор по оптовому каналу \nДолжность клиента. Если несколько, то дополните позже.",
                                  chat_id=call.message.chat.id, reply_markup=keyboard)

        elif "Dir" in call.data and "Sob" not in call.data and "Opt" not in call.data and "Roz" in call.data and "Zak" not in call.data:
            # results[10] = "Директор"
            update_message(id_=id_search(user_id=call.message.chat.id), field='post',
                           mean="Директор, Директор по розничному каналу")

            keyboard = types.InlineKeyboardMarkup()
            keyboard.row(types.InlineKeyboardButton(text="Собственник",
                                                    callback_data="callback_c_post_del_Dir_Roz_Sob"))
            keyboard.row(types.InlineKeyboardButton(text="Директор по оптовому каналу",
                                                    callback_data="callback_c_post_del_Dir_Roz_Opt"))
            keyboard.row(types.InlineKeyboardButton(text="Специалист по закупкам",
                                                    callback_data="callback_c_post_del_Dir_Roz_Zak"))
            keyboard.row(types.InlineKeyboardButton(text="Далее",
                                                    callback_data="callback_c_post_dalee"))
            bot.send_message(text="Выбрано: Директор, Директор по розничному каналу \nДолжность клиента. Если несколько, то дополните позже.",
                                  chat_id=call.message.chat.id, reply_markup=keyboard)

        elif "Dir" in call.data and "Sob" not in call.data and "Opt" not in call.data and "Roz" not in call.data and "Zak" in call.data:
            # results[10] = "Директор"
            update_message(id_=id_search(user_id=call.message.chat.id), field='post',
                           mean="Директор, Специалист по закупкам")

            keyboard = types.InlineKeyboardMarkup()
            keyboard.row(types.InlineKeyboardButton(text="Собственник",
                                                    callback_data="callback_c_post_del_Dir_Zak_Sob"))
            keyboard.row(types.InlineKeyboardButton(text="Директор по оптовому каналу",
                                                    callback_data="callback_c_post_del_Dir_Zak_Opt"))
            keyboard.row(types.InlineKeyboardButton(text="Директор по розничному каналу",
                                                    callback_data="callback_c_post_del_Dir_Zak_Roz"))
            keyboard.row(types.InlineKeyboardButton(text="Далее",
                                                    callback_data="callback_c_post_dalee"))
            bot.send_message(
                text="Выбрано: Директор, Специалист по закупкам \nДолжность клиента. Если несколько, то дополните позже.",
                chat_id=call.message.chat.id, reply_markup=keyboard)
        elif "Dir" in call.data and "Sob" in call.data and "Opt" in call.data and "Roz" not in call.data and "Zak" not in call.data:
            # results[10] = "Директор"
            print('qwe')
            update_message(id_=id_search(user_id=call.message.chat.id), field='post',
                           mean="Директор, Собственник, Директор по оптовому каналу")
            keyboard = types.InlineKeyboardMarkup()
            keyboard.row(types.InlineKeyboardButton(text="Директор по розничному каналу",
                                                    callback_data="callback_c_post_del_Dir_Sob_Opt_Roz"))
            keyboard.row(types.InlineKeyboardButton(text="Специалист по закупкам",
                                                    callback_data="callback_c_post_del_Dir_Sob_Opt_Zak"))
            keyboard.row(types.InlineKeyboardButton(text="Далее",
                                                    callback_data="callback_c_post_dalee"))
            bot.send_message(
                text="Выбрано: Директор, Собственник, Директор по оптовому каналу \nДолжность клиента. Если несколько, то дополните позже.",
                chat_id=call.message.chat.id, reply_markup=keyboard)

        elif "Dir" in call.data and "Sob" in call.data and "Opt" not in call.data and "Roz" in call.data and not "Zak" in call.data:
            # results[10] = "Директор"
            update_message(id_=id_search(user_id=call.message.chat.id), field='post',
                           mean="Директор, Собственник, Директор по розничному каналу")

            keyboard = types.InlineKeyboardMarkup()
            keyboard.row(types.InlineKeyboardButton(text="Директор по оптовому каналу",
                                                    callback_data="callback_c_post_del_Dir_Sob_Opt"))
            keyboard.row(types.InlineKeyboardButton(text="Специалист по закупкам",
                                                    callback_data="callback_c_post_del_Dir_Sob_Zak"))
            keyboard.row(types.InlineKeyboardButton(text="Далее",
                                                    callback_data="callback_c_post_dalee"))
            bot.send_message(
                text="Выбрано: Директор, Собственник, Директор по розничному каналу \nДолжность клиента. Если несколько, то дополните позже.",
                chat_id=call.message.chat.id, reply_markup=keyboard)

        elif "Dir" in call.data and "Sob" in call.data and "Opt" not in call.data and "Roz" not in call.data and "Zak" in call.data:
            # results[10] = "Директор"
            update_message(id_=id_search(user_id=call.message.chat.id), field='post',
                           mean="Директор, Собственник, Специалист по закупкам")

            keyboard = types.InlineKeyboardMarkup()
            keyboard.row(types.InlineKeyboardButton(text="Директор по оптовому каналу",
                                                    callback_data="callback_c_post_del_Dir_Sob_Opt"))
            keyboard.row(types.InlineKeyboardButton(text="Директор по розничному каналу",
                                                    callback_data="callback_c_post_del_Dir_Sob_Roz"))
            keyboard.row(types.InlineKeyboardButton(text="Далее",
                                                    callback_data="callback_c_post_dalee"))
            bot.send_message(
                text="Выбрано: Директор, Собственник, Специалист по закупкам \nДолжность клиента. Если несколько, то дополните позже.",
                chat_id=call.message.chat.id, reply_markup=keyboard)

        elif "Dir" in call.data and "Sob" in call.data and "Opt" in call.data and "Roz" in call.data and "Zak" not in call.data:
            # results[10] = "Директор"
            update_message(id_=id_search(user_id=call.message.chat.id), field='post',
                           mean="Директор, Собственник, Директор по оптовому каналу, Директор по розничному каналу")
            keyboard = types.InlineKeyboardMarkup()
            keyboard.row(types.InlineKeyboardButton(text="Специалист по закупкам",
                                                    callback_data="callback_c_post_del_Dir_Sob_Opt_Roz_Zak"))
            keyboard.row(types.InlineKeyboardButton(text="Далее",
                                                    callback_data="callback_c_post_dalee"))
            bot.send_message(
                text="Выбрано: Директор, Собственник, Директор по оптовому каналу, Директор по розничному каналу \nДолжность клиента. Если несколько, то дополните позже.",
                chat_id=call.message.chat.id,reply_markup=keyboard)

        elif "Dir" in call.data and "Sob" in call.data and "Opt" in call.data and "Roz" not in call.data and "Zak" in call.data:
            # results[10] = "Директор"
            update_message(id_=id_search(user_id=call.message.chat.id), field='post',
                           mean="Директор, Собственник, Директор по оптовому каналу, Специалист по закупкам")
            keyboard = types.InlineKeyboardMarkup()
            keyboard.row(types.InlineKeyboardButton(text="Директор по розничному каналу",
                                                    callback_data="callback_c_post_del_Dir_Sob_Opt_Roz"))
            keyboard.row(types.InlineKeyboardButton(text="Далее",
                                                    callback_data="callback_c_post_dalee"))
            bot.send_message(
                text="Выбрано: Директор, Собственник, Директор по оптовому каналу, Специалист по закупкам \nДолжность клиента. Если несколько, то дополните позже.",
                chat_id=call.message.chat.id, reply_markup=keyboard)

        elif "Dir" in call.data and "Sob" in call.data and "Opt" in call.data and "Roz" in call.data and "Zak" in call.data:
            # results[10] = "Директор"
            update_message(id_=id_search(user_id=call.message.chat.id), field='post',
                           mean="Директор, Собственник, Директор по оптовому каналу, Специалист по закупкам, Директор по розничному каналу")
            keyboard = types.InlineKeyboardMarkup()
            keyboard.row(types.InlineKeyboardButton(text="Далее",
                                                    callback_data="callback_c_post_dalee"))
            bot.send_message(
                text="Выбрано: Директор, Собственник, Директор по оптовому каналу, Специалист по закупкам, Директор по розничному каналу\nДолжность клиента. Если несколько, то дополните позже.",
                chat_id=call.message.chat.id, reply_markup=keyboard)



        elif "zak" in call.data:
            # results[10] = "Директор"
            update_message(id_=id_search(user_id=call.message.chat.id), field='post',
                           mean="Специалист по закупкам")

            keyboard = types.InlineKeyboardMarkup()
            keyboard.row(types.InlineKeyboardButton(text="Директор",
                                                    callback_data="callback_c_post_del_Zak_Dir"))
            keyboard.row(types.InlineKeyboardButton(text="Собственник",
                                                    callback_data="callback_c_post_del_Zak_Sob"))
            keyboard.row(types.InlineKeyboardButton(text="Директор по оптовому каналу",
                                                    callback_data="callback_c_post_del_Zak_Opt"))
            keyboard.row(types.InlineKeyboardButton(text="Директор по розничному каналу",
                                                    callback_data="callback_c_post_del_Zak_Roz"))
            keyboard.row(types.InlineKeyboardButton(text="Далее",
                                                    callback_data="callback_c_post_dalee"))
            bot.send_message(text="Выбрано: Специалист по закупкам \nДолжность клиента. Если несколько, то дополните позже.",
                                  chat_id=call.message.chat.id, reply_markup=keyboard)

        elif "Dir" not in call.data and "Sob" in call.data and "Opt" not in call.data and "Roz" not in call.data and "Zak" in call.data:
            # results[10] = "Директор"
            update_message(id_=id_search(user_id=call.message.chat.id), field='post',
                           mean="Собственник, Специалист по закупкам")

            keyboard = types.InlineKeyboardMarkup()
            keyboard.row(types.InlineKeyboardButton(text="Директор",
                                                    callback_data="callback_c_post_del_Zak_Sob_Dir"))
            keyboard.row(types.InlineKeyboardButton(text="Директор по оптовому каналу",
                                                    callback_data="callback_c_post_del_Zak_Sob_Opt"))
            keyboard.row(types.InlineKeyboardButton(text="Директор по розничному каналу",
                                                    callback_data="callback_c_post_del_Zak_Sob_Roz"))
            keyboard.row(types.InlineKeyboardButton(text="Далее",
                                                    callback_data="callback_c_post_dalee"))
            bot.send_message(text="Выбрано: Собственник, Специалист по закупкам \nДолжность клиента. Если несколько, то дополните позже.",
                                  chat_id=call.message.chat.id, reply_markup=keyboard)

        elif "Dir" not in call.data and "Sob" not in call.data and "Opt" in call.data and "Roz" not in call.data and "Zak" in call.data:
            # results[10] = "Директор"
            update_message(id_=id_search(user_id=call.message.chat.id), field='post',
                           mean="Директор по оптовому каналу, Специалист по закупкам")

            keyboard = types.InlineKeyboardMarkup()
            keyboard.row(types.InlineKeyboardButton(text="Директор",
                                                    callback_data="callback_c_post_del_Zak_Opt_Dir"))
            keyboard.row(types.InlineKeyboardButton(text="Собственник",
                                                    callback_data="callback_c_post_del_Zak_Opt_Sob"))

            keyboard.row(types.InlineKeyboardButton(text="Директор по розничному каналу",
                                                    callback_data="callback_c_post_del_Zak_Opt_Roz"))

            keyboard.row(types.InlineKeyboardButton(text="Далее",
                                                    callback_data="callback_c_post_dalee"))
            bot.send_message(text="Выбрано: Директор по оптовому каналу, Специалист по закупкам \nДолжность клиента. Если несколько, то дополните позже.",
                                  chat_id=call.message.chat.id, reply_markup=keyboard)



        elif "Dir" not in call.data and "Sob" not in call.data and "Opt" not in call.data and "Roz"  in call.data and "Zak" in call.data:
            # results[10] = "Директор"
            update_message(id_=id_search(user_id=call.message.chat.id), field='post',
                           mean="Директор по розничному каналу, Специалист по закупкам")

            keyboard = types.InlineKeyboardMarkup()
            keyboard.row(types.InlineKeyboardButton(text="Директор",
                                                    callback_data="callback_c_post_del_Zak_Roz_Dir"))
            keyboard.row(types.InlineKeyboardButton(text="Собственник",
                                                    callback_data="callback_c_post_del_Zak_Roz_Sob"))
            keyboard.row(types.InlineKeyboardButton(text="Директор по оптовому каналу",
                                                    callback_data="callback_c_post_del_Zak_Roz_Opt"))

            keyboard.row(types.InlineKeyboardButton(text="Далее",
                                                    callback_data="callback_c_post_dalee"))
            bot.send_message(text="Выбрано: Директор по розничному каналу, Специалист по закупкам \nДолжность клиента. Если несколько, то дополните позже.",
                                  chat_id=call.message.chat.id, reply_markup=keyboard)


        elif "Dir" not in call.data and "Sob" in call.data and "Opt" in call.data and "Roz" not in call.data and "Zak" in call.data:
            update_message(id_=id_search(user_id=call.message.chat.id), field='post',
                           mean="Собственник, Специалист по закупкам, Директор по оптовому каналу")
            keyboard = types.InlineKeyboardMarkup()
            keyboard.row(types.InlineKeyboardButton(text="Директор",
                                                    callback_data="callback_c_post_del_Zak_Sob_Opt_Dir"))
            keyboard.row(types.InlineKeyboardButton(text="Директор по розничному каналу",
                                                    callback_data="callback_c_post_del_Zak_Sob_Opt_Roz"))
            keyboard.row(types.InlineKeyboardButton(text="Далее",
                                                    callback_data="callback_c_post_dalee"))
            bot.send_message(
                text="Выбрано: Собственник, Директор по оптовому каналу, Специалист по закупкам \nДолжность клиента. Если несколько, то дополните позже.",
                chat_id=call.message.chat.id, reply_markup=keyboard)

        elif "Dir" not in call.data and "Sob" in call.data and "Opt" not in call.data and "Roz" in call.data and "Zak" in call.data:
            update_message(id_=id_search(user_id=call.message.chat.id), field='post',
                           mean="Собственник, Специалист по закупкам, Директор по розничному каналу")
            keyboard = types.InlineKeyboardMarkup()
            keyboard.row(types.InlineKeyboardButton(text="Директор",
                                                    callback_data="callback_c_post_del_Zak_Sob_Roz_Dir"))
            keyboard.row(types.InlineKeyboardButton(text="Директор по розничному каналу",
                                                    callback_data="callback_c_post_del_Zak_Sob_Roz_Opt"))
            keyboard.row(types.InlineKeyboardButton(text="Далее",
                                                    callback_data="callback_c_post_dalee"))
            bot.send_message(
                text="Выбрано: Собственник, Директор по розничному каналу, Специалист по закупкам \nДолжность клиента. Если несколько, то дополните позже.",
                chat_id=call.message.chat.id, reply_markup=keyboard)

        elif "Dir" not in call.data and "Sob" in call.data and "Opt" in call.data and "Roz" in call.data and "Zak" in call.data:
            update_message(id_=id_search(user_id=call.message.chat.id), field='post',
                           mean="Собственник, Директор по оптовому каналу, Директор по розничному каналу, Специалист по закупкам")
            keyboard = types.InlineKeyboardMarkup()
            keyboard.row(types.InlineKeyboardButton(text="Директор",
                                                    callback_data="callback_c_post_del_Zak_Sob_Roz_Dir_Opt"))
            keyboard.row(types.InlineKeyboardButton(text="Далее",
                                                    callback_data="callback_c_post_dalee"))
            bot.send_message(
                text="Выбрано: Собственник, Директор по оптовому каналу, Директор по розничному каналу, Специалист по закупкам \nДолжность клиента. Если несколько, то дополните позже.",
                chat_id=call.message.chat.id, reply_markup=keyboard)


        # elif "zak" in call.data:
        #     update_message(id_=id_search(user_id=call.message.chat.id), field='post',
        #                    mean="Специалист по закупкам")
        #     keyboard = types.InlineKeyboardMarkup()
        #     keyboard.row(types.InlineKeyboardButton(text="Директор",
        #                                             callback_data="callback_c_post_delZak_Dir"))
        #     keyboard.row(types.InlineKeyboardButton(text="Собственник",
        #                                             callback_data="callback_c_post_delZak_Sob"))
        #     keyboard.row(types.InlineKeyboardButton(text="Директор по оптовому каналу",
        #                                             callback_data="callback_c_post_delZak_Opt"))
        #     keyboard.row(types.InlineKeyboardButton(text="Директор по розничному каналу",
        #                                             callback_data="callback_c_post_delZak_Roz"))
        #
        #     keyboard.row(types.InlineKeyboardButton(text="Далее",
        #                                             callback_data="callback_c_post_dalee"))
        #     bot.edit_message_text(text="Выбрано: Специалист по закупкам \nДолжность клиента. Если несколько, то дополните позже.",
        #                           chat_id=call.message.chat.id, message_id=call.message.message_id,
        #                           reply_markup=keyboard)
        elif "sob" in call.data:
            update_message(id_=id_search(user_id=call.message.chat.id), field='post',
                           mean="Собственник")

            keyboard = types.InlineKeyboardMarkup()
            keyboard.row(types.InlineKeyboardButton(text="Директор",
                                                    callback_data="callback_c_post_del_Sob_Dir"))
            keyboard.row(types.InlineKeyboardButton(text="Директор по оптовому каналу",
                                                    callback_data="callback_c_post_del_Sob_Opt"))
            keyboard.row(types.InlineKeyboardButton(text="Директор по розничному каналу",
                                                    callback_data="callback_c_post_del_Sob_Roz"))
            keyboard.row(types.InlineKeyboardButton(text="Специалист по закупкам",
                                                    callback_data="callback_c_post_del_Sob_Zak"))
            keyboard.row(types.InlineKeyboardButton(text="Далее",
                                                    callback_data="callback_c_post_dalee"))
            bot.send_message(
                text="Выбрано: Собственник \nДолжность клиента. Если несколько, то дополните позже.",
                chat_id=call.message.chat.id, reply_markup=keyboard)

        elif "Dir" not in call.data and "Sob" in call.data and "Opt" in call.data and "Roz" not in call.data and "Zak" not in call.data:
            update_message(id_=id_search(user_id=call.message.chat.id), field='post',
                           mean="Собственник, Директор по оптовому каналу")

            keyboard = types.InlineKeyboardMarkup()
            keyboard.row(types.InlineKeyboardButton(text="Директор",
                                                    callback_data="callback_c_post_del_Sob_Opt_Dir"))
            keyboard.row(types.InlineKeyboardButton(text="Директор по розничному каналу",
                                                    callback_data="callback_c_post_del_Sob_Opt_Roz"))
            keyboard.row(types.InlineKeyboardButton(text="Специалист по закупкам",
                                                    callback_data="callback_c_post_del_Sob_Opt_Zak"))
            keyboard.row(types.InlineKeyboardButton(text="Далее",
                                                    callback_data="callback_c_post_dalee"))
            bot.send_message(
                text="Выбрано: Собственник, Директор по оптовому каналу \nДолжность клиента. Если несколько, то дополните позже.",
                chat_id=call.message.chat.id, reply_markup=keyboard)





        elif "Dir" not in call.data and "Sob" in call.data and "Opt" not in call.data and "Roz" in call.data and "Zak" not in call.data:
            update_message(id_=id_search(user_id=call.message.chat.id), field='post',
                           mean="Собственник, Директор по розничному каналу")

            keyboard = types.InlineKeyboardMarkup()
            keyboard.row(types.InlineKeyboardButton(text="Директор",
                                                    callback_data="callback_c_post_del_Sob_Roz_Dir"))
            keyboard.row(types.InlineKeyboardButton(text="Директор по оптовому каналу",
                                                    callback_data="callback_c_post_del_Sob_Roz_Opt"))
            keyboard.row(types.InlineKeyboardButton(text="Специалист по закупкам",
                                                    callback_data="callback_c_post_del_Sob_Roz_Zak"))
            keyboard.row(types.InlineKeyboardButton(text="Далее",
                                                    callback_data="callback_c_post_dalee"))
            bot.send_message(
                text="Выбрано: Собственник, Директор по розничному каналу \nДолжность клиента. Если несколько, то дополните позже.",
                chat_id=call.message.chat.id, reply_markup=keyboard)

        elif "Dir" not in call.data and "Sob" in call.data and "Opt" in call.data and "Roz" in call.data and "Zak" not in call.data:
            update_message(id_=id_search(user_id=call.message.chat.id), field='post',
                           mean="Собственник, Директор по оптовому каналу, Директор по розничному каналу")

            keyboard = types.InlineKeyboardMarkup()
            keyboard.row(types.InlineKeyboardButton(text="Директор",
                                                    callback_data="callback_c_post_del_Sob_Opt_Roz_Dir"))
            keyboard.row(types.InlineKeyboardButton(text="Специалист по закупкам",
                                                    callback_data="callback_c_post_del_Sob_Opt_Roz_Zak"))
            keyboard.row(types.InlineKeyboardButton(text="Далее",
                                                    callback_data="callback_c_post_dalee"))
            bot.send_message(
                text="Выбрано: Собственник, Директор по оптовому каналу, Директор по розничному каналу \nДолжность клиента. Если несколько, то дополните позже.",
                chat_id=call.message.chat.id, reply_markup=keyboard)




        elif "opt" in call.data:
            update_message(id_=id_search(user_id=call.message.chat.id), field='post',
                           mean="Директор по оптовому каналу")

            keyboard = types.InlineKeyboardMarkup()
            keyboard.row(types.InlineKeyboardButton(text="Директор",
                                                    callback_data="callback_c_post_del_Opt_Dir"))
            keyboard.row(types.InlineKeyboardButton(text="Собственник",
                                                    callback_data="callback_c_post_del_Opt_Sob"))
            keyboard.row(types.InlineKeyboardButton(text="Директор по розничному каналу",
                                                    callback_data="callback_c_post_del_Opt_Roz"))
            keyboard.row(types.InlineKeyboardButton(text="Специалист по закупкам",
                                                    callback_data="callback_c_post_del_Opt_Zak"))
            keyboard.row(types.InlineKeyboardButton(text="Далее",
                                                    callback_data="callback_c_post_dalee"))
            bot.send_message(
                text="Выбрано: Директор по оптовому каналу \nДолжность клиента. Если несколько, то дополните позже.",
                chat_id=call.message.chat.id, reply_markup=keyboard)

        elif "Dir" not in call.data and "Sob" not in call.data and "Opt" in call.data and "Roz" in call.data and "Zak" not in call.data:
            update_message(id_=id_search(user_id=call.message.chat.id), field='post',
                           mean="Директор по оптовому каналу, Директор по розничному каналу")

            keyboard = types.InlineKeyboardMarkup()
            keyboard.row(types.InlineKeyboardButton(text="Директор",
                                                    callback_data="callback_c_post_del_Opt_Roz_Dir"))
            keyboard.row(types.InlineKeyboardButton(text="Собственник",
                                                    callback_data="callback_c_post_del_Opt_Roz_Sob"))
            keyboard.row(types.InlineKeyboardButton(text="Специалист по закупкам",
                                                    callback_data="callback_c_post_del_Opt_Roz_Zak"))
            keyboard.row(types.InlineKeyboardButton(text="Далее",
                                                    callback_data="callback_c_post_dalee"))
            bot.send_message(
                text="Выбрано: Директор по оптовому каналу, Директор по розничному каналу \nДолжность клиента. Если несколько, то дополните позже.",
                chat_id=call.message.chat.id, reply_markup=keyboard)




        # elif "sob" in call.data:
        #     # results[10] = "Собственник"
        #     update_message(id_=id_search(user_id=call.message.chat.id), field='post',
        #                    mean="Собственник")
        # elif "opt" in call.data:
        #     # results[10] = "Директор по оптовому каналу"
        #     update_message(id_=id_search(user_id=call.message.chat.id), field='post',
        #                    mean="Директор по оптовому каналу")
        elif "roz" in call.data:
            update_message(id_=id_search(user_id=call.message.chat.id), field='post',
                           mean="Директор по розничному каналу")

            keyboard = types.InlineKeyboardMarkup()
            keyboard.row(types.InlineKeyboardButton(text="Директор",
                                                    callback_data="callback_c_post_del_Roz_Dir"))
            keyboard.row(types.InlineKeyboardButton(text="Собственник",
                                                    callback_data="callback_c_post_del_Roz_Sob"))
            keyboard.row(types.InlineKeyboardButton(text="Директор по оптовому каналу",
                                                    callback_data="callback_c_post_del_Roz_Opt"))
            keyboard.row(types.InlineKeyboardButton(text="Специалист по закупкам",
                                                    callback_data="callback_c_post_del_Roz_Zak"))
            keyboard.row(types.InlineKeyboardButton(text="Далее",
                                                    callback_data="callback_c_post_dalee"))
            bot.send_message(
                text="Выбрано: Директор по розничному каналу \nДолжность клиента. Если несколько, то дополните позже.",
                chat_id=call.message.chat.id, reply_markup=keyboard)

        # elif "roz" in call.data:
        #     # results[10] = "Директор по розничному каналу"
        #     update_message(id_=id_search(user_id=call.message.chat.id), field='post',
        #                    mean="Директор по розничному каналу")
        elif "dalee" in call.data:
            bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Укажите название торговой точки"),
                                       c_direction)

    elif call.data == "callback_c_dir_d":
        bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Уточните данные"), c_field)


    elif "callback_c_dir" in call.data:
        print(call.data)
        if "opt" in call.data:
            # results[11] = "Оптовая торговля"
            update_message(id_=id_search(user_id=call.message.chat.id), field='direction',
                           mean="Оптовая торговля")
        elif "rok" in call.data:
            # results[11] = "Корпоративные продажи"
            update_message(id_=id_search(user_id=call.message.chat.id), field='direction',
                           mean="Корпоративные продажи")
        elif "int" in call.data:
            # results[11] = "Интернет"
            update_message(id_=id_search(user_id=call.message.chat.id), field='direction',
                           mean="Интернет")
        elif "roz" in call.data:
            # results[11] = "Розница"
            update_message(id_=id_search(user_id=call.message.chat.id), field='direction',
                           mean="Розница")

        keyboard = types.InlineKeyboardMarkup(row_width=3)
        keyboard.add(types.InlineKeyboardButton(text="Канцелярия",
                                                callback_data="callback_c_field_kan"),
                     types.InlineKeyboardButton(text="Детские товары",
                                                callback_data="callback_c_field_det"),
                     types.InlineKeyboardButton(text="Книги",
                                                callback_data="callback_c_field_kni"),
                     types.InlineKeyboardButton(text="Сумки",
                                                callback_data="callback_c_field_sum"),
                     types.InlineKeyboardButton(text="Сувениры",
                                                callback_data="callback_c_field_suv"),
                     types.InlineKeyboardButton(text="Другое",
                                                callback_data="callback_c_field_d")
                     )
        bot.send_message(call.message.chat.id, "Укажите сферу:", reply_markup=keyboard)

    elif call.data == "callback_c_field_d":
        bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Уточните данные"), c_offline)

    elif "callback_c_field" in call.data:
        if "kan" in call.data:
            # results[12] = "Канцелярия"
            update_message(id_=id_search(user_id=call.message.chat.id), field='field',
                           mean="Канцелярия")
        elif "det" in call.data:
            # results[12] = "Детские товары"
            update_message(id_=id_search(user_id=call.message.chat.id), field='field',
                           mean="Детские товары")
        elif "kni" in call.data:
            # results[12] = "Книги"
            update_message(id_=id_search(user_id=call.message.chat.id), field='field',
                           mean="Книги")
        elif "sum" in call.data:
            # results[12] = "Сумки"
            update_message(id_=id_search(user_id=call.message.chat.id), field='field',
                           mean="Сумки")
        elif "suv" in call.data:
            # results[12] = "Сувениры"
            update_message(id_=id_search(user_id=call.message.chat.id), field='field',
                           mean="Сувениры")
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        keyboard.add(types.InlineKeyboardButton(text="✅Есть",
                                                callback_data="callback_c_offline_yes"),
                     types.InlineKeyboardButton(text="❌Нет",
                                                callback_data="callback_c_offline_no"),
                     )
        bot.send_message(call.message.chat.id, "Наличие оффлайн точек:", reply_markup=keyboard)


    elif call.data == "callback_c_offline_yes":
        # results[13] = "Да"
        update_message(id_=id_search(user_id=call.message.chat.id), field='offline',
                       mean="Да")
        bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Укажите количество"), c_assort)


    elif call.data == "callback_c_offline_no":
        # results[13] = "Нет"
        update_message(id_=id_search(user_id=call.message.chat.id), field='offline',
                       mean="Нет")
        keyboard = types.InlineKeyboardMarkup()
        keyboard.row(types.InlineKeyboardButton(text="Интересна вся продукция",
                                                callback_data="callback_c_assort_prod"))
        keyboard.row(types.InlineKeyboardButton(text="Интересна некоторая продукция",
                                                callback_data="callback_c_assort_some"))
        keyboard.row(types.InlineKeyboardButton(text="Офис",
                                                callback_data="callback_c_assort_ofi"),
                     types.InlineKeyboardButton(text="Пластик",
                                                callback_data="callback_c_assort_spa"),
                     types.InlineKeyboardButton(text="Бумажно-беловая",
                                                callback_data="callback_c_assort_bum"))
        keyboard.row(types.InlineKeyboardButton(text="Сумки-рюкзаки",
                                                callback_data="callback_c_assort_sum"),
                     types.InlineKeyboardButton(text="Творчество",
                                                callback_data="callback_c_assort_two"))
        bot.send_message(call.message.chat.id, "Укажите интересующий ассортимент.", reply_markup=keyboard)


    elif "callback_c_assort" in call.data:
        if "some" in call.data:
            bot.register_next_step_handler(bot.send_message(call.message.chat.id, ("Введите через пробел номер интересующего Вас ассортимента:\n"
                                                    "1. Офис\n"
                                                    "2. Пластик\n"
                                                    "3. Бумажно-беловая прод.\n"
                                                    "4. Сумки-рюкзаки\n"
                                                    "5. Творчество\n")), c_some_assort)
        else:
            if "prod" in call.data:
                # results[15] = "Интересна вся продукция"
                update_message(id_=id_search(user_id=call.message.chat.id), field='interest',
                               mean="Интересна вся продукция")
            elif "ofi" in call.data:
                # results[15] = "Офис"
                update_message(id_=id_search(user_id=call.message.chat.id), field='interest',
                               mean="Офис")
            elif "spa" in call.data:
                # results[15] = "Пластик"
                update_message(id_=id_search(user_id=call.message.chat.id), field='interest',
                               mean="Пластик")
            elif "bum" in call.data:
                # results[15] = "Бумажно-беловая"
                update_message(id_=id_search(user_id=call.message.chat.id), field='interest',
                               mean="Бумажно-беловая")
            elif "sum" in call.data:
                # results[15] = "Сумки-рюкзаки"
                update_message(id_=id_search(user_id=call.message.chat.id), field='interest',
                               mean="Сумки-рюкзаки")
            elif "two" in call.data:
                # results[15] = "Творчество"
                update_message(id_=id_search(user_id=call.message.chat.id), field='interest',
                               mean="Творчество")
            keyboard = types.InlineKeyboardMarkup(row_width=3)
            keyboard.add(types.InlineKeyboardButton(text="✅Да",
                                                    callback_data="callback_c_comment_yes"),
                         types.InlineKeyboardButton(text="❌Нет",
                                                    callback_data="callback_c_comment_no"),
                         )
            bot.send_message(call.message.chat.id, "У вас есть комментарии по заполненной анкете?", reply_markup=keyboard)


    elif call.data == "callback_c_comment_no":
        # results[16] = "Нет"
        update_message(id_=id_search(user_id=call.message.chat.id), field='com',
                       mean="Нет")
        bot.register_next_step_handler(
            bot.send_message(call.message.chat.id, ("Спасибо за заполнение анкеты, все данные сохранены! 🎉\n"
                                                    f"*Ваш универсальный номер: {random.randint(10000,90000)}-{iid[0]}. Покажите его сотруднику на *"
                                                    "*стойке регистрации на стенде ErichKrause и получите подарок. *"
                                                    "🎁"), parse_mode='Markdown'), c_pass)
        iid[0] = iid[0] + 1

    elif call.data == "callback_c_comment_yes":
        # results[16] = "Да"
        update_message(id_=id_search(user_id=call.message.chat.id), field='com',
                       mean="Да")
        bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Укажите Ваш комментарий"), c_finish)

        #############################


@bot.message_handler(content_types='text')
def m_m_fio(message):
    # results[2] = message.text
    print("ready1")
    update_message(id_=id_search(user_id=message.chat.id), field='division',
                   mean=message.text)
    print("ready2")
    bot.register_next_step_handler(bot.send_message(message.chat.id, "Ваше ФИО"), m_fio)


@bot.message_handler(content_types='text')
def m_fio(message):
    # results[3] = message.text
    update_message(id_=id_search(user_id=message.chat.id), field='manager_fio',
                   mean=message.text)
    bot.register_next_step_handler(bot.send_message(message.chat.id, "ФИО клиента"), m_coop)


def m_coop(message):
    # results[4] = message.text
    update_message(id_=id_search(user_id=message.chat.id), field='client_fio',
                   mean=message.text)
    # keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(types.InlineKeyboardButton(text="✅Да",
                                            callback_data="callback_m_coop_yes"),
                 types.InlineKeyboardButton(text="❌Нет",
                                            callback_data="callback_m_coop_no"),
                 types.InlineKeyboardButton(text="Другое",
                                            callback_data="callback_m_coop_d")
                 )
    keyboard.row(types.InlineKeyboardButton(text="🔄Работали ранее, но прекратили",
                                            callback_data="callback_m_coop_worked"))
    bot.send_message(message.chat.id, "Ранее было сотрудничество с «Офис Премьер»?", reply_markup=keyboard)


@bot.message_handler(content_types='text')
def m_city(message):
    # results[5] = message.text
    update_message(id_=id_search(user_id=message.chat.id), field='coop',
                   mean=message.text)
    bot.register_next_step_handler(
        bot.send_message(message.chat.id, "Город офиса клиента. Если несколько – введите через пробела"), m_region)


@bot.message_handler(content_types='text')
def m_region(message):
    # results[6] = message.text
    update_message(id_=id_search(user_id=message.chat.id), field='city',
                   mean=message.text)
    bot.register_next_step_handler(bot.send_message(message.chat.id, "Регионы продаж клиента"), m_phone)


@bot.message_handler(content_types='text')
def m_phone(message):
    # results[7] = message.text
    update_message(id_=id_search(user_id=message.chat.id), field='region',
                   mean=message.text)
    bot.register_next_step_handler(
        bot.send_message(message.chat.id, "Введите номер телефона клиента в международном формате (начинается с +)"),
        m_phone_sure)



def m_phone_sure(message):
    if re.findall(r'\+\d{10,13}$', message.text):
        update_message(id_=id_search(user_id=message.chat.id), field='phone',
                       mean=message.text)
        bot.register_next_step_handler(
            bot.send_message(message.chat.id,
                             "Вы ввели верный номер телефона? Введите *Да* или *Нет*", parse_mode='Markdown'),
            m_email)
        print(message.text)

    else:
        bot.register_next_step_handler(bot.send_message(message.chat.id, "❗️Кажется, Вы ошиблись. Номер телефона "
                                                                         "должен начинаться с + и включать в себя "
                                                                         "только цифры. Перепроверьте правильность "
                                                                         "данных"), m_phone_sure)


@bot.message_handler(content_types='text')
def m_email(message):
    print(message.text)
    if message.text.lower() == "да":
        bot.register_next_step_handler(bot.send_message(message.chat.id, "Введите e-mail клиента"), m_email_sure)
    elif message.text.lower() == "нет":
        bot.register_next_step_handler(bot.send_message(message.chat.id, "Введите номер телефона клиента в "
                                                                         "международном формате (начинается с "
                                                                         "+)"), m_phone_sure)
    else:
        bot.register_next_step_handler(
            bot.send_message(message.chat.id, "Вы ввели верный номер телефона? Введите *Да* или *Нет*",
                             parse_mode='Markdown'), m_email)

def m_email_sure(message):
    if re.findall(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?", message.text):
        update_message(id_=id_search(user_id=message.chat.id), field='email',
                       mean=message.text)
        bot.register_next_step_handler(
            bot.send_message(message.chat.id, "Вы ввели верный email? Введите *Да* или *Нет*",
                             parse_mode='Markdown'), m_post)

    else:
        bot.register_next_step_handler(bot.send_message(message.chat.id,
                                                        "❗❗️Перепроверьте правильность данных и введите e-mail снова. Почта должна содержать символы «@» и «.»"),
                                       m_email_sure)

# @bot.callback_query_handler(func=lambda call: "callback_m_post" in call.data)
# def m_post_mass(call):
#     if "dir" in call.data:





def m_post(message):
    if message.text.lower() == "да":
        keyboard = types.InlineKeyboardMarkup()
        keyboard.row(types.InlineKeyboardButton(text="Директор",
                                                callback_data="callback_m_post_dir"),
                     types.InlineKeyboardButton(text="Собственник",
                                                callback_data="callback_m_post_sob"))
        keyboard.row(types.InlineKeyboardButton(text="Директор по оптовому каналу",
                                                callback_data="callback_m_post_opt"))
        keyboard.row(types.InlineKeyboardButton(text="Директор по розничному каналу",
                                                callback_data="callback_m_post_roz"))
        keyboard.row(types.InlineKeyboardButton(text="Специалист по закупкам",
                                                callback_data="callback_m_post_zak"),
                     types.InlineKeyboardButton(text="Другое",
                                                callback_data="callback_m_post_d"))
        bot.send_message(message.chat.id, "Должность клиента. Если несколько, то дополните позже.",
                         reply_markup=keyboard)

    elif message.text.lower() == "нет":
        bot.register_next_step_handler(bot.send_message(message.chat.id, "Введите Ваш e-mail"), m_email_sure)
    else:
        bot.register_next_step_handler(
            bot.send_message(message.chat.id, "Вы ввели верный email? Введите *Да* или *Нет*",
                             parse_mode='Markdown'), m_post)


@bot.message_handler(content_types='text')
def m_point(message):
    # results[10] = message.text
    update_message(id_=id_search(user_id=message.chat.id), field='post',
                   mean=message.text)
    bot.register_next_step_handler(bot.send_message(message.chat.id, "Укажите название торговой точки"), m_direction)


def m_direction(message):
    # results[11] = message.text
    update_message(id_=id_search(user_id=message.chat.id), field='direction',
                   mean=message.text)
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text="Оптовая торговля",
                                            callback_data="callback_m_dir_opt"),
                 types.InlineKeyboardButton(text="Корпоративные продажи",
                                            callback_data="callback_m_dir_kor"),
                 types.InlineKeyboardButton(text="Интернет",
                                            callback_data="callback_m_dir_int"),
                 types.InlineKeyboardButton(text="Розница",
                                            callback_data="callback_m_dir_roz"),
                 types.InlineKeyboardButton(text="Другое",
                                            callback_data="callback_m_dir_d")
                 )
    bot.send_message(message.chat.id, "Укажите направление деятельности. Если несколько, то дополните позже.",
                     reply_markup=keyboard)


def m_field(message):
    # results[11] = message.text
    update_message(id_=id_search(user_id=message.chat.id), field='field',
                   mean=message.text)
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(types.InlineKeyboardButton(text="Канцелярия",
                                            callback_data="callback_m_field_kan"),
                 types.InlineKeyboardButton(text="Детские товары",
                                            callback_data="callback_m_field_det"),
                 types.InlineKeyboardButton(text="Книги",
                                            callback_data="callback_m_field_kni"),
                 types.InlineKeyboardButton(text="Сумки",
                                            callback_data="callback_m_field_sum"),
                 types.InlineKeyboardButton(text="Сувениры",
                                            callback_data="callback_m_field_suv"),
                 types.InlineKeyboardButton(text="Другое",
                                            callback_data="callback_m_field_d")
                 )
    bot.send_message(message.chat.id, "Укажите сферу деятельности:", reply_markup=keyboard)


def m_offline(message):
    # results[12] = message.text
    update_message(id_=id_search(user_id=message.chat.id), field='offline',
                   mean=message.text)
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(types.InlineKeyboardButton(text="✅Есть",
                                            callback_data="callback_m_offline_yes"),
                 types.InlineKeyboardButton(text="❌Нет",
                                            callback_data="callback_m_offline_no"),
                 )
    bot.send_message(message.chat.id, "Наличие оффлайн точек:", reply_markup=keyboard)

def m_some_assort(message):
    update_message(id_=id_search(user_id=message.chat.id), field='interest',
                   mean=message.text)
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(types.InlineKeyboardButton(text="✅Да",
                                            callback_data="callback_m_comment_yes"),
                 types.InlineKeyboardButton(text="❌Нет",
                                            callback_data="callback_m_comment_no"),
                 )
    bot.send_message(message.chat.id, "У вас есть комментарии по заполненной анкете?", reply_markup=keyboard)


def m_assort(message):
    # results[14] = message.text
    update_message(id_=id_search(user_id=message.chat.id), field='count',
                   mean=message.text)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(types.InlineKeyboardButton(text="Интересна вся продукция",
                                            callback_data="callback_m_assort_prod"))
    keyboard.row(types.InlineKeyboardButton(text="Интересна некоторая продукция",
                                            callback_data="callback_m_assort_some"))
    keyboard.row(types.InlineKeyboardButton(text="Офис",
                                            callback_data="callback_m_assort_ofi"),
                 types.InlineKeyboardButton(text="Пластик",
                                            callback_data="callback_m_assort_spa"),
                 types.InlineKeyboardButton(text="Бумажно-беловая",
                                            callback_data="callback_m_assort_bum"))
    keyboard.row(types.InlineKeyboardButton(text="Сумки-рюкзаки",
                                            callback_data="callback_m_assort_sum"),
                 types.InlineKeyboardButton(text="Творчество",
                                            callback_data="callback_m_assort_two"))
    bot.send_message(message.chat.id, "Укажите интересующий ассортимент.", reply_markup=keyboard)


def m_finish(message):
    # results[17] = message.text
    update_message(id_=id_search(user_id=message.chat.id), field='comment',
                   mean=message.text)
    # add_message(user_id=results[18], data=results)
    bot.send_message(message.chat.id, ("Спасибо за заполнение анкеты, все данные сохранены! 🎉\n"
                                       f"*Универсальный номер анкеты: {random.randint(10000,90000)}{iid[0]},*"
                                       " *по нему клиент может получить подарок.*"), parse_mode='Markdown')
    iid[0] = iid[0] + 1

    m_pass()


def m_pass():
    add_excel()


###############
def c_coop(message):
    # results[4] = message.text
    update_message(id_=id_search(user_id=message.chat.id), field='client_fio',
                   mean=message.text)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(types.InlineKeyboardButton(text="✅Да",
                                            callback_data="callback_c_coop_yes"),
                 types.InlineKeyboardButton(text="❌Нет",
                                            callback_data="callback_c_coop_no"),
                 types.InlineKeyboardButton(text="Другое",
                                            callback_data="callback_c_coop_d"
                                            ))
    keyboard.row(types.InlineKeyboardButton(text="🔄Работали ранее, но прекратили",
                                            callback_data="callback_c_coop_worked"))

    bot.send_message(message.chat.id, "Ранее было сотрудничество с «Офис Премьер»?", reply_markup=keyboard)


@bot.message_handler(content_types='text')
def c_city(message):
    # results[5] = message.text
    update_message(id_=id_search(user_id=message.chat.id), field='coop',
                   mean=message.text)
    bot.register_next_step_handler(bot.send_message(message.chat.id, "Город Вашего офиса"), c_region)


@bot.message_handler(content_types='text')
def c_region(message):
    # results[6] = message.text
    update_message(id_=id_search(user_id=message.chat.id), field='city',
                   mean=message.text)
    bot.register_next_step_handler(bot.send_message(message.chat.id, "Регионы ваших продаж"), c_phone)


@bot.message_handler(content_types='text')
def c_phone(message):
    # results[7] = message.text
    update_message(id_=id_search(user_id=message.chat.id), field='region',
                   mean=message.text)
    bot.register_next_step_handler(
        bot.send_message(message.chat.id, "Ваш номер телефона в международном формате (начинается с +)"), c_email)


def c_phone_sure(message):
    if re.findall(r'\+\d{10,13}$', message.text):
        update_message(id_=id_search(user_id=message.chat.id), field='phone',
                       mean=message.text)
        bot.register_next_step_handler(
            bot.send_message(message.chat.id, "Вы ввели верный номер телефона? Введите *Да* или *Нет*",
                             parse_mode='Markdown'), c_email)
        print(message.text)

    else:
        bot.register_next_step_handler(bot.send_message(message.chat.id, "❗️Кажется, Вы ошиблись. Номер телефона "
                                                                         "должен начинаться с + и включать в себя "
                                                                         "только цифры. Перепроверьте правильность "
                                                                         "данных"), c_phone_sure)


@bot.message_handler(content_types='text')
def c_email(message):
    print(message.text)
    if message.text.lower() == "да":
        bot.register_next_step_handler(bot.send_message(message.chat.id, "Введите ваш e-mail"), c_email_sure)
    elif message.text.lower() == "нет":
        bot.register_next_step_handler(bot.send_message(message.chat.id, "Введите ваш номер телефона в "
                                                                         "международном формате (начинается с "
                                                                         "+)"), c_phone_sure)
    else:
        bot.register_next_step_handler(
            bot.send_message(message.chat.id, "Вы ввели верный номер телефона? Введите *Да* или *Нет*",
                             parse_mode='Markdown'), c_email)

def c_email_sure(message):
    if re.findall(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?", message.text):
        update_message(id_=id_search(user_id=message.chat.id), field='email',
                       mean=message.text)
        bot.register_next_step_handler(
            bot.send_message(message.chat.id, "Вы ввели верный email? Введите *Да* или *Нет*",
                             parse_mode='Markdown'), c_post)

    else:
        bot.register_next_step_handler(
            bot.send_message(message.chat.id,
                             "❗❗️Перепроверьте правильность данных и введите e-mail снова. Почта должна содержать символы «@» и «.»"),
            c_email_sure)


def c_post(message):
    if message.text.lower() == "да":
        keyboard = types.InlineKeyboardMarkup()
        keyboard.row(types.InlineKeyboardButton(text="Директор",
                                                callback_data="callback_c_post_dir"),
                     types.InlineKeyboardButton(text="Собственник",
                                                callback_data="callback_c_post_sob")
                     )
        keyboard.row(types.InlineKeyboardButton(text="Директор по оптовому каналу",
                                                callback_data="callback_c_post_opt"))
        keyboard.row(types.InlineKeyboardButton(text="Директор по розничному каналу",
                                                callback_data="callback_c_post_roz"))
        keyboard.row(types.InlineKeyboardButton(text="Специалист по закупкам",
                                                callback_data="callback_c_post_zak"),
                     types.InlineKeyboardButton(text="Другое",
                                                callback_data="callback_c_post_d"))
        bot.send_message(message.chat.id, "Ваша должность. Если несколько, то дополните позже.",
                         reply_markup=keyboard)


    elif message.text.lower() == "нет":
        bot.register_next_step_handler(bot.send_message(message.chat.id, "Введите Ваш e-mail"), c_email_sure)
    else:
        bot.register_next_step_handler(
            bot.send_message(
                message.chat.id, "Вы ввели верный email? Введите *Да* или *Нет*",
                parse_mode='Markdown'), c_post)




@bot.message_handler(content_types='text')
def c_point(message):
    # results[10] = message.text
    update_message(id_=id_search(user_id=message.chat.id), field='post',
                   mean=message.text)
    bot.register_next_step_handler(bot.send_message(message.chat.id, "Укажите название торговой точки"), c_direction)


def c_direction(message):
    # results[11] = message.text
    update_message(id_=id_search(user_id=message.chat.id), field='direction',
                   mean=message.text)

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text="Оптовая торговля",
                                            callback_data="callback_c_dir_opt"),
                 types.InlineKeyboardButton(text="Корпоративные продажи",
                                            callback_data="callback_c_dir_kor"),
                 types.InlineKeyboardButton(text="Интернет",
                                            callback_data="callback_c_dir_int"),
                 types.InlineKeyboardButton(text="Розница",
                                            callback_data="callback_c_dir_roz"),
                 types.InlineKeyboardButton(text="Другое",
                                            callback_data="callback_c_dir_d")
                 )
    bot.send_message(message.chat.id, "Укажите направление деятельности. Если несколько, то дополните позже.",
                     reply_markup=keyboard)


def c_field(message):
    # results[11] = message.text
    update_message(id_=id_search(user_id=message.chat.id), field='field',
                   mean=message.text)
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(types.InlineKeyboardButton(text="Канцелярия",
                                            callback_data="callback_c_field_kan"),
                 types.InlineKeyboardButton(text="Детские товары",
                                            callback_data="callback_c_field_det"),
                 types.InlineKeyboardButton(text="Книги",
                                            callback_data="callback_c_field_kni"),
                 types.InlineKeyboardButton(text="Сумки",
                                            callback_data="callback_c_field_sum"),
                 types.InlineKeyboardButton(text="Сувениры",
                                            callback_data="callback_c_field_suv"),
                 types.InlineKeyboardButton(text="Другое",
                                            callback_data="callback_c_field_d")
                 )
    bot.send_message(message.chat.id, "Укажите сферу деятельности:", reply_markup=keyboard)


def c_offline(message):
    # results[12] = message.text
    update_message(id_=id_search(user_id=message.chat.id), field='offline',
                   mean=message.text)
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(types.InlineKeyboardButton(text="✅Есть",
                                            callback_data="callback_c_offline_yes"),
                 types.InlineKeyboardButton(text="❌Нет",
                                            callback_data="callback_c_offline_no"),
                 )
    bot.send_message(message.chat.id, "Наличие оффлайн точек:", reply_markup=keyboard)

def c_some_assort(message):
    update_message(id_=id_search(user_id=message.chat.id), field='interest',
                   mean=message.text)
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(types.InlineKeyboardButton(text="✅Да",
                                            callback_data="callback_c_comment_yes"),
                 types.InlineKeyboardButton(text="❌Нет",
                                            callback_data="callback_c_comment_no"),
                 )
    bot.send_message(message.chat.id, "У вас есть комментарии по заполненной анкете?", reply_markup=keyboard)

def c_assort(message):
    # results[14] = message.text
    update_message(id_=id_search(user_id=message.chat.id), field='count',
                   mean=message.text)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(types.InlineKeyboardButton(text="Интересна вся продукция",
                                            callback_data="callback_c_assort_prod"))
    keyboard.row(types.InlineKeyboardButton(text="Интересна некоторая продукция",
                                            callback_data="callback_c_assort_some"))
    keyboard.row(types.InlineKeyboardButton(text="Офис",
                                            callback_data="callback_c_assort_ofi"),
                 types.InlineKeyboardButton(text="Пластик",
                                            callback_data="callback_c_assort_spa"),
                 types.InlineKeyboardButton(text="Бумажно-беловая",
                                            callback_data="callback_c_assort_bum"))
    keyboard.row(types.InlineKeyboardButton(text="Сумки-рюкзаки",
                                            callback_data="callback_c_assort_sum"),
                 types.InlineKeyboardButton(text="Творчество",
                                            callback_data="callback_c_assort_two"))
    bot.send_message(message.chat.id, "Укажите интересующий ассортимент.", reply_markup=keyboard)


def c_finish(message):
    # results[17] = message.text
    update_message(id_=id_search(user_id=message.chat.id), field='comment',
                   mean=message.text)
    bot.send_message(message.chat.id,f"Cпасибо за заполнение анкеты, все данные сохранены! 🎉\n *Ваш универсальный номер: {random.randint(10000,90000)}-{iid[0]}*. Покажите его сотруднику на стойке регистрации на стенде ErichKrause и получите подарок. 🎁", parse_mode='Markdown')
    iid[0] = iid[0] + 1
    c_pass()


def c_pass():
    add_excel()

def get_db_data():

    for i in range(1, get_max_id()):
        bot.send_message(chat_id="363674843", text=str(get_db(id_=i)))
    # get_db()

def get_exel():
    f=open("output.xlsx","rb")
    bot.send_document(chat_id="363674843", document=f)


###############

# def delete(call):
#     bot.delete_message(call.message.chat.id, call.message.message_id, 1)
#
#
# def delete_mess(message):
#     bot.delete_message(message.chat.id, message.message_id, 1)
#     bot.delete_message(message.chat.id, message.message_id - 1, 1)


bot.infinity_polling()
