import telebot
from telebot import types
from text import HELLO
from db import init_db, add_message, add_excel, get_number
import random
import re

token = "6380116131:AAEcboCnRR8Inldj914AKc2oBRRG429jZZY"
# token = "6477369209:AAELdd8Lt8cj8m0bbMHewGLgDF9CpSVlYqs"
bot = telebot.TeleBot(token)
results = {a: '' for a in range(19)}


@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = types.InlineKeyboardMarkup(row_width=4)
    keyboard.add(types.InlineKeyboardButton(text="Начать",
                                            callback_data="callback_start_anketa"))
    bot.send_message(message.chat.id, HELLO, reply_markup=keyboard)
    init_db()


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "callback_start_anketa":
        results[18] = call.message.from_user.id
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
        results[0] = call.data.strip("callback_date")
        print(results)
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(types.InlineKeyboardButton(text="Менеджер",
                                                callback_data="callback_manager"),
                     types.InlineKeyboardButton(text="Клиент",
                                                callback_data="callback_client"))
        bot.send_message(call.message.chat.id, "Вы менеджер или клиент?", reply_markup=keyboard)


    elif call.data == "callback_manager":
        results[1] = call.data.strip("callback_")
        print(results)
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
            results[2] = "ДСП"
        elif "drp" in call.data:
            results[2] = "ДРП"
        elif "mez" in call.data:
            results[2] = "Меж.деп"
        print(results)
        bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Ваше ФИО"), m_fio)

    elif call.data == "callback_m_coop_d":
        bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Уточните данные"), m_city)


    elif "callback_m_coop" in call.data:
        if "yes" in call.data:
            results[5] = "Да"
        elif "no" in call.data:
            results[5] = "Нет"
        elif "worked" in call.data:
            results[5] = "Работали ранее, но прекратили"
        print(results)
        bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Город офиса клиента. Если несколько – введите через пробел"), m_region)


    elif call.data == "callback_m_post_d":
        bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Уточните данные"), m_point)


    elif "callback_m_post" in call.data:
        if "dir" in call.data:
            results[10] = "Директор"
        elif "zak" in call.data:
            results[10] = "Специалист по закупкам"
        elif "sob" in call.data:
            results[10] = "Собственник"
        elif "opt" in call.data:
            results[10] = "Директор по оптовому каналу"
        elif "roz" in call.data:
            results[10] = "Директор по розничному каналу"
        print(results)
        bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Укажите название торговой точки"),
                                       m_direction)


    elif call.data == "callback_m_dir_d":
        bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Уточните данные"), m_field)


    elif "callback_m_dir" in call.data:
        if "opt" in call.data:
            results[11] = "Оптовая торговля"
        elif "rok" in call.data:
            results[11] = "Корпоративные продажи"
        elif "int" in call.data:
            results[11] = "Интернет"
        elif "roz" in call.data:
            results[11] = "Розница"
        print(results)
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
            results[12] = "Канцелярия"
        elif "det" in call.data:
            results[12] = "Детские товары"
        elif "kni" in call.data:
            results[12] = "Книги"
        elif "sum" in call.data:
            results[12] = "Сумки"
        elif "suv" in call.data:
            results[12] = "Сувениры"
        print(results)
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        keyboard.add(types.InlineKeyboardButton(text="Да",
                                                callback_data="callback_m_offline_yes"),
                     types.InlineKeyboardButton(text="Нет",
                                                callback_data="callback_m_offline_no"),
                     )
        bot.send_message(call.message.chat.id, "Наличие оффлайн точек:", reply_markup=keyboard)


    elif call.data == "callback_m_offline_yes":
        results[13] = "Да"
        print(results)
        bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Укажите количество"), m_assort)


    elif call.data == "callback_m_offline_no":
        results[13] = "Нет"
        print(results)
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        keyboard.add(types.InlineKeyboardButton(text="Интересна вся продукция",
                                                callback_data="callback_m_assort_prod"),
                     types.InlineKeyboardButton(text="Офис",
                                                callback_data="callback_m_assort_ofi"),
                     types.InlineKeyboardButton(text="Пластик",
                                                callback_data="callback_m_assort_spa"),
                     types.InlineKeyboardButton(text="Бумажно-беловая",
                                                callback_data="callback_m_assort_bum"),
                     types.InlineKeyboardButton(text="Сумки-рюкзаки",
                                                callback_data="callback_m_assort_sum"),
                     types.InlineKeyboardButton(text="Творчество",
                                                callback_data="callback_m_assort_two")
                     )
        bot.send_message(call.message.chat.id, "Укажите интересующий ассортимент.", reply_markup=keyboard)


    elif "callback_m_assort" in call.data:
        if "prod" in call.data:
            results[15] = "Интересна вся продукция"
        elif "ofi" in call.data:
            results[15] = "Офис"
        elif "spa" in call.data:
            results[15] = "Пластик"
        elif "bum" in call.data:
            results[15] = "Бумажно-беловая"
        elif "sum" in call.data:
            results[15] = "Сумки-рюкзаки"
        elif "two" in call.data:
            results[15] = "Творчество"
        print(results)
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        keyboard.add(types.InlineKeyboardButton(text="Да",
                                                callback_data="callback_m_comment_yes"),
                     types.InlineKeyboardButton(text="Нет",
                                                callback_data="callback_m_comment_no"),
                     )
        bot.send_message(call.message.chat.id, "У вас есть комментарии по заполненной анкете?", reply_markup=keyboard)


    elif call.data == "callback_m_comment_no":
        results[16] = "Нет"
        print(results)
        add_message(user_id=results[18], data=results)
        bot.register_next_step_handler(
            bot.send_message(call.message.chat.id, ("Спасибо за заполнение анкеты, все данные сохранены! 🎉\n"
                                                    f"Универсальный номер анкеты: {random.randint(1,100000)},"
                                                    " по нему клиент может получить подарок.")), m_pass)
    elif call.data == "callback_m_comment_yes":
        results[16] = "Да"
        print(results)
        bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Укажите Ваш комментарий"), m_finish)


    ######################################################
    elif call.data == "callback_client":
        results[1] = call.data.strip("callback_")
        print(results)
        bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Ваше ФИО"), c_coop)


    elif call.data == "callback_c_coop_d":
        bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Уточните данные"), c_city)


    elif "callback_c_coop" in call.data:
        if "yes" in call.data:
            results[5] = "Да"
        elif "no" in call.data:
            results[5] = "Нет"
        elif "worked" in call.data:
            results[5] = "Работали ранее, но прекратили"
        print(results)
        bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Город Вашего офиса"), c_region)


    elif call.data == "callback_c_post_d":
        bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Уточните данные"), c_point)


    elif "callback_c_post" in call.data:
        print(call.data)
        if "dir" in call.data:
            results[10] = "Директор"
        elif "zak" in call.data:
            results[10] = "Специалист по закупкам"
        elif "sob" in call.data:
            results[10] = "Собственник"
        elif "opt" in call.data:
            results[10] = "Директор по оптовому каналу"
        elif "roz" in call.data:
            results[10] = "Директор по розничному каналу"
        print(results)
        bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Укажите название торговой точки"),
                                       c_direction)

    elif call.data == "callback_c_dir_d":
        bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Уточните данные"), c_field)


    elif "callback_c_dir" in call.data:
        print(call.data)
        if "opt" in call.data:
            results[11] = "Оптовая торговля"
        elif "rok" in call.data:
            results[11] = "Корпоративные продажи"
        elif "int" in call.data:
            results[11] = "Интернет"
        elif "roz" in call.data:
            results[11] = "Розница"
        print(results)
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
            results[12] = "Канцелярия"
        elif "det" in call.data:
            results[12] = "Детские товары"
        elif "kni" in call.data:
            results[12] = "Книги"
        elif "sum" in call.data:
            results[12] = "Сумки"
        elif "suv" in call.data:
            results[12] = "Сувениры"
        print(results)
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        keyboard.add(types.InlineKeyboardButton(text="Да",
                                                callback_data="callback_c_offline_yes"),
                     types.InlineKeyboardButton(text="Нет",
                                                callback_data="callback_c_offline_no"),
                     )
        bot.send_message(call.message.chat.id, "Наличие оффлайн точек:", reply_markup=keyboard)


    elif call.data == "callback_c_offline_yes":
        results[13] = "Да"
        print(results)
        bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Укажите количество"), c_assort)


    elif call.data == "callback_c_offline_no":
        results[13] = "Нет"
        print(results)
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        keyboard.add(types.InlineKeyboardButton(text="Интересна вся продукция",
                                                callback_data="callback_c_assort_prod"),
                     types.InlineKeyboardButton(text="Офис",
                                                callback_data="callback_c_assort_ofi"),
                     types.InlineKeyboardButton(text="Пластик",
                                                callback_data="callback_c_assort_spa"),
                     types.InlineKeyboardButton(text="Бумажно-беловая",
                                                callback_data="callback_c_assort_bum"),
                     types.InlineKeyboardButton(text="Сумки-рюкзаки",
                                                callback_data="callback_c_assort_sum"),
                     types.InlineKeyboardButton(text="Творчество",
                                                callback_data="callback_c_assort_two")
                     )
        bot.send_message(call.message.chat.id, "Укажите интересующий ассортимент.", reply_markup=keyboard)


    elif "callback_c_assort" in call.data:
        if "prod" in call.data:
            results[15] = "Интересна вся продукция"
        elif "ofi" in call.data:
            results[15] = "Офис"
        elif "spa" in call.data:
            results[15] = "Пластик"
        elif "bum" in call.data:
            results[15] = "Бумажно-беловая"
        elif "sum" in call.data:
            results[15] = "Сумки-рюкзаки"
        elif "two" in call.data:
            results[15] = "Творчество"
        print(results)
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        keyboard.add(types.InlineKeyboardButton(text="Да",
                                                callback_data="callback_c_comment_yes"),
                     types.InlineKeyboardButton(text="Нет",
                                                callback_data="callback_c_comment_no"),
                     )
        bot.send_message(call.message.chat.id, "У вас есть комментарии по заполненной анкете?", reply_markup=keyboard)


    elif call.data == "callback_c_comment_no":
        results[16] = "Нет"
        print(results)
        add_message(user_id=results[18], data=results)
        bot.register_next_step_handler(
            bot.send_message(call.message.chat.id, ("Спасибо за заполнение анкеты, все данные сохранены! 🎉\n"
                                                    f"Универсальный номер анкеты: {random.randint(1,100000)},"
                                                    " по нему клиент может получить подарок.")), c_pass)
    elif call.data == "callback_c_comment_yes":
        results[16] = "Да"
        print(results)
        bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Укажите Ваш комментарий"), c_finish)

        #############################


