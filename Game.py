import random, vk_api, secrets, threading  # copy, vk, bs4, requests, os
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll  # VkBotEventType
from vk_api.longpoll import VkLongPoll, VkEventType
from multiprocessing import Process
from threading import Thread
from lists import Lists
vk_session = vk_api.VkApi(token="vk1.a.CTTFMK9FAqi30OEbycat_ukNTOYp93w22GiV3CFaZodr6E1EWYTKN6nx7N-FZV1oDbm-1y9F20T1QD6oyXRiSKB9vsG9-Ui6jWde0DbwpsBMqXnzLtEyNAxdyAlSOm1hdVB0Ix5Mygxhh8my-nGW5dS063w3N60so2RJZPN43B6IJKPj6f0CpSe9e3uvE1iFVqzMaebofiB8OjrtaAJmHQ")
longpoll = VkBotLongPoll(vk_session, 224992987)
vk = vk_session.get_api()
Lslongpoll = VkLongPoll(vk_session)
Lsvk = vk_session.get_api()

def user_name(user_id):
    user = vk_session.method("users.get", {"user_ids": user_id})  # вместо 1 подставляете айди нужного юзера
    return user[0]['first_name'] #+ ' ' + user[0]['last_name'] # Нам нужно только имя

# Клавиатура основная
def get_menu(label_1, label_2, label_3, label_4):
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Подсказка', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Забрать деньги', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button(label_1, color=VkKeyboardColor.SECONDARY)
    keyboard.add_button(label_2, color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button(label_3, color=VkKeyboardColor.SECONDARY)
    keyboard.add_button(label_4, color=VkKeyboardColor.SECONDARY)
    return keyboard.get_keyboard()

# Клавиатура подсказок
def get_hints():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Убрать 2 неверных ответа', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Звонок другу', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Помощь зала', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Не использовать', color=VkKeyboardColor.NEGATIVE)
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
def total(hints_a, hints_b, hints_c):
    if hints_a == 1 and hints_b == 1 and hints_c == 1:
        output_request(random.choice(Lists.congratulations_100), None, None)
        output_request(None, random.choice(Lists.congrat_sticks_100), None)
    else:
        output_request(random.choice(Lists.congratulations_80_100), None, None)
        output_request(None, random.choice(Lists.congrat_sticks_80_100), None)
    output_request(Lists.all_farewells(user_name(event.user_id)), None, None)
    init_message(event.user_id)

print('Бот запущен')
init_message(773548672) # Выводим вступительное сообщение пользователю 773548672 (я) и в чаты сообщества (без клавы)
gamers = []

