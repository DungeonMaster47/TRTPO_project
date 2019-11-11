from bsuir_api.bsuir_api import *

print(get_current_group_schedules(750505))
print(get_current_group_schedules(1212121))

print(get_current_employee_schedules('Искра Наталья Александровна'))
print(get_current_employee_schedules('a'))
print(get_current_employee_schedules('Романовский Егор Игоревичь'))