@bot.message_handler(content_types='text')
def m_m_fio(message):
    results[2] = message.text

    bot.register_next_step_handler(bot.send_message(message.chat.id, "Ваше ФИО"), m_fio)
    print(results)


@bot.message_handler(content_types='text')
def m_fio(message):
    results[3] = message.text

    bot.register_next_step_handler(bot.send_message(message.chat.id, "ФИО клиента"), m_coop)
    print(results)


def m_coop(message):
    results[4] = message.text
    print(results)
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text="Да",
                                            callback_data="callback_m_coop_yes"),
                 types.InlineKeyboardButton(text="Нет",
                                            callback_data="callback_m_coop_no"),
                 types.InlineKeyboardButton(text="Работали ранее, но прекратили",
                                            callback_data="callback_m_coop_worked"),
                 types.InlineKeyboardButton(text="Другое",
                                            callback_data="callback_m_coop_d")
                 )
    bot.send_message(message.chat.id, "Ранее было сотрудничество с «Офис Премьер»?", reply_markup=keyboard)



@bot.message_handler(content_types='text')
def m_city(message):
    results[5] = message.text
    bot.register_next_step_handler(bot.send_message(message.chat.id, "Город офиса клиента. Если несколько – введите через пробела"), m_region)
    print(results)



@bot.message_handler(content_types='text')
def m_region(message):
    results[6] = message.text
    bot.register_next_step_handler(bot.send_message(message.chat.id, "Регионы продаж клиента"), m_phone)
    print(results)



