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
        self.users = self.__load_users()
        self.notify_time = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=3)))
        self.vk = None
        self.handlers = {self.UserInfo.INIT_STATE: self.__menu_handler,
                         self.UserInfo.GROUP_INPUT_STATE: self.__group_schedule_request_input,
                         self.UserInfo.EMPLOYEE_INPUT_STATE: self.__employee_schedule_request_input,
                         self.UserInfo.NOTIFY_GROUP_INPUT_STATE: self.__notify_on_request_input}
        self.menu_handlers = {'расписание группы': self.__group_schedule_request,
                              'расписание преподавателя': self.__employee_schedule_request,
                              'список свободных аудиторий': self.__free_auditory_list_request,
                              'включить уведомления': self.__notify_on_request,
                              'выключить уведомления': self.__notify_off_request}

    def __save_users(self):
        with open('users.json', 'w') as file:
            try:
                users = {}
                for user_id, user_info in self.users.items():
                    users[user_id] = {}
                    users[user_id]['group'] = user_info.group
                    users[user_id]['state'] = user_info.state
                    users[user_id]['notify'] = user_info.notify
                file.write(json.dumps(users))
            except Exception:
                pass

    def __load_users(self):
        users = {}
        try:
            with open('users.json', 'r') as file:
                users_file = json.loads(file.read())
                for user_id, user_info in users_file.items():
                    user_id = int(user_id)
                    users[user_id] = self.UserInfo()
                    users[user_id].group = user_info['group']
                    users[user_id].state = user_info['state']
                    users[user_id].notify = user_info['notify']
        except Exception:
            pass
        return users

    def __notify(self):
        if (datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=3))) - self.notify_time).seconds / 60 >= 3:
            for user_id, user_info in self.users.items():
                if user_info.notify:
                    schedule = self.bsuir_api.get_group_schedule(user_info.group)
                    now = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=3)))
                    for lesson in schedule['todaySchedules']:

                        start_lesson_time = datetime.datetime(
                            minute=int(lesson['startLessonTime'].split(sep=':')[1]),
                            hour=int(lesson['startLessonTime'].split(sep=':')[0]),
                            second=0,
                            year=now.year,
                            month=now.month,
                            day=now.day,
                            tzinfo=datetime.timezone(datetime.timedelta(hours=3))
                        )
                        time_before_lesson = (start_lesson_time - now).seconds / 60
                        if 5 >= time_before_lesson > 0:
                            self.vk.messages.send(
                                user_id=user_id,
                                message='Скоро пара' + ' ' + lesson['lessonType'] + ' ' + lesson['subject'],
                                random_id=random.getrandbits(64)
                            )
            self.notify_time = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=3)))

    def __event_handler(self, event: vk_api.longpoll.Event):
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text and event.from_user:
            if self.users.get(event.user_id) is None:
                self.__new_user_request(event)
            try:
                self.handlers[self.users[event.user_id].state](event)
            except Exception:
                self.__invalid_request(event)

    def __menu_handler(self, event: vk_api.longpoll.Event):
        self.menu_handlers[event.text.lower()](event)

    def __group_schedule_request(self, event: vk_api.longpoll.Event):
        self.vk.messages.send(
            user_id=event.user_id,
            message='Введите номер группы',
            random_id=random.getrandbits(64)
        )
        self.users[event.user_id].state = self.UserInfo.GROUP_INPUT_STATE
        self.__save_users()

    def __employee_schedule_request(self, event: vk_api.longpoll.Event):
        self.vk.messages.send(
            user_id=event.user_id,
            message='Введите ФИО преподавателя в формате Фамилия Имя Отчество',
            random_id=random.getrandbits(64)
        )
        self.users[event.user_id].state = self.UserInfo.EMPLOYEE_INPUT_STATE
        self.__save_users()

    def __free_auditory_list_request(self, event: vk_api.longpoll.Event):
        self.vk.messages.send(
            user_id=event.user_id,
            message='Пожалуйста подождите, это может занять некоторое время',
            random_id=random.getrandbits(64),
        )
        self.vk.messages.send(
            user_id=event.user_id,
            message=self.bsuir_api.get_free_auditory_list(),
            random_id=random.getrandbits(64),
            keyboard=self.keyboard
        )

    def __notify_on_request(self, event: vk_api.longpoll.Event):
        self.vk.messages.send(
            user_id=event.user_id,
            message='Введите номер группы',
            random_id=random.getrandbits(64)
        )
        self.users[event.user_id].state = self.UserInfo.NOTIFY_GROUP_INPUT_STATE
        self.__save_users()

    def __notify_off_request(self, event: vk_api.longpoll.Event):
        self.vk.messages.send(
            user_id=event.user_id,
            message='Уведомления выключены',
            random_id=random.getrandbits(64),
            keyboard=self.keyboard
        )
        self.users[event.user_id].notify = False
        self.users[event.user_id].state = self.UserInfo.INIT_STATE
        self.__save_users()

    def __invalid_request(self, event: vk_api.longpoll.Event):
        self.vk.messages.send(
            user_id=event.user_id,
            message='Ошибка',
            random_id=random.getrandbits(64),
            keyboard=self.keyboard
        )

    def __group_schedule_request_input(self, event: vk_api.longpoll.Event):
        self.vk.messages.send(
            user_id=event.user_id,
            message=self.bsuir_api.get_current_group_schedules(event.text),
            random_id=random.getrandbits(64),
            keyboard=self.keyboard
        )
        self.users[event.user_id].state = self.UserInfo.INIT_STATE
        self.__save_users()

    def __employee_schedule_request_input(self, event: vk_api.longpoll.Event):
        self.vk.messages.send(
            user_id=event.user_id,
            message=self.bsuir_api.get_current_employee_schedules(event.text),
            random_id=random.getrandbits(64),
            keyboard=self.keyboard
        )
        self.users[event.user_id].state = self.UserInfo.INIT_STATE
        self.__save_users()

    def __notify_on_request_input(self, event: vk_api.longpoll.Event):
        if self.bsuir_api.get_current_group_schedules(
                event.text) == 'Ошибка при получении расписания':
            self.vk.messages.send(
                user_id=event.user_id,
                message='Неверный номер группы',
                random_id=random.getrandbits(64),
                keyboard=self.keyboard
            )
            self.users[event.user_id].state = self.UserInfo.INIT_STATE
            self.__save_users()

        else:
            self.vk.messages.send(
                user_id=event.user_id,
                message='Уведомления включены',
                random_id=random.getrandbits(64),
                keyboard=self.keyboard
            )
            self.users[event.user_id].group = event.text
            self.users[event.user_id].notify = True
            self.users[event.user_id].state = self.UserInfo.INIT_STATE
            self.__save_users()

    def __new_user_request(self, event: vk_api.longpoll.Event):
        self.users[event.user_id] = self.UserInfo()
        self.vk.messages.send(
            user_id=event.user_id,
            message='Здравствуйте',
            random_id=random.getrandbits(64),
            keyboard=self.keyboard
        )
        self.__save_users()

    def run(self):
        vk_session = vk_api.VkApi(token=self.token)
        self.vk = vk_session.get_api()
        vk_longpoll = VkLongPoll(vk_session, wait=25)
        while True:
            self.__notify()
            for event in vk_longpoll.check():
                self.__event_handler(event)
