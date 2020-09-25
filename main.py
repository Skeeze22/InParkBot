from vk_api.bot_longpoll import VkBotEventType
from _thread import start_new_thread
from config  import longpoll, vk, vk_session, get_random_id



def main():
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text =="Начать":
            print("hello world")




main()