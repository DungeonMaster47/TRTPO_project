import urllib.request
import json


def get_schedule(schedule):
    results = ''
    for lesson in schedule:
        fio = ' '
        if len(lesson['employee']) > 0:
            fio = lesson['employee'][0]['fio']

        auditory = ' '
        if len(lesson['auditory']) > 0:
            auditory = lesson['auditory'][0]

        result = lesson['subject'] + ' ' \
                 + fio + ' ' \
                 + lesson['startLessonTime'] + '-' \
                 + lesson['endLessonTime'] + ' ' \
                 + auditory

        results += result + '\n'

    return results


def get_current_group_schedules(group):
    data = urllib.request.urlopen('https://journal.bsuir.by/api/v1/studentGroup/schedule?studentGroup=' + str(group))
    try:
        data = json.loads(data.read())
    except:
        return 'Ошибка при получении расписания'

    result = 'Расписание на сегодня \n' + \
             get_schedule(data["todaySchedules"]) + '\n' + \
             '\nРасписание на завтра' + '\n' + \
             get_schedule(data["tomorrowSchedules"])
    return result