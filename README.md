
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

VK BSUIR schedule bot. Бот будет обладать возможностью предоставлять расписание групп и преподавателей, а также список свободных аудиторий.

<a name="user_requirements"/>

# 2 Требования пользователя 

<a name="program_interfaces"/>

## 2.1 Программные интерфейсы
[VK api](https://pypi.org/project/vk-api/), [jsonlib](https://docs.python.org/3/library/json.html). Код будет написан на Python3. 

<a name="user_interface"/>

## 2.2 Интерфейс пользователя

<a name="UI"/>

### 2.2.1 Текст и графический интерфейс. 

Диалог с ботом.

![GitHub Logo](/Mockups/UI.jpg)

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
Бот будет предоставлять:
1. Расписание групп.
2. Расписание преподавателей.
3. Список свободных аудиторий.

<a name="non_functional_requirements"/>

## 3.2 Нефункциональные требования

<a name="quality_attributes"/>

**3.2.1 Атрибуты качества**

Бот должен работать без сбоев логики и всегда быть доступным для предоставления информации.

<a name="analogs"/>

# 4 Аналоги
1. [Расписание на сайте БГУИР](https://iis.bsuir.by/schedule).
2. Android приложение [Расписание БГУИР](https://play.google.com/store/apps/details?id=com.bakan.universchedule&hl=ru).
