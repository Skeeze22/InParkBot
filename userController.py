from config import longpoll, vk, vk_session, get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from Scenario import Scenario
from Words import Words
from models.DataFromUser import DataFromUser
from models.PhotoMessage import PhotoMessage


class userController():

    def __init__(self, user_id):
        self.data = DataFromUser()
        self.scenario = Scenario()
        self.words = Words()
        self.menu(user_id)

    def menu(self, user_id):
        vk.messages.send(message=self.scenario.hello_message,
                         peer_id=user_id,
                         random_id=get_random_id(),
                         keyboard=self.get_start_keyboard())
        for event in longpoll.listen():
            self.data.user_id = event.obj.from_id
            self.data.text = event.obj.text
            self.data.bot_user_id = user_id
            if self.check_message(self.words.park_ifro):
                self.chech_info(user_id)
                break
            if self.check_message(self.words.events):
                pass
                break
            if self.check_message(self.words.kafe):
                pass
                break
            if self.check_message(self.words.rides):
                pass
                break
            if self.check_message(self.words.apps):
                pass
                break

    def get_start_keyboard(self):
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button(self.words.park_ifro, color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button(self.words.events, color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button(self.words.kafe, color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button(self.words.rides, color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button(self.words.apps, color=VkKeyboardColor.POSITIVE)
        return keyboard.get_keyboard()

    def check_message(self, bot_message):
        return self.data.text != self.words.start and self.data.text == bot_message and self.data.user_id == self.data.bot_user_id and self.data.text != self.words.back

    def chech_info(self, user_id):
        photo = PhotoMessage(photo="-198989984_457239018",
                             description="Мы  крупнейший городской парк Липецка, основанный в 1805 году.")
        self.send_photo_message(self.get_start_keyboard(), photo=photo, user_id=user_id)
        self.menu(user_id)

    def send_photo_message(self, keyboard, photo, user_id):
        vk.messages.send(message=photo.description, peer_id=user_id, random_id=get_random_id(), attachment=photo.photo,
                         keyboard=keyboard)
