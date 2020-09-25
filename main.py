from vk_api.bot_longpoll import VkBotEventType
from _thread import start_new_thread
from config import longpoll, vk, vk_session, get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.bot_longpoll import VkBotEventType
from Words import Words
from userController import userController


def main():
    words = Words()
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == words.start:
            start_new_thread(userController, (event.obj.from_id,))






main()
