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

# Клавиатура
def get_menu(one_time, label_1, label_2, label_3, label_4):
    keyboard = VkKeyboard(one_time=one_time)
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
        keyboard=get_menu(False, a1, a2, a3, a4),
    )

# Вывод задания для пользователя и чата
def task_handle(vk_event, enter_message, message, random_id, a1, a2, a3, a4):
    if vk_event.text == enter_message:
        if vk_event.from_user:
            return output_task(vk_event.user_id, None, message, random_id, a1, a2, a3, a4)
        elif vk_event.from_chat:
            return output_task(None, vk_event.chat_id, message, random_id, a1, a2, a3, a4)

# Вывод ответа бота для пользователя и чата
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

# Сообщения для пользователя и для чата в начале работы бота
print('Бот запущен')
Lsvk.messages.send(
        user_id=773548672,
        chat_id=None,
        message='"Игра" - войти в игру.',
        random_id=get_random_id(),
        )
Lsvk.messages.send(
        user_id=None,
        chat_id=1,
        message='"Игра" - войти в игру.',
        random_id=get_random_id(),
        )
Lsvk.messages.send(
        user_id=None,
        chat_id=2,
        message='"Игра" - войти в игру.',
        random_id=get_random_id(),
        )

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
    output_request('"Игра" - войти в игру.', None, None)

# Работа
for event in Lslongpoll.listen():
  if event.type == VkEventType.MESSAGE_NEW and event.to_me:
    if event.text == 'Игра':
     output_request(f"Я буду задавать вопросы, на которые будут 4 варианта ответа.\nВыберите правильный ответ.\nДля подсказки введите 'Подсказка'.", None, None)
     output_request(f"Всего будет 15 вопросов и 3 подсказки.\nПогнали!", None, None)
     right_answers_count = 0
     questions_count = 0
     initq = []
     initq = initq + Lists.questions
     inita = []
     inita = inita + Lists.answers
     questions = []
     answers = []
     for j in range(15):
      k = random.randrange(len(initq))
      questions.append(initq[k])
      answers.append(inita[k])
      del initq[k]
      del inita[k]
      j += 1
     del initq
     del inita
     num_questions = len(questions)
     hint = 3
     while True:
        if questions == []:
            del questions
            del answers
            del variants
            total(right_answers_count, num_questions, hint)
            break
        i = random.randrange(len(questions))
        variants = []
        variants = variants + answers[i]
        quest = questions[i]
        right = variants[0]
        del questions[i]
        del answers[i]
        random.shuffle(variants)
        questions_count += 1
        task_handle(event, event.text, f"Вопрос № {questions_count}:\n{quest}", get_random_id(), variants[0], variants[1], variants[2], variants[3])
        for event in Lslongpoll.listen():
         if event.type == VkEventType.MESSAGE_NEW and event.to_me:
          if event.text == right or event.text[32:] == right:
            output_request(random.choice(Lists.ans_right), None, None)
            right_answers_count += 1
            break
          elif event.text == 'Подсказка' or event.text[32:] == 'Подсказка':
            if hint > 0:
                hint -= 1
                hint_variants = []
                hint_variants = hint_variants + variants
                hint_variants.remove(right)
                random.shuffle(hint_variants)
                output_request(f"Неправильные ответы: {hint_variants[0]}, {hint_variants[1]}\nПодсказок осталось: {hint} ", None, None)
                del hint_variants
            else:
                output_request(f"Вы уже воспользовались подсказками!", None, None)
          elif event.text != right and event.text != 'Подсказка' or event.text[32:] != right and event.text[32:] != 'Подсказка':
            output_request(random.choice(Lists.ans_wrong), None, None)
            break
        if event.text == 'Завершить игру' or event.text[32:] == 'Завершить игру':
            break
