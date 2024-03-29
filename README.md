
# Требования к проекту

---

# Содержание
  [Глоссарий](#glossary)  
1 [Введение](#intro)  
2 [Требования пользователя](#user_requirements)  
2.1 [Программные интерфейсы](#program_interfaces)  
2.2 [Интерфейс пользователя](#user_interface)  
2.2.1 [Текст и графический интерфейс](#UI)   
2.3 [Характеристики пользователей](#user)  
2.4 [Зависимости](#dependencies)    
3 [Системные требования](#system_requirements)  
3.1 [Функциональные требования](#functional_requirements)  
3.2 [Нефункциональные требования](#non_functional_requirements)  
3.2.1 [Атрибуты качества](#quality_attributes)   
4 [Аналоги](#analogs)

<a name="glossary"/>

## Глоссарий
[VK](http://vk.com) — социальная сеть.

<a name="intro"/>

# 1 Введение

VK BSUIR schedule bot. В данное время существует множество приложений для получения расписания БГУИР, однако у всех отсутствует возможность получения списка свободных в данный момент аудиторий, данный бот будет способен это делать, также он будет обладать способностью предоставлять расписание групп и преподавателей.  

<a name="user_requirements"/>

# 2 Требования пользователя 

<a name="program_interfaces"/>

## 2.1 Программные интерфейсы
[VK api](https://pypi.org/project/vk-api/), [jsonlib](https://docs.python.org/3/library/json.html), [BSUIR api](https://iis.bsuir.by/login). Код будет написан на Python3. 

<a name="user_interface"/>

## 2.2 Интерфейс пользователя

<a name="UI"/>

### 2.2.1 Текст и графический интерфейс. 

Диалог с ботом.

![GitHub Logo](/Mockups/UI.jpg)

Предоставление расписания.

![GitHub Logo](/Mockups/Schedule.jpg)

Предоставление свободных аудиторий.

![GitHub Logo](/Mockups/Cabinets.jpg)

<a name="user"/>

## 2.3 Характеристики пользователей
Учащиеся и преподаватели БГУИР.

<a name="dependencies"/>

## 2.4 Зависимости
Для работы с ботом необходимо подключение к интернету, браузер, аккаунт ВКонтакте.

<a name="system_requirements"/>

# 3 Системные требования

<a name="functional_requirements"/>

## 3.1 Функциональные требования
1. Предоставление расписания группы по запросу пользователя.  
1.1 Номер группы указывается пользователем.  
2. Предоставление расписания преподавателя по запросу пользователя.  
2.1 ФИО преподавателя указывается пользователем.  
3. Предоставление списка свободных в данный момент аудиторий по запросу пользователя.  
4. Отправка уведомлений перед началом пары.  
4.1 Включение или выключение отправки уведомлений устанавливается пользователем.  

<a name="non_functional_requirements"/>

## 3.2 Нефункциональные требования

<a name="quality_attributes"/>

**3.2.1 Атрибуты качества**

1. Система обратной связи.  
2. Интуитивно понятный интерфейс.  
3. Актуальность информации.  
4. Полная доступность (при наличии интернет-соединения и аккаунта ВКонтакте).  

<a name="analogs"/>

# 4 Аналоги
1. [Расписание на сайте БГУИР](https://iis.bsuir.by/schedule) - расписание доступное онлайн через браузер, позволяет получить расписание групп и преподавателей.
2. Android приложение [Расписание БГУИР](https://play.google.com/store/apps/details?id=com.bakan.universchedule&hl=ru) - расписание доступное в виде Android приложения, предоставляет расписание групп и преподавателей, а также позволяет хранить несколько расписаний сразу.