# Работа
def work(event):
     output_request(Lists.all_greatings(user_name(event.user_id)), None, None)    # Бот приветствует тебя!
     output_request(f"Я буду задавать вопросы, на которые будут 4 варианта ответа.\nВыберите правильный ответ.\n\nВсего будет 15 вопросов и 3 подсказки.\nПогнали!", None, None)  # Выводим вступительные сообщения (см. def output request)
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
     hint_a = 1                              # Количество подсказок за игру (3)
     hint_b = 1
     hint_c = 1
     sum = 0                               # Количество выигранных денег (до начала игры - 0)
     while True:                           # Игра началась (инициируем цикл игры)
        break_out_flag = False  # Если отвечаем неправильно, этот флаг становится True и происходит выход из цикла игры
        if is_empty(questions):            # Если закончились вопросы (список вопросов пуст - см. def is_empty()), то чистим за собой все оставшиеся списки и выводим итог (см. def total) и выходим из цикла игры
            answers = []
            del vars_to_out
            total(hint_a, hint_b, hint_c)                      # Выводим итог (см. def total)
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
            right_answers_count += 1                                      # Наращиваем счетчик правильных ответов на 1
            sum = Lists.points[right_answers_count]
            if sum == 5000:
                output_request(f"{random.choice(Lists.ans_right)}\nУ Вас первая несгораемая сумма в {sum} рублей.", None, None)
            elif sum == 100000:
                output_request(f"{random.choice(Lists.ans_right)}\nУ Вас вторая несгораемая сумма в {sum} рублей.", None, None)
            else:
                output_request(f"{random.choice(Lists.ans_right)}\nУ Вас {sum} рублей.", None, None)  # Выводим случайное одобрение (см. список ans_rigt в файле lists.py)
            break                                                         # Выходим из цикла ответа на вопрос
          elif event.text == 'Подсказка' or event.text[32:] == 'Подсказка':    # "Ботик, родненький, подскажи, пожалуйста!!!"
            output_request('Выберите подсказку:', None, get_hints())
            for event in Lslongpoll.listen():  # Инициируем цикл выбора подсказки
                if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                    if event.text == 'Убрать 2 неверных ответа' or event.text[32:] == 'Убрать 2 неверных ответа':
                        if hint_a > 0:                                                # "ОК, но у тебя {hint} попыток!"
                            hint_a -= 1                                               # Осталось {hint-1} попыток
                            hint_variants_a = []                                      # Инициируем/обнуляем список выводимых ответов, за исключением правильного
                            hint_variants_a = hint_variants_a + vars_to_out           # Записываем в него список всех выводимых ответов
                            hint_variants_a.remove(right)                               # Убираем из него правильный ответ
                            random.shuffle(hint_variants_a)                             # Затем его перемешаем
                            for i in range(4):
                                if vars_to_out[i] == hint_variants_a[0] or vars_to_out[i] == hint_variants_a[1]:
                                    vars_to_out[i] = '-'
                            output_request('Убраны 2 неверных ответа', None, get_menu(vars_to_out[0], vars_to_out[1], vars_to_out[2], vars_to_out[3]))  # "Держи 2 неверных ответа)))"
                            del hint_variants_a                                         # Прибираемся за собой
                            break
                        else:                                                         # "А попытки-то закончились!"
                            output_request('Вы уже воспользовались данной подсказкой!', None, get_menu(vars_to_out[0], vars_to_out[1], vars_to_out[2], vars_to_out[3]))   # "Хрен тебе, а не подсказка!))"
                            break
                    elif event.text == 'Звонок другу' or event.text[32:] == 'Звонок другу':
                        if hint_b > 0:
                            hint_b -= 1  # Осталось {hint-1} попыток
                            hint_variants_b = []  # Инициируем/обнуляем список выводимых ответов, за исключением правильного
                            hint_variants_b = hint_variants_b + vars_to_out  # Записываем в него список всех выводимых ответов
                            hint_variants_b.remove(right)  # Убираем из него правильный ответ
                            hint_variants_b.append(right)  # Добавляем правильный ответ в конец. Он будет hint_variants_b[3]
                            if '-' in hint_variants_b:     # Если была использована подсказка -2 ответа, просим выбирать друга из оставшихся ответов
                                hint_variants_b = list(set(hint_variants_b))
                                hint_variants_b.remove('-')
                                hint_variants_b.remove(right)
                                hint_variants_b.append(right)
                            if len(hint_variants_b) == 2:
                                friend = hint_variants_b[1] if random.random() < 0.75 else hint_variants_b[0]
                            else:
                                friend = hint_variants_b[3] if secrets.randbelow(100) < 75 else random.choice([hint_variants_b[0], hint_variants_b[1], hint_variants_b[2]])  # С вероятностью в 75% выпадет правильный ответ
                            output_request(f"Друг считает, что правильный ответ - {friend}", None, get_menu(vars_to_out[0], vars_to_out[1], vars_to_out[2], vars_to_out[3]))  # "Держи 2 неверных ответа)))"
                            del hint_variants_b  # Прибираемся за собой
                            del friend
                            break
                        else:  # "А попытки-то закончились!"
                            output_request('Вы уже воспользовались данной подсказкой!', None, get_menu(vars_to_out[0], vars_to_out[1], vars_to_out[2], vars_to_out[3]))  # "Хрен тебе, а не подсказка!))"
                            break
                    elif event.text == 'Помощь зала' or event.text[32:] == 'Помощь зала':
                        if hint_c > 0:
                            hint_c -= 1  # Осталось {hint-1} попыток
                            hint_variants_c = []
                            vars_to_out.remove(right)
                            random.shuffle(vars_to_out)
                            if secrets.randbelow(100) < 75:                                                      # C 75-процентной вероятностью правильный ответ будет на первом месте
                                if '-' in vars_to_out:
                                    vars_to_out = list(set(vars_to_out))
                                    vars_to_out.remove('-')
                                    vars_to_out.insert(0, right)
                                    vars_to_out.append('-')
                                    vars_to_out.append('-')
                                else:
                                    hint_variants_c = [right, vars_to_out[0], vars_to_out[1], vars_to_out[2]]
                                    vars_to_out = hint_variants_c
                            else:
                                vars_to_out.append(right)                                                        # Хотя еще накидывается 25% от оставшихся 25%
                                if '-' in vars_to_out:
                                    vars_to_out = list(set(vars_to_out))
                                    vars_to_out.remove('-')
                                    vars_to_out.remove(right)
                                    vars_to_out.insert(1, right)
                                    vars_to_out.append('-')
                                    vars_to_out.append('-')
                                else:
                                    random.shuffle(vars_to_out)
                            output_request('После голосования порядок ответов изменился (с большей долей вероятности правильный ответ - на первой кнопке)',None, get_menu(vars_to_out[0], vars_to_out[1], vars_to_out[2], vars_to_out[3]))  # "Держи 2 неверных ответа)))"
                            del hint_variants_c
                            break
                        else:  # "А попытки-то закончились!"
                            output_request('Вы уже воспользовались данной подсказкой!', None, get_menu(vars_to_out[0], vars_to_out[1], vars_to_out[2], vars_to_out[3]))  # "Хрен тебе, а не подсказка!))"
                            break
                    elif event.text == 'Не использовать' or event.text[32:] == 'Не использовать':
                        output_request('OK!', None, get_menu(vars_to_out[0], vars_to_out[1], vars_to_out[2], vars_to_out[3]))
                        break
          elif event.text == 'Забрать деньги' or event.text[32:] == 'Забрать деньги': # "Хочешь выйти из игры?"
            output_request(Lists.get_ans_commit(sum), None, VkKeyboard.get_empty_keyboard()) # Выводим сообщение о завершении игры и прячем клаву
            init_message(event.user_id)                                   # Выводим вступительное сообщение пользователю и в чаты (без клавы)
            break_out_flag = True
            break                                                         # Выходим из цикла ответа на вопрос
          elif event.text == '-' or event.text[32:] == '-':               # На убранный ответ не реагируем
              continue
          elif (event.text in [vars_to_out[0], vars_to_out[1], vars_to_out[2], vars_to_out[3]] and event.text != right) or (event.text[32:] in [vars_to_out[0], vars_to_out[1], vars_to_out[2], vars_to_out[3]] and event.text[32:] != right):
            sum = 0 if sum < 5000 else 5000 if 5000 <= sum < 100000 else 100000 if 100000 <= sum < 3000000 else 3000000    # Остается только та несгораемая сумма, до которой вы дошли
            output_request(f"{Lists.get_ans_wrong(right)}\nВы выиграли {sum} рублей.", None, None)    # "Осуждаю!"   (см. список осуждений ans_wrong из файла lists.py)
            init_message(event.user_id)
            break_out_flag = True
            break                                                         # Выходим из цикла ответа на вопрос
        if break_out_flag == True:  # "Хочешь выйти из игры? Ставим это же условие в цикле уровнем выше, чтобы..."
            del sum
            del hint_a
            del hint_b
            del hint_c
            del questions
            del answers
            del vars_to_out
            break                                                         # ...выйти и из него тоже, т.е. из цикла игры


for event in Lslongpoll.listen():          # Инициируем цикл работы бота
  if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
    if event.text == 'Игра':               # "Бот, давай поиграем!)"
     if event.user_id not in gamers:
         gamers.append(event.user_id)
         print(gamers)
         work(event)
     else:
         print(gamers)
         work(event)
         #continue