@bot.message_handler(content_types='text')
def m_phone(message):
    results[7] = message.text
    bot.register_next_step_handler(
        bot.send_message(message.chat.id, "Введите номер телефона клиента в международном формате (начинается с +)"),
        m_email)
    print(results)



@bot.message_handler(content_types='text')
def m_email(message):
    if re.findall(r'\+\d{10,13}$', message.text):
        results[8] = message.text
        bot.register_next_step_handler(bot.send_message(message.chat.id, "Введите e-mail клиента"), m_post)
        print(results)

    else:
        bot.register_next_step_handler(bot.send_message(message.chat.id,
                                                        "Кажется, Вы ошиблись. Номер телефона должен начинаться с + и включать в себя только цифры.\n"
                                                        "Перепроверьте правильность данных и введите номер снова, начиная с +."), m_email)



def m_post(message):
    if re.findall(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?", message.text):
        results[9] = message.text
        print(results)
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(types.InlineKeyboardButton(text="Директор",
                                                callback_data="callback_m_post_dir"),
                     types.InlineKeyboardButton(text="Специалист по закупкам",
                                                callback_data="callback_m_post_zak"),
                     types.InlineKeyboardButton(text="Собственник",
                                                callback_data="callback_m_post_sob"),
                     types.InlineKeyboardButton(text="Директор по оптовому каналу",
                                                callback_data="callback_m_post_opt"),
                     types.InlineKeyboardButton(text="Директор по розничному каналу",
                                                callback_data="callback_m_post_roz"),
                     types.InlineKeyboardButton(text="Другое",
                                                callback_data="callback_m_post_d")
                     )
        bot.send_message(message.chat.id, "Должность клиента. Если несколько, то дополните позже.",
                         reply_markup=keyboard)

    else:
        bot.register_next_step_handler(bot.send_message(message.chat.id, "Перепроверьте правильность данных и введите e-mail снова"), m_post)


@bot.message_handler(content_types='text')
def m_point(message):
    results[10] = message.text
    print(results)
    bot.register_next_step_handler(bot.send_message(message.chat.id, "Укажите название торговой точки"), m_direction)


def m_direction(message):
    results[11] = message.text
    print(results)
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
    results[11] = message.text
    print(results)
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
    results[12] = message.text
    print(results)
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(types.InlineKeyboardButton(text="Да",
                                            callback_data="callback_m_offline_yes"),
                 types.InlineKeyboardButton(text="Нет",
                                            callback_data="callback_m_offline_no"),
                 )
    bot.send_message(message.chat.id, "Наличие оффлайн точек:", reply_markup=keyboard)



def m_assort(message):
    results[14] = message.text
    print(results)
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(types.InlineKeyboardButton(text="Интересна вся продукция",
                                            callback_data="callback_m_assort_prod"),
                 types.InlineKeyboardButton(text="Офис",
                                            callback_data="callback_m_assort_ofi"),
                 types.InlineKeyboardButton(text="Пластик",
                                            callback_data="callback_m_assort_spa"),
                 types.InlineKeyboardButton(text="Бумажно-беловая",
                                            callback_data="callback_m_assort_bum"),
                 types.InlineKeyboardButton(text="Сумки-рюкзаки",
                                            callback_data="callback_m_assort_sum"),
                 types.InlineKeyboardButton(text="Творчество",
                                            callback_data="callback_m_assort_two")
                 )
    bot.send_message(message.chat.id, "Укажите интересующий ассортимент.", reply_markup=keyboard)



def m_finish(message):
    results[17] = message.text
    print(results)
    add_message(user_id=results[18], data=results)
    bot.send_message(message.chat.id, ("Спасибо за заполнение анкеты, все данные сохранены! 🎉\nУниверсальный номер "
                                       f"анкеты: {random.randint(1,100000)}, по нему клиент может получить "
                                       "подарок."))
    m_pass()


def m_pass():
    add_excel()


###############
def c_coop(message):
    results[4] = message.text
    print(results)
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text="Да",
                                            callback_data="callback_c_coop_yes"),
                 types.InlineKeyboardButton(text="Нет",
                                            callback_data="callback_c_coop_no"),
                 types.InlineKeyboardButton(text="Работали ранее, но прекратили",
                                            callback_data="callback_c_coop_worked"),
                 types.InlineKeyboardButton(text="Другое",
                                            callback_data="callback_c_coop_d")
                 )
    bot.send_message(message.chat.id, "Ранее было сотрудничество с «Офис Премьер»?", reply_markup=keyboard)



