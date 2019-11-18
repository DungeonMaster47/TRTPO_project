import datetime
import urllib.request
import urllib.parse
import json
import re


class BSUIR:
    @staticmethod
    def get_group_schedule(group):
        data = urllib.request.urlopen(
            'https://journal.bsuir.by/api/v1/studentGroup/schedule?' +
            urllib.parse.urlencode({'studentGroup': str(group)}))
        try:
            data = json.loads(data.read())
        except Exception:
            return None
        return data

    @staticmethod
    def group_schedule_to_str(schedule):
        results = ''
        for lesson in schedule:
            fio = ''
            if len(lesson['employee']) > 0:
                fio = lesson['employee'][0]['fio']

            auditory = ''
            if len(lesson['auditory']) > 0:
                auditory = lesson['auditory'][0]

            result = lesson['lessonType'] + ' ' + lesson['subject'] + ' ' + fio + ' ' + lesson[
                'startLessonTime'] + '-' + \
                     lesson['endLessonTime'] + ' ' + auditory

            results += result + '\n'

        return results

    @classmethod
    def get_current_group_schedules(cls, group):
        data = urllib.request.urlopen('https://journal.bsuir.by/api/v1/studentGroup/schedule?' +
                                      urllib.parse.urlencode({'studentGroup': str(group)}))
        try:
            data = json.loads(data.read())
        except Exception:
            return 'Ошибка при получении расписания'

        result = 'Расписание на сегодня \n' + \
                 cls.group_schedule_to_str(data["todaySchedules"]) + '\n' + \
                 '\nРасписание на завтра' + '\n' + \
                 cls.group_schedule_to_str(data["tomorrowSchedules"])
        return result

    @staticmethod
    def employee_schedule_to_str(schedule):
        results = ''
        for lesson in schedule:
            auditory = ''
            if len(lesson['auditory']) > 0:
                auditory = lesson['auditory'][0]
            groups = lesson['studentGroup'][0]
            for group in lesson['studentGroup']:
                if int(group) < int(groups):
                    groups = group
            if len(lesson['studentGroup']) > 1:
                groups = groups + '-' + str(len(lesson['studentGroup']) - int(groups[-1:]) + 1)

            result = lesson['lessonType'] + ' ' + lesson['subject'] + ' ' + groups + ' ' + \
                     lesson['startLessonTime'] + '-' + lesson['endLessonTime'] + ' ' + auditory
            results += result + '\n'

        return results

    @classmethod
    def get_current_employee_schedules(cls, name: str):
        # name = name.split(sep=' ')
        # if len(name) != 3:
        #     return 'Неверный формат имени'
        employees = urllib.request.urlopen('https://journal.bsuir.by/api/v1/employees')
        employees = json.loads(employees.read())
        now = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=3)))
        employees = list(filter(lambda x: name.lower() in f'{x["lastName"]} {x["firstName"]} {x["middleName"]}'.lower(),
                                employees))

        print(datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=3))) - now)
        if len(employees) == 0:
            return 'Преподаватель не найден'
        schedule = urllib.request.urlopen(
            'https://journal.bsuir.by/api/v1/portal/employeeSchedule?employeeId=' + str(employees[0]['id']))
        schedule = json.loads(schedule.read())
        result = 'Расписание на сегодня \n' + \
                 cls.employee_schedule_to_str(schedule["todaySchedules"]) + '\n' + \
                 '\nРасписание на завтра' + '\n' + \
                 cls.employee_schedule_to_str(schedule["tomorrowSchedules"])
        return result

    @classmethod
    def get_free_auditory_list(cls):
        auditories = urllib.request.urlopen('https://journal.bsuir.by/api/v1/auditory')
        auditories = json.loads(auditories.read())
        auditories = list(map(lambda x: f'{x["name"]}-{x["buildingNumber"]["name"]}', auditories))
        auditories = list(filter(lambda x: re.match(r'\d{3}\S{,3}-\d', x) is not None, auditories))
        groups = urllib.request.urlopen('https://journal.bsuir.by/api/v1/groups')
        groups = json.loads(groups.read())
        groups = list(map(lambda x: x['name'], groups))
        now = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=3)))
        for group in groups:
            schedule = cls.get_group_schedule(group)
            if schedule is None:
                continue
            schedule = schedule["todaySchedules"]
            for lesson in schedule:
                start_time = datetime.datetime(hour=int(lesson["startLessonTime"].split(sep=':')[0]),
                                               minute=int(lesson["startLessonTime"].split(sep=':')[1]),
                                               second=0,
                                               day=now.day,
                                               month=now.month,
                                               year=now.year,
                                               )
                end_time = datetime.datetime(hour=int(lesson["endLessonTime"].split(sep=':')[0]),
                                             minute=int(lesson["endLessonTime"].split(sep=':')[1]),
                                             second=0,
                                             day=now.day,
                                             month=now.month,
                                             year=now.year,
                                             )
                if start_time <= now <= end_time:
                    if len(lesson["auditory"]) > 0:
                        auditories.remove(lesson["auditory"][0])
                    break
        auditories.sort()
        return auditories
