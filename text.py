# HELLO = ("*Добро пожаловать в умную анкету ErichKrause,*\n"
#          "*Благодарим Вас за желание о сотрудничестве! *\n\n"
#          "Пожалуйста, заполните данные и перепроверьте ответы перед отправкой анкеты. \n"
#          "В случае ошибки нажмите «Исправить» там, где это доступно. \n"
#          "Если данные не могут быть предоставлены, вводите в поле ввода прочерк. \n"
#          "Инструкция по корректному заполнению анкеты: (тут будет ссылка)\n\n"
#          "В конце опроса Вас ожидает подарок :)\n"
#          "Будем рады видеть Вас среди наших клиентов! ")

HELLO = ("*Добро пожаловать в умную анкету ErichKrause,*\n"
         "*Благодарим Вас за интерес к нашей продукции!*\n\n"

         "Пожалуйста, заполните данные и перепроверьте ответы перед отправкой анкеты.\n"
         "В случае ошибки Вы можете исправить ответ там, где это доступно.\n"
         "Если Вы не можете предоставить данные, вводите в поле ввода прочерк.\n"
         "Инструкция по заполнению анкеты: /help \n\n"

         "В конце опроса Вас ожидает подарок :) \n"
         "Будем рады видеть Вас среди наших клиентов! ")

HELP = ("Инструкция по использованию анкеты\n\n"
        "*1. Отправляйте ответ один раз.* \n\n"
        "Если ответ можно ввести вручную – отправляйте одно сообщение. \n"
        "Если ответ выбирается нажатием на кнопку – нажимайте на кнопку один раз.\n"
        "Отправка нескольких ответов подряд может привести к некорректной работе бота.\n"
        )

HELP2 = (
    "*2. Экстренно начать ввод анкеты заново.*\n\n"
    "Начать проходить анкету заново можно командой /start. \n"
    "Использовать данную команду без крайней необходимости (например, ошибка в работе бота) не рекомендуется.\n"
    "Команда активна только в том случае, если Вы остановились на вопросе, где ответ можно выбрать кнопкой. \n"
    "Если Вы остановились на вопросе, где нужно ввести текст вручную – дойдите до вопроса, где ответ выбирается кнопкой. Можете указывать в поле ввода прочерки, либо любую информацию, чтобы в базе данных было ясно, что анкета недействительна.\n"

    "\n*3. Запуск анкеты после полного прохождения.*\n\n"
    "Для того чтобы начать заполнение новой анкеты после полного прохождения предыдущей (Вы получили уникальный номер анкеты для получения подарка), один раз введите /start.\n"
    "Если Вы убедились, что сообщение отправлено (две галочки возле сообщения) и в течение 15-ти секунд ничего не произошло, введите /start снова.\n"
)

HELP3 = (
    "*4. Ошибки в работе бота.*\n\n"
    "Если бот начал задавать вопросы, которые Вы уже получали в ходе прохождения этой анкеты, первым делом убедитесь, что вопрос действительно такой же. Некоторые вопросы могут быть визуально схожи (например, «Ваше ФИО» и «ФИО клиента»).\n"
    "Ошибкой в работе может также являться отправка нескольких одинаковых сообщений от бота подряд.\n"
    "\n*В случае возникновения такой ошибки – введите /start. *\n\n"

    "Вы можете отправить скриншот с некорректной работой бота в whats’app или telegram по номеру +79151050228. Не забудьте указать, какой путь прохождения используется – «менеджер» или «клиент».\n"

    "\n*5. Ввод номера телефона.*\n\n"
    "Номер телефона вводится *слитно*, используются *только цифры* и знак *плюс в начале* номера.\n"
    "В конце сообщения точку ставить не нужно. \n"
    "Например, +79151234567 или +74951234567\n"
)

