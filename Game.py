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
from random import shuffle
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


# Вывод сообщения
def output_message(user_id, chat_id, message, random_id, a1,a2,a3,a4):
    Lsvk.messages.send(
        user_id=user_id,
        chat_id=chat_id,
        message=message,
        random_id=random_id,
        keyboard=get_menu(a1,a2,a3,a4),
    )

# Вывод ответа
def output_request(user_id, chat_id, otvet):
     Lsvk.messages.send(
        user_id=user_id,
        chat_id=chat_id,
        message=otvet,
        random_id=get_random_id(),
        )
# Сообщения для пользователя или для чата
def message_handle(event, enter_message, message, random_id, a1,a2,a3,a4):
    if event.text == enter_message:
        if event.from_user:
            return output_message(event.user_id, None, message, random_id, a1,a2,a3,a4)
            #return output_message(event.user_id, None, message, random_id, keyboard)
        elif event.from_chat:
            return output_message(None, event.chat_id, message, random_id, a1,a2,a3,a4)
            #return output_message(None, event.chat_id, message, random_id, keyboard)

# Работа
for event in Lslongpoll.listen():
  if event.type == VkEventType.MESSAGE_NEW and event.to_me:
    if event.text == 'Игра':
     questions = []
     questions = questions+Lists.questions
     answers = []
     answers = answers+Lists.answers
     ans = True
     while ans == True:
        if questions == []:
            if event.from_user:
                output_request(event.user_id, None, 'Вопросы кончились')
                break
            if event.from_chat:
                output_request(None, event.chat_id, 'Вопросы кончились')
                break
        variants = []
        variants = variants+Lists.answers
        print(Lists.answers)
        i = random.randrange(len(questions))
        quest = questions[i]
        right = answers[i]
        del questions[i]
        del answers[i]
        variants.remove(right)
        ans_to_out = [right]
        ans_to_out = ans_to_out+variants
        shuffle(ans_to_out)
        message_handle(event, event.text, quest, get_random_id(), ans_to_out[0],ans_to_out[1],ans_to_out[2],ans_to_out[3])
        for event in Lslongpoll.listen():
         if event.type == VkEventType.MESSAGE_NEW and event.to_me:
          if event.text == right and event.from_user:
            output_request(event.user_id, None, 'Правильно')
            ans = True
            break
          elif event.text != right and event.from_user:
            output_request(event.user_id, None, 'Неправильно')
            ans = False
            break
          if event.text[32:] == right and event.from_chat:
            output_request(None, event.chat_id, 'Правильно')
            ans = True
            break
          elif event.text[32:] != right and event.from_chat:
            output_request(None, event.chat_id, 'Неправильно')
            ans = False
            break






