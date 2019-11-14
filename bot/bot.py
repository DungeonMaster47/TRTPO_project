import json

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random
from bsuir.api import BSUIR
import datetime


class Bot:
    class UserInfo:
        INIT_STATE = 0
        GROUP_INPUT_STATE = 1
        EMPLOYEE_INPUT_STATE = 2
        NOTIFY_GROUP_INPUT_STATE = 3

        def __init__(self):
            self.state = self.INIT_STATE
            self.group = '0'
            self.notify = False

        def __str__(self):
            return self.__repr__()

        def __repr__(self):
            return f'{{"state": self.state, "group": self.group, "notify": self.notify}}'

    def __init__(self, token):
        self.token = token
        self.bsuir_api = BSUIR()
        self.keyboard = open("bot/KB.json", "r").read()
        try:
            with open('users.json', 'r') as file:
                try:
                    self.users = json.load(file)
                except Exception:
                    self.users = {}
        except FileNotFoundError:
            self.users = {}
        self.notify_time = datetime.datetime.now()

    def run(self):
        vk_session = vk_api.VkApi(token=self.token)
        vk_longpoll = VkLongPoll(vk_session, wait=25)
        vk = vk_session.get_api()
        while True:
            if (datetime.datetime.now() - self.notify_time).seconds / 60 >= 1:
                for user_id, user_info in self.users.items():
                    if user_info.notify:
                        schedule = self.bsuir_api.get_group_schedule(user_info.group)
                        now = datetime.datetime.now()
                        for lesson in schedule['todaySchedules']:

                            start_lesson_time = datetime.datetime(
                                minute=int(lesson['startLessonTime'].split(sep=':')[1]),
                                hour=int(lesson['startLessonTime'].split(sep=':')[0]),
                                second=0,
                                year=now.year,
                                month=now.month,
                                day=now.day
                            )
                            time_before_lesson = (start_lesson_time - now).seconds / 60
                            if 5 >= time_before_lesson > 0:
                                vk.messages.send(
                                    user_id=user_id,
                                    message='Скоро пара' + ' ' + lesson['lessonType'] + ' ' + lesson['subject'],
                                    random_id=random.getrandbits(64)
                                )
                                self.users[event.user_id].state = self.UserInfo.GROUP_INPUT_STATE
                self.notify_time = datetime.datetime.now()

            for event in vk_longpoll.check():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                    if event.from_user:
                        if self.users.get(event.user_id) is not None:
                            if self.users[event.user_id].state == self.UserInfo.INIT_STATE:
                                if event.text == 'Расписание группы':
                                    vk.messages.send(
                                        user_id=event.user_id,
                                        message='Введите номер группы',
                                        random_id=random.getrandbits(64)
                                    )
                                    self.users[event.user_id].state = self.UserInfo.GROUP_INPUT_STATE

                                elif event.text == 'Расписание преподавателя':
                                    vk.messages.send(
                                        user_id=event.user_id,
                                        message='Введите ФИО преподавателя в формате Фамилия Имя Отчество',
                                        random_id=random.getrandbits(64)
                                    )
                                    self.users[event.user_id].state = self.UserInfo.EMPLOYEE_INPUT_STATE

                                elif event.text == 'Список свободных аудиторий':
                                    vk.messages.send(
                                        user_id=event.user_id,
                                        message='Пожалуйста подождите, это может занять некоторое время',
                                        random_id=random.getrandbits(64),
                                    )
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
                                    self.users[event.user_id].state = self.UserInfo.NOTIFY_GROUP_INPUT_STATE

                                elif event.text == 'Выключить уведомления':
                                    vk.messages.send(
                                        user_id=event.user_id,
                                        message='Уведомления выключены',
                                        random_id=random.getrandbits(64),
                                        keyboard=self.keyboard
                                    )
                                    self.users[event.user_id].notify = False
                                    self.users[event.user_id].state = self.UserInfo.INIT_STATE

                                else:
                                    vk.messages.send(
                                        user_id=event.user_id,
                                        message='Ошибка',
                                        random_id=random.getrandbits(64),
                                        keyboard=self.keyboard
                                    )

                            elif self.users[event.user_id].state == self.UserInfo.GROUP_INPUT_STATE:
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message=self.bsuir_api.get_current_group_schedules(event.text),
                                    random_id=random.getrandbits(64),
                                    keyboard=self.keyboard
                                )
                                self.users[event.user_id].state = self.UserInfo.INIT_STATE

                            elif self.users[event.user_id].state == self.UserInfo.EMPLOYEE_INPUT_STATE:
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message=self.bsuir_api.get_current_employee_schedules(event.text),
                                    random_id=random.getrandbits(64),
                                    keyboard=self.keyboard
                                )
                                self.users[event.user_id].state = self.UserInfo.INIT_STATE

                            elif self.users[event.user_id].state == self.UserInfo.NOTIFY_GROUP_INPUT_STATE:
                                if self.bsuir_api.get_current_group_schedules(
                                        event.text) == 'Ошибка при получении расписания':
                                    vk.messages.send(
                                        user_id=event.user_id,
                                        message='Неверный номер группы',
                                        random_id=random.getrandbits(64),
                                        keyboard=self.keyboard
                                    )
                                    self.users[event.user_id].state = self.UserInfo.INIT_STATE

                                else:
                                    vk.messages.send(
                                        user_id=event.user_id,
                                        message='Уведомления включены',
                                        random_id=random.getrandbits(64),
                                        keyboard=self.keyboard
                                    )
                                    self.users[event.user_id].group = event.text
                                    self.users[event.user_id].notify = True
                                    self.users[event.user_id].state = self.UserInfo.INIT_STATE

                        else:
                            self.users[event.user_id] = self.UserInfo()
                            vk.messages.send(
                                user_id=event.user_id,
                                message='Здравствуйте',
                                random_id=random.getrandbits(64),
                                keyboard=self.keyboard
                            )
                            with open('users.json', 'w') as file:
                                try:
                                    json.dump(file, self.users)
                                except Exception:
                                    pass
