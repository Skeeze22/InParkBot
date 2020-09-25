from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import vk_api
import random

token = "ef32513379e02d03e8bcca1b373382e5f9f69e83da889f9b61d54201aef3edf31ff4f5e060765ec2083e5"
vk_session = vk_api.VkApi(token = token)
longpoll = VkBotLongPoll(vk_session , "198989984")
vk = vk_session.get_api()

def get_random_id():
    return random.randint(0,1000000)