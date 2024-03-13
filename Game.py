import random, vk_api, copy, vk, bs4, requests, os
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
vk_session = vk_api.VkApi(token = "vk1.a.CTTFMK9FAqi30OEbycat_ukNTOYp93w22GiV3CFaZodr6E1EWYTKN6nx7N-FZV1oDbm-1y9F20T1QD6oyXRiSKB9vsG9-Ui6jWde0DbwpsBMqXnzLtEyNAxdyAlSOm1hdVB0Ix5Mygxhh8my-nGW5dS063w3N60so2RJZPN43B6IJKPj6f0CpSe9e3uvE1iFVqzMaebofiB8OjrtaAJmHQ")
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
longpoll = VkBotLongPoll(vk_session, 224992987)
vk = vk_session.get_api()
from vk_api.longpoll import VkLongPoll, VkEventType
Lslongpoll = VkLongPoll(vk_session)
Lsvk = vk_session.get_api()
from lists import Lists

# Клавиатура
def get_menu(label_1, label_2, label_3, label_4):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button(label_1, color=VkKeyboardColor.SECONDARY)
    keyboard.add_button(label_2, color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button(label_3, color=VkKeyboardColor.SECONDARY)
    keyboard.add_button(label_4, color=VkKeyboardColor.SECONDARY)
    return keyboard.get_keyboard()


# Вывод задания
def output_task(user_id, chat_id, message, random_id, a1,a2,a3,a4):
    Lsvk.messages.send(
        user_id=user_id,
        chat_id=chat_id,
        message=message,
        random_id=random_id,
        keyboard=get_menu(a1,a2,a3,a4),
    )

# Вывод задания для пользователя и чата
def task_handle(event, enter_message, message, random_id, a1,a2,a3,a4):
    if event.text == enter_message:
        if event.from_user:
            return output_task(event.user_id, None, message, random_id, a1,a2,a3,a4)
            #return output_message(event.user_id, None, message, random_id, keyboard)
        elif event.from_chat:
            return output_task(None, event.chat_id, message, random_id, a1,a2,a3,a4)
            #return output_message(None, event.chat_id, message, random_id, keyboard)

# Вывод ответа бота для пользователя и чата
def output_request(otvet):
    if event.from_user:
     Lsvk.messages.send(
        user_id=event.user_id,
        chat_id=None,
        message=otvet,
        random_id=get_random_id(),
        )
    if event.from_chat:
     Lsvk.messages.send(
        user_id=None,
        chat_id=event.chat_id,
        message=otvet,
        random_id=get_random_id(),
        )
# Сообщения для пользователя или для чата

print('Бот запущен')
Lsvk.messages.send(
        user_id=773548672,
        chat_id=None,
        message='"Игра" - войти в игру.\n"Завершить игру" - выйти из игры.',
        random_id=get_random_id(),
        )
Lsvk.messages.send(
        user_id=None,
        chat_id=1,
        message='"Игра" - войти в игру.\n"Завершить игру" - выйти из игры.',
        random_id=get_random_id(),
        )
Lsvk.messages.send(
        user_id=None,
        chat_id=2,
        message='"Игра" - войти в игру.\n"Завершить игру" - выйти из игры.',
        random_id=get_random_id(),
        )
def total(num_questions, num_right_questions):
    if num_right_questions == 1:
        output_request(f"Вы ответили на {num_right_questions} вопрос из {num_questions}")
    elif 2 <= num_right_questions <= 4:
        output_request(f"Вы ответили на {num_right_questions} вопроса из {num_questions}")
    else:
        output_request(f"Вы ответили на {num_right_questions} вопросов из {num_questions}")
    output_request('"Игра" - войти в игру.\n"Завершить игру" - выйти из игры.')

# Работа
for event in Lslongpoll.listen():
  if event.type == VkEventType.MESSAGE_NEW and event.to_me:
    if event.text == 'Игра':
     count = 0
     rights = 0
     questions = []
     questions = questions+Lists.questions
     answers = []
     answers = answers+Lists.answers
     ans = True
     while ans == True:
        if questions == []:
            output_request('Вопросы кончились')
            total(count, rights)
            break
        variants = []
        variants = variants+Lists.answers
        i = random.randrange(len(questions))
        quest = questions[i]
        right = answers[i]
        del questions[i]
        del answers[i]
        variants.remove(right)
        ans_to_out = [right]
        ans_to_out = ans_to_out+variants
        random.shuffle(ans_to_out)
        task_handle(event, event.text, quest, get_random_id(), ans_to_out[0],ans_to_out[1],ans_to_out[2],ans_to_out[3])
        for event in Lslongpoll.listen():
         if event.type == VkEventType.MESSAGE_NEW and event.to_me:
          if event.text == right or event.text[32:] == right:
            output_request('Правильно')
            count += 1
            rights += 1
            break
          elif event.text == 'Завершить игру' or event.text[32:] == 'Завершить игру':
            output_request('Игра завершена')
            total(count, rights)
            break
          elif event.text != right or event.text[32:] != right:
            output_request('Неправильно')
            count += 1
            break
        if event.text == 'Завершить игру' or event.text[32:] == 'Завершить игру':
            break







