import urllib.request
import urllib.parse
import json


class BSUIR:
    def get_group_schedule(self, schedule):
        results = ''
        for lesson in schedule:
            fio = ''
            if len(lesson['employee']) > 0:
                fio = lesson['employee'][0]['fio']

            auditory = ''
            if len(lesson['auditory']) > 0:
                auditory = lesson['auditory'][0]

            result = lesson['lessonType'] + ' ' \
                     + lesson['subject'] + ' ' \
                     + fio + ' ' \
                     + lesson['startLessonTime'] + '-' \
                     + lesson['endLessonTime'] + ' ' \
                     + auditory

            results += result + '\n'

        return results

    def get_current_group_schedules(self, group):
        data = urllib.request.urlopen('https://journal.bsuir.by/api/v1/studentGroup/schedule?' + \
                                      urllib.parse.urlencode({'studentGroup': str(group)}))
        try:
            data = json.loads(data.read())
        except:
            return 'Ошибка при получении расписания'

        result = 'Расписание на сегодня \n' + \
                 self.get_group_schedule(data["todaySchedules"]) + '\n' + \
                 '\nРасписание на завтра' + '\n' + \
                 self.get_group_schedule(data["tomorrowSchedules"])
        return result

    def get_employee_schedule(self, schedule):
        results = ''
        for lesson in schedule:
            auditory = ''
            if len(lesson['auditory']) > 0:
                auditory = lesson['auditory'][0]
            groups = lesson['studentGroup'][0]
            if len(lesson['studentGroup']) > 1:
                groups = lesson['studentGroup'][0] + '-' + str(len(lesson['studentGroup']))
            result = lesson['lessonType'] + ' ' \
                     + lesson['subject'] + ' ' \
                     + groups + ' ' \
                     + lesson['startLessonTime'] + '-' \
                     + lesson['endLessonTime'] + ' ' \
                     + auditory

            results += result + '\n'

        return results

    def get_current_employee_schedules(self, name):
        name = name.split(sep=' ')
        if len(name) != 3:
            return 'Неверный формат имени'
        employees = urllib.request.urlopen('https://journal.bsuir.by/api/v1/employees')
        employees = json.loads(employees.read())
        employees = list(
            filter(lambda x: x['firstName'] == name[1] and x['lastName'] == name[0] and x['middleName'] == name[2],
                   employees))
        if (len(employees) == 0):
            return 'Преподаватель не найден'
        schedule = urllib.request.urlopen(
            'https://journal.bsuir.by/api/v1/portal/employeeSchedule?employeeId=' + str(employees[0]['id']))
        schedule = json.loads(schedule.read())
        result = 'Расписание на сегодня \n' + \
                 self.get_employee_schedule(schedule["todaySchedules"]) + '\n' + \
                 '\nРасписание на завтра' + '\n' + \
                 self.get_employee_schedule(schedule["tomorrowSchedules"])
        return result
