# -*- coding: utf-8 -*-
import datetime
from time import sleep
from bot.bot import Bot


if __name__ == '__main__':
    bot = Bot('154e00683e8ab940c179f50c4f04a4ebfd9da709bcdd355e002a88095aac0a80cf26312d1c016acf3697d')
    print(datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=3))))
    while True:
        try:
            bot.run()
        except Exception as e:
            print(f'"restoring connection", {datetime.datetime.now()}')
            sleep(5)


'''
bsuir_api = BSUIR()

print(bsuir_api.get_current_group_schedules(750505))
print(bsuir_api.get_current_group_schedules(1212121))

print(bsuir_api.get_current_employee_schedules('Искра Наталья Александровна'))
print(bsuir_api.get_current_employee_schedules('a'))
print(bsuir_api.get_current_employee_schedules('Романовский Егор Игоревичь'))
'''