HELP4 = (
    "*6. Ввод электронного адреса (e-mail).*\n\n"
    "Адрес электронной почты вводится только с наличием символов «.» и «@». \n"
    "В конце сообщения точку ставить не нужно. \n"
    "Например, example@postmail.ru\n"

    "\n*7. Использование нескольких вариантов ответа.*\n\n"
    "Некоторые вопросы подразумевают ввод нескольких вариантов ответа по желанию клиента или менеджера.\n"

    "\n*7.1 Выбор должности клиента.*\n\n"
    "При выборе нескольких должностей клиента выбирайте по одной должности в каждом появляющемся сообщении с таким выбором. \n"
    "Например, если необходимо указать «Директор» и «Собственник», нажмите сначала на Выбор №1 (напр. Директор). В появившемся сообщении Выбор №1 (напр. Директор) будет отсутствовать, и Вы можете совершить Выбор №2 (напр. Собственник).\n"
    "\n*Для того, чтобы перейти к следующему вопросу, нажмите «Далее».*\n"
)

HELP5 = (
    "*7.2 Другие вопросы с несколькими вариантами ответа.*\n\n"
    "Для Вашего удобства, в некоторых вопросах предлагается указать интересующий выбор, отправив в чат через пробел необходимые цифровые значения. \n"

    "\nНапример:\n\n"
    '_Укажите направление деятельности. Если несколько — нажмите "Интересует несколько_"\n\n'

    "При нажатии на соответствующий вариант ответа, будет выведено сообщение:\n"
    "\n_Введите через пробел номер интересующего Вас направления деятельности:_\n\n"
    "_1. Оптовая торговля\n_"
    "_2. Корпоративные продажи\n_"
    "_3. Интернет\n_"
    "_4. Розница\n\n_"

    "Отправьте в поле ввода текста интересующие Вас номера. Например, интересует Оптовая торговля и Розница. В таком случае в чат следует отправить такое сообщение: 1 4\n"
)

HELP6 = (

    "*8. Фамилия Имя Отчество.*\n\n"
    "ФИО должно содержать минимум два слова, не иметь цифр и спец. Символов\n\n"

    "*9. Подтверждение правильности ввода e-mail и номера телефона.*\n\n"
    "После ввода номера телефона и e-mail, бот попросит Вас подтвердить правильность ввода. Перепроверьте введенные данные и отправьте в чат текстом «Да» (в случае, если всё указано верно) или «Нет» (в случае, если в номере/e-mail совершена ошибка). \n"
    "В случае ответа «Нет», Вам будет предложено ввести данные еще раз.\n"

    "\n*10. Комментарий по заполнению анкеты.*\n\n"
    "Последним вопросом Вам предлагается ввести комментарий по анкете. Если Вы ошиблись при ответе на какой-либо вопрос, то укажите в комментарий о своей ошибке. Оператор анкеты исправит данные вручную.\n"
)

HELP7 = (
    "*11. Интернет соединение.*\n\n"
    "Часто сообщения с ответами не отправляются сразу из-за нестабильного интернет соединения.Чтобы убедиться, что ответ отправлен, убедитесь, что в отправленном сообщении стоит «две галочки».В случае, если в сообщении стоят «часы» – подождите, пока не появятся «галочки».\n"
    "\nЕсли ответ был отправлен нажатием на кнопку, подождите, пока не появится новое сообщение от бота.Оно может задержаться из-за плохого интернет соединения.\n"

    "\n*12. Выбор – менеджер или клиент.*\n\n"
    "Если Вы являетесь сотрудником АО Офис Премьер или ErichKrause, то выбирайте «Менеджер».Если Вы действующий или потенциальный клиент – выбирайте «Клиент».\n"
    "\n*Напоминаем, что Вы можете сообщить о некорректной работе данного бота. \nОтправьте в whats’app или telegram по номеру +79151050228 скриншоты с ошибкой в работе. Не забудьте указать, какой путь прохождения используется – «менеджер» или «клиент».*\n"
    "\nЖелаем Вам приятного использования! :)\n")

DIRECTION = ['Оптовая торговля', 'Корпоративные продажи', 'Интернет', 'Розница']
FIELD = ['Канцелярия', 'Детские товары', 'Книги', 'Сумки', 'Сувениры']
ASSORT = ['Офис', 'Пластик', 'Бумажно-беловая', 'Сумки-рюкзаки', 'Творчество']
