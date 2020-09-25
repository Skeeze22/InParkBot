from config import longpoll, vk, vk_session, get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from Scenario import Scenario
from Words import Words
from models.DataFromUser import DataFromUser
from models.PhotoMessage import PhotoMessage
from DataClasses.RailsData import rails_list
from DataClasses.FoodData import  food_data

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
                self.check_rails(user_id , 0,food_data ,self.words.food, self.scenario.food)
                break
            if self.check_message(self.words.rides):
                self.check_rails(user_id, 0, rails_list, self.words.rails, self.scenario.rails_choise)
                break
            if self.check_message(self.words.apps):
                self.send_link(user_id)
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

    def check_message_loop(self, words):
        for i in range(0 , len(words)):
            if words[i] == str(self.data.text) and self.data.text != self.words.in_menu and self.data.text != self.words.back and self.data.text != self.words.next and self.data.user_id == self.data.bot_user_id:

                return True , i
        return False, 0

    def check_message(self, bot_message):
        return self.data.text != self.words.start and self.data.text == bot_message and self.data.user_id == self.data.bot_user_id and self.data.text != self.words.back

    def chech_info(self, user_id):
        photo = PhotoMessage(photo="-198989984_457239018",
                             description="Мы  крупнейший городской парк Липецка, основанный в 1805 году.")
        self.send_photo_message(self.get_start_keyboard(), photo=photo, user_id=user_id)
        self.menu(user_id)

    def push_system_button(self, message):
        return message == self.data.text and self.data.user_id == self.data.bot_user_id and self.words.start != self.data.text

    def get_rails_keyboard(self, start, words):
        keyboard = VkKeyboard(one_time=True)
        i = start
        while i < start + 5:
            if i < len(words):
                keyboard.add_button(words[i], color=VkKeyboardColor.POSITIVE)
                keyboard.add_line()
                i = i + 1
            else:
                break
        if start + 5 < len(words) and start - 5 >= 0:
            print(1)
            keyboard.add_button(self.words.back, color=VkKeyboardColor.POSITIVE)
            keyboard.add_button(self.words.next, color=VkKeyboardColor.POSITIVE)
            keyboard.add_line()
            keyboard.add_button(self.words.in_menu, color=VkKeyboardColor.POSITIVE)
        if start - 5 >= 0 and start + 5 >= len(words):
            print(2)
            keyboard.add_button(self.words.back, color=VkKeyboardColor.POSITIVE)
            keyboard.add_line()
            keyboard.add_button(self.words.in_menu, color=VkKeyboardColor.POSITIVE)
        if start + 5 < len(words) and start == 0:
            print(3)
            keyboard.add_button(self.words.next, color=VkKeyboardColor.POSITIVE)
            keyboard.add_line()
            keyboard.add_button(self.words.in_menu, color=VkKeyboardColor.POSITIVE)
        if start + 5 >= len(words) and start - 5 <= 0:
            keyboard.add_button(self.words.in_menu, color=VkKeyboardColor.POSITIVE)

        return keyboard.get_keyboard()


    def send_photo_message(self, keyboard, photo, user_id):
        vk.messages.send(message=photo.description, peer_id=user_id, random_id=get_random_id(), attachment=photo.photo,
                         keyboard=keyboard)

    def check_rails(self, user_id, index, data, words, mess):
        keyboard = self.get_rails_keyboard(index, words)
        vk.messages.send(message=mess, peer_id=user_id, random_id=get_random_id(),
                         keyboard=keyboard)
        for event in longpoll.listen():
            self.data.text = event.obj.text
            self.data.user_id = event.obj.from_id
            self.data.bot_user_id = user_id

            flag , i = self.check_message_loop(words)
            if flag == True:
                self.send_photo_message(self.get_rails_keyboard(index, words), data[i], user_id)
            if self.push_system_button(self.words.next):
                self.check_rails(user_id, index + 5, data,words, mess)
            if self.push_system_button(self.words.back):
                self.check_rails(user_id, index - 5, data,words, mess)
            if self.push_system_button(self.words.in_menu):
                self.menu(user_id)

    def send_link(self, user_id):
        vk.messages.send(message=self.scenario.apps, peer_id=user_id, random_id=get_random_id())
        self.menu(user_id)





