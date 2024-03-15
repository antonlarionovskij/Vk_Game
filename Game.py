import random, vk_api  # copy, vk, bs4, requests, os
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll  # VkBotEventType
from vk_api.longpoll import VkLongPoll, VkEventType
from lists import Lists
vk_session = vk_api.VkApi(token="vk1.a.CTTFMK9FAqi30OEbycat_ukNTOYp93w22GiV3CFaZodr6E1EWYTKN6nx7N-FZV1oDbm-1y9F20T1QD6oyXRiSKB9vsG9-Ui6jWde0DbwpsBMqXnzLtEyNAxdyAlSOm1hdVB0Ix5Mygxhh8my-nGW5dS063w3N60so2RJZPN43B6IJKPj6f0CpSe9e3uvE1iFVqzMaebofiB8OjrtaAJmHQ")
longpoll = VkBotLongPoll(vk_session, 224992987)
vk = vk_session.get_api()
Lslongpoll = VkLongPoll(vk_session)
Lsvk = vk_session.get_api()

def user_name(user_id):
    user = vk_session.method("users.get", {"user_ids": user_id})  # вместо 1 подставляете айди нужного юзера
    return user[0]['first_name'] + ' ' + user[0]['last_name']

# Клавиатура
def get_menu(label_1, label_2, label_3, label_4):
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Подсказка', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Завершить игру', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button(label_1, color=VkKeyboardColor.SECONDARY)
    keyboard.add_button(label_2, color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button(label_3, color=VkKeyboardColor.SECONDARY)
    keyboard.add_button(label_4, color=VkKeyboardColor.SECONDARY)
    return keyboard.get_keyboard()


# Вывод задания и вариантов ответа на кнопках
def output_task(user_id, chat_id, message, random_id, a1, a2, a3, a4):
    Lsvk.messages.send(
        user_id=user_id,
        chat_id=chat_id,
        message=message,
        random_id=random_id,
        keyboard=get_menu(a1, a2, a3, a4),
    )

# Вывод задания для пользователя и чата. Если пользователь не в беседе, задание не выводится.
def task_handle(vk_event, enter_message, message, random_id, a1, a2, a3, a4):
    if vk_event.text == enter_message:
        if vk_event.from_user:
            return output_task(vk_event.user_id, None, message, random_id, a1, a2, a3, a4)
        elif vk_event.from_chat:
            return output_task(None, vk_event.chat_id, message, random_id, a1, a2, a3, a4)

# Вывод ответа бота для пользователя и чата с возможностью использования стикера и клавиатуры. Если пользователь не в беседе, сообщение не выводится.
def output_request(otvet, sticker, keyboard):
    if event.from_user:
        Lsvk.messages.send(
         user_id=event.user_id,
         chat_id=None,
         message=otvet,
         sticker_id=sticker,
         random_id=get_random_id(),
         keyboard=keyboard
         )
    if event.from_chat:
        Lsvk.messages.send(
         user_id=None,
         chat_id=event.chat_id,
         message=otvet,
         sticker_id=sticker,
         random_id=get_random_id(),
         keyboard=keyboard
          )

# Сообщения для пользователя user_id и для чатов(уже зашиты) в начале работы бота без клавы
def init_message(user_id):
    Lsvk.messages.send(
        user_id=user_id,
        chat_id=None,
        message='"Игра" - войти в игру.',
        random_id=get_random_id(),
        keyboard=VkKeyboard.get_empty_keyboard(),
        )
    Lsvk.messages.send(
        user_id=None,
        chat_id=1,
        message='"Игра" - войти в игру.',
        random_id=get_random_id(),
        keyboard=VkKeyboard.get_empty_keyboard(),
        )
    Lsvk.messages.send(
        user_id=None,
        chat_id=2,
        message='"Игра" - войти в игру.',
        random_id=get_random_id(),
        keyboard=VkKeyboard.get_empty_keyboard(),
        )

# Проверяем, пустой ли список или все подсписки списка пустые
def is_empty(l):
    return all(is_empty(i) if isinstance(i, list) else False for i in l)

# Подведение итогов
def total(num_right_questions, enter_questions, hints):
    output_request(f"Вы ответили на {num_right_questions} вопросов из {enter_questions}\nПодсказок использовано: {3-hints}", None, VkKeyboard.get_empty_keyboard())
    if num_right_questions / enter_questions*100 == 100.0 and hints == 3:
        output_request(random.choice(Lists.congratulations_100), None, None)
        output_request(None, random.choice(Lists.congrat_sticks_100), None)
    elif (80.0 < num_right_questions / enter_questions * 100 <= 100 and hints < 3) or (80.0 < num_right_questions / enter_questions * 100 < 100 and hints <= 3):
        output_request(random.choice(Lists.congratulations_80_100), None, None)
        output_request(None, random.choice(Lists.congrat_sticks_80_100), None)
    elif 50.0 < num_right_questions / enter_questions * 100 <= 80:
        output_request(random.choice(Lists.congratulations_50_80), None, None)
    elif 25.0 < num_right_questions / enter_questions * 100 <= 50:
        output_request(random.choice(Lists.congratulations_25_50), None, None)
    elif 0.0 <= num_right_questions / enter_questions * 100 <= 25:
        output_request(random.choice(Lists.congratulations_0_25), None, None)
    init_message(event.user_id)

print('Бот запущен')
init_message(773548672) # Выводим вступительное сообщение пользователю 773548672 (я) и в чаты сообщества (без клавы)

# Работа
for event in Lslongpoll.listen():          # Инициируем цикл работы бота
  if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
    if event.text == 'Игра':               # "Бот, давай поиграем!)"
     output_request(Lists.all_greatings(user_name(event.user_id)), None, None)    # Бот приветствует тебя!
     output_request(f"Я буду задавать вопросы, на которые будут 4 варианта ответа.\nВыберите правильный ответ.", None, None)  # Выводим вступительные сообщения (см. def output request)
     output_request(f"Всего будет 15 вопросов и 3 подсказки.\nПогнали!", None, None)
     right_answers_count = 0               # Счетчик правильных ответов
     questions_count = 0                   # Счетчик заданных вопросов (используется в выводе "Вопрос №_")
     initq = []                            # Инициируем/обнуляем общий список вопросов
     initq = initq + Lists.questions       # Подгружаем общий список вопросов (см. список questions в файле lists.py)
     inita = []                            # Инициируем/обнуляем общий список вариантов ответов
     inita = inita + Lists.answers         # Подгружаем список общий вариантов ответов(см. список answers в файле lists.py)
     questions = []                        # Инициируем/обнуляем список из n вопросов (см. цикл for j in range(n))
     answers = []                          # Инициируем/обнуляем список из n вариантов ответов (см. цикл for j in range(n))
     for j in range(15):                   # Всего вопросов - 15
      k = random.randrange(len(initq))     # В цикле: по случайному индексу k из общих списков вопросов и вариантов ответов выбираем случайные n штук (в общих списках вопросы соответствуют вариантам ответов), выбранное соответствие удаляется для избежания повторов
      questions.append(initq[k])
      answers.append(inita[k])
      del initq[k]
      del inita[k]
      j += 1
     del initq                             # Удаляем общий список вопросов без выбранных в игру
     del inita                             # Удаляем общий список вариантов ответов без выбранных в игру
     num_questions = len(questions)        # Количество вопросов в игре
     hint = 3                              # Количество подсказок за игру (3)
     while True:                           # Игра началась (инициируем цикл игры)
        if is_empty(questions):            # Если закончились вопросы (список вопросов пуст - см. def is_empty()), то чистим за собой все оставшиеся списки и выводим итог (см. def total) и выходим из цикла игры
            del questions
            del answers
            del vars_to_out
            total(right_answers_count, num_questions, hint)   # Выводим итог (см. def total)
            break
        i = random.randrange(len(questions)) # Случайным образом выбираем номер соответствия (вопрос-варианты ответа) из 15 вопросов-вариантов ответов
        variants = []                        # Инициируем/обнуляем список ответов по номеру выбранного соответствия
        variants = variants + answers[i]     # Подгружаем подсписок ответов по номеру выбранного соответствия
        quest = questions[i]                 # Из списка из 15 вопросов выбираем вопрос по номеру выбранного соответствия
        right = variants[0]                  # Правильный ответ всегда первый в подсписках ответов общего и игрового списков вариантов ответов. Записываем его в переменную
        del questions[i]                     # Убираем выбранный вопрос соответствия
        del answers[i]                       # Убираем выбранный подсписок ответов соответствия
        del variants[0]                      # Убираем правильный ответ из подгруженного подсписка ответов соответствия
        vars_to_out = [right]                # Инициируем список выводимых вариантов ответов и записываем в него правильный ответ
        for other_vars in range(3):          # Дописываем в список выводимых вариантов ответов еще 3 ответа из подгруженного подсписка ответов соответствия (правилный ответ оттуда уже убран)
            new_var = random.choice(variants)
            vars_to_out.append(new_var)
            variants.remove(new_var)         # Каждый добавленный ответ убираем из подсписка для избежания повторов
            other_vars += 1
        del variants                         # Удаляем подгруженный подсписок
        random.shuffle(vars_to_out)          # Перемешиваем список выводимых ответов
        questions_count += 1                 # Наращиваем счетчик заданных вопросов на 1
        task_handle(event, event.text, f"Вопрос № {questions_count}:\n{quest}", get_random_id(), vars_to_out[0], vars_to_out[1], vars_to_out[2], vars_to_out[3]) # Выводим вопрос с номером счетчика заданных вопросов и соответствующий ему список выводимых ответов (см. def task_handle)
        for event in Lslongpoll.listen():                                 # Инициируем цикл ответа на вопрос
         if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
          if event.text == right or event.text[32:] == right:             # Отвечаем верно (также чистим наш ответ от служебной информации - для чатов)
            output_request(random.choice(Lists.ans_right), None, None)    # Выводим случайное одобрение (см. список ans_rigt в файле lists.py)
            right_answers_count += 1                                      # Наращиваем счетчик правильных ответов на 1
            break                                                         # Выходим из цикла ответа на вопрос
          elif event.text == 'Подсказка' or event.text[32:] == 'Подсказка':    # "Ботик, родненький, подскажи, пожалуйста!!!"
            if hint > 0:                                                  # "ОК, но у тебя {hint} попыток!"
                hint -= 1                                                 # Осталось {hint-1} попыток
                hint_variants = []                                        # Инициируем/обнуляем список выводимых ответов, за исключением правильного
                hint_variants = hint_variants + vars_to_out               # Записываем в него список всех выводимых ответов
                hint_variants.remove(right)                               # Убираем из него правильный ответ
                random.shuffle(hint_variants)                             # Затем его перемешаем
                output_request(f"Неправильные ответы: {hint_variants[0]}, {hint_variants[1]}\nПодсказок осталось: {hint} ", None, None)  # "Держи 2 неверных ответа)))"
                del hint_variants                                         # Прибираемся за собой
            else:                                                         # "А попытки-то закончились!"
                output_request(f"Вы уже воспользовались подсказками!", None, None)   # "Хрен тебе, а не подсказка!))"
          elif event.text == 'Завершить игру' or event.text[32:] == 'Завершить игру': # "Хочешь выйти из игры?"
            del questions                                                 # Немного прибираемся
            del answers
            del vars_to_out
            output_request('Не хотите продолжать? Ну что ж, хозяин-барин.\nА с вами был Экзаменатор! До новых встреч!', None, VkKeyboard.get_empty_keyboard()) # Выводим сообщение о завершении игры и прячем клаву
            init_message(event.user_id)                                   # Выводим вступительное сообщение пользователю и в чаты (без клавы)
            break                                                         # Выходим из цикла ответа на вопрос
          elif event.text not in [str(right), 'Подсказка', 'Завершить игру'] or event.text[32:] not in [str(right), 'Подсказка', 'Завершить игру']: # Сморозил что-то невнятное (сюда же входит и неверный ответ, но не входит запрос подсказки или просьба о завершении игры)
            output_request(random.choice(Lists.ans_wrong), None, None)    # "Осуждаю!"   (см. список осуждений ans_wrong из файла lists.py)
            break                                                         # Выходим из цикла ответа на вопрос
        if event.text == 'Завершить игру' or event.text[32:] == 'Завершить игру':  # "Хочешь выйти из игры? Ставим это же условие в цикле уровнем выше, чтобы..."
            break                                                         # ...выйти и из него тоже, т.е. из цикла игры
