from bsuir.api import BSUIR
from bot.bot import Bot


bot = Bot('b6c76b3f6f6e89a3af32669501b94227035a989823e626963eda64ca13d39cfd8ae9c11b3c04ee1c03758')
bot.run()






bsuir_api = BSUIR()


print(bsuir_api.get_current_group_schedules(750505))
print(bsuir_api.get_current_group_schedules(1212121))

print(bsuir_api.get_current_employee_schedules('Искра Наталья Александровна'))
print(bsuir_api.get_current_employee_schedules('a'))
print(bsuir_api.get_current_employee_schedules('Романовский Егор Игоревичь'))
