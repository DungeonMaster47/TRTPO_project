import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random
from bsuir.api import BSUIR
import datetime


class Bot:
    class UserInfo:
        init_state = 0
        group_input_state = 1
        employee_input_state = 2
        notify_group_input_state = 3
        state = init_state
        group = '0'
        notify = False

    def __init__(self, token):
        self.token = token
        self.bsuir_api = BSUIR()
        self.keyboard = open("bot/KB.json", "r").read()
        self.users = dict()

    def run(self):
        vk_session = vk_api.VkApi(token=self.token)
        vk_longpoll = VkLongPoll(vk_session, wait=25)
        vk = vk_session.get_api()
        while True:
            for event in vk_longpoll.check():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                    if event.from_user:
                        if self.users.get(event.user_id) is not None:
                            if self.users[event.user_id].state == self.UserInfo.init_state:
                                if event.text == 'Расписание группы':
                                    vk.messages.send(
                                        user_id=event.user_id,
                                        message='Введите номер группы',
                                        random_id=random.getrandbits(64)
                                    )
                                    self.users[event.user_id].state = self.UserInfo.group_input_state

                                elif event.text == 'Расписание преподавателя':
                                    vk.messages.send(
                                        user_id=event.user_id,
                                        message='Введите ФИО преподавателя в формате Фамилия Имя Отчество',
                                        random_id=random.getrandbits(64)
                                    )
                                    self.users[event.user_id].state = self.UserInfo.employee_input_state

                                elif event.text == 'Список свободных аудиторий':
                                    vk.messages.send(
                                        user_id=event.user_id,
                                        message=self.bsuir_api.get_free_auditory_list(),
                                        random_id=random.getrandbits(64),
                                        keyboard=self.keyboard
                                    )

                                elif event.text == 'Включить уведомления':
                                    vk.messages.send(
                                        user_id=event.user_id,
                                        message='Введите номер группы',
                                        random_id=random.getrandbits(64)
                                    )
                                    self.users[event.user_id].state = self.UserInfo.notify_group_input_state

                                elif event.text == 'Выключить уведомления':
                                    vk.messages.send(
                                        user_id=event.user_id,
                                        message='Уведомления выключены',
                                        random_id=random.getrandbits(64),
                                        keyboard=self.keyboard
                                    )
                                    self.users[event.user_id].notify = False
                                    self.users[event.user_id].state = self.UserInfo.init_state

                                else:
                                    vk.messages.send(
                                        user_id=event.user_id,
                                        message='Ошибка',
                                        random_id=random.getrandbits(64),
                                        keyboard=self.keyboard
                                    )

                            elif self.users[event.user_id].state == self.UserInfo.group_input_state:
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message=self.bsuir_api.get_current_group_schedules(event.text),
                                    random_id=random.getrandbits(64),
                                    keyboard=self.keyboard
                                )
                                self.users[event.user_id].state = self.UserInfo.init_state

                            elif self.users[event.user_id].state == self.UserInfo.employee_input_state:
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message=self.bsuir_api.get_current_employee_schedules(event.text),
                                    random_id=random.getrandbits(64),
                                    keyboard=self.keyboard
                                )
                                self.users[event.user_id].state = self.UserInfo.init_state

                            elif self.users[event.user_id].state == self.UserInfo.notify_group_input_state:
                                if self.bsuir_api.get_current_group_schedules(event.text) == 'Ошибка при получении расписания':
                                    vk.messages.send(
                                        user_id=event.user_id,
                                        message='Неверный номер группы',
                                        random_id=random.getrandbits(64),
                                        keyboard=self.keyboard
                                    )
                                    self.users[event.user_id].state = self.UserInfo.init_state
                                    
                                else:
                                    vk.messages.send(
                                        user_id=event.user_id,
                                        message='Уведомления включены',
                                        random_id=random.getrandbits(64),
                                        keyboard=self.keyboard
                                    )
                                    self.users[event.user_id].group = event.text
                                    self.users[event.user_id].notify = True
                                    self.users[event.user_id].state = self.UserInfo.init_state

                        else:
                            self.users[event.user_id] = self.UserInfo()
                            vk.messages.send(
                                user_id=event.user_id,
                                message='Здравствуйте',
                                random_id=random.getrandbits(64),
                                keyboard=self.keyboard
                            )