@bot.message_handler(content_types='text')
def c_city(message):
    results[5] = message.text
    bot.register_next_step_handler(bot.send_message(message.chat.id, "Город Вашего офиса"), c_region)
    print(results)



@bot.message_handler(content_types='text')
def c_region(message):
    results[6] = message.text
    bot.register_next_step_handler(bot.send_message(message.chat.id, "Регионы ваших продаж"), c_phone)
    print(results)



@bot.message_handler(content_types='text')
def c_phone(message):
    results[7] = message.text
    bot.register_next_step_handler(
        bot.send_message(message.chat.id, "Ваш номер телефона в международном формате (начинается с +)"), c_email)
    print(results)



@bot.message_handler(content_types='text')
def c_email(message):
    if re.findall(r'\+\d{10,13}$', message.text):
        results[8] = message.text
        bot.register_next_step_handler(bot.send_message(message.chat.id, "Ваш e-mail"), c_post)
        print(results)
    else:
        bot.register_next_step_handler(
            bot.send_message(message.chat.id, "Кажется, Вы ошиблись. Номер телефона должен начинаться с + и включать в себя только цифры.\n"
                                              "Перепроверьте правильность данных и введите номер снова, начиная с +."), c_email)



def c_post(message):
    if re.findall(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?", message.text):
        results[9] = message.text
        print(results)
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(types.InlineKeyboardButton(text="Директор",
                                                callback_data="callback_c_post_dir"),
                     types.InlineKeyboardButton(text="Специалист по закупкам",
                                                callback_data="callback_c_post_zak"),
                     types.InlineKeyboardButton(text="Собственник",
                                                callback_data="callback_c_post_sob"),
                     types.InlineKeyboardButton(text="Директор по оптовому каналу",
                                                callback_data="callback_c_post_opt"),
                     types.InlineKeyboardButton(text="Директор по розничному каналу",
                                                callback_data="callback_c_post_roz"),
                     types.InlineKeyboardButton(text="Другое",
                                                callback_data="callback_c_post_d")
                     )
        bot.send_message(message.chat.id, "Ваша должность. Если несколько, то дополните позже.",
                         reply_markup=keyboard)

    else:
        bot.register_next_step_handler(bot.send_message(message.chat.id, "Перепроверьте правильность данных и введите e-mail снова"), c_post)



@bot.message_handler(content_types='text')
def c_point(message):
    results[10] = message.text
    print(results)
    bot.register_next_step_handler(bot.send_message(message.chat.id, "Укажите название торговой точки"), c_direction)


def c_direction(message):
    results[11] = message.text
    print(results)
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
    results[11] = message.text
    print(results)
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
    results[12] = message.text
    print(results)
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(types.InlineKeyboardButton(text="Да",
                                            callback_data="callback_c_offline_yes"),
                 types.InlineKeyboardButton(text="Нет",
                                            callback_data="callback_c_offline_no"),
                 )
    bot.send_message(message.chat.id, "Наличие оффлайн точек:", reply_markup=keyboard)



def c_assort(message):
    results[14] = message.text
    print(results)
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(types.InlineKeyboardButton(text="Интересна вся продукция",
                                            callback_data="callback_c_assort_prod"),
                 types.InlineKeyboardButton(text="Офис",
                                            callback_data="callback_c_assort_ofi"),
                 types.InlineKeyboardButton(text="Пластик",
                                            callback_data="callback_c_assort_spa"),
                 types.InlineKeyboardButton(text="Бумажно-беловая",
                                            callback_data="callback_c_assort_bum"),
                 types.InlineKeyboardButton(text="Сумки-рюкзаки",
                                            callback_data="callback_c_assort_sum"),
                 types.InlineKeyboardButton(text="Творчество",
                                            callback_data="callback_c_assort_two")
                 )
    bot.send_message(message.chat.id, "Укажите интересующий ассортимент.", reply_markup=keyboard)



def c_finish(message):
    results[17] = message.text
    print(results)
    add_message(user_id=results[18], data=results)
    bot.send_message(message.chat.id, ("Спасибо за заполнение анкеты, все данные сохранены! 🎉\n"
                                       f"Ваш универсальный номер: {random.randint(1,100000)}.\n"
                                       "Покажите это сообщение нашему сотруднику для того, чтобы получить подарок."))
    c_pass()


def c_pass():
    add_message(user_id=results[18], data=results)
    add_excel()


###############

@bot.message_handler(commands=['button'])
def button_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Кнопка")
    item2 = types.KeyboardButton("Тык")
    markup.add(item1, item2)
    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)


@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text == "Кнопка":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Кнопка 2")
        markup.add(item1)
        bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)
    elif message.text == "Кнопка 2":
        bot.send_message(message.chat.id, 'Спасибо за прочтение статьи!')


def delete(call):
    bot.delete_message(call.message.chat.id, call.message.message_id, 1)


def delete_mess(message):
    bot.delete_message(message.chat.id, message.message_id, 1)
    bot.delete_message(message.chat.id, message.message_id - 1, 1)


bot.infinity_polling()
