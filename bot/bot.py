import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random
from bsuir.api import BSUIR
import datetime


class Bot:
    def __init__(self, token):
        self.token = token
        self.bsuir_api = BSUIR()

    def run(self):
        vk_session = vk_api.VkApi(token=self.token)
        vk_longpoll = VkLongPoll(vk_session, wait=25)
        vk = vk_session.get_api()
        while True:
            for event in vk_longpoll.check():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                    if event.from_user:
                        vk.messages.send(
                            user_id=event.user_id,
                            message=self.bsuir_api.get_current_group_schedules(event.text.split(sep=' ')[0]),
                            random_id=random.getrandbits(64)
                        )
