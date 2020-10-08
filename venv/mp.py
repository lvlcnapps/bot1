# -*- coding: utf-8 -*-

import vk_api
import requests as rq
import time
import random
import json


token = ''

your_group_id = 198823110
str_your_group_id = '198823110'

vk = vk_api.VkApi(token=token)


def get_key():
    response = vk.method('groups.getLongPollServer', {'group_id': str_your_group_id})
    print(response)
    return response['key'], response['server'], response['ts']


def get_events():
    response = rq.get(f'{server}?act=a_check&key={key}&ts={ts}&wait=25').json()
    if 'ts' in response:
        return response, response['ts']
    else:
        print(response)
    return answer, -1

def get_name_1(user_id):
    return vk.method('users.get', {'user_ids': user_id})[0]

def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.randint(0, 1e10)})
    return


def write_msg_to_conversation(peer_id, message):
    vk.method('messages.send', {'peer_id': peer_id, 'message': message, 'group_id': your_group_id,
                                'random_id': random.randint(0, 10e10), 'v': '5.110'})

def write_msg_to_conversation_keyboard(peer_id, lab, message):
    kk = json.dumps(tab0_constr(lab))
    vk.method('messages.send', {'peer_id': peer_id, 'message': message, 'group_id': your_group_id,
                                'random_id': random.randint(0, 10e10), 'keyboard': kk, 'v': '5.110'})

def write_msg_to_conversation_keyboard_nh(peer_id, lab, message):
    kk = json.dumps(tab1_constr(lab))
    vk.method('messages.send', {'peer_id': peer_id, 'message': message, 'group_id': your_group_id,
                                'random_id': random.randint(0, 10e10), 'keyboard': kk, 'v': '5.110'})

monday_r_1 = "📋Расписание на сегодня (Понедельник):\n\n🇬🇧 8:30-10:05\nИн. язык(с) Каф"
monday_r_2 = "\n\n📐 10:15-11:50\nЛинал(с) 739л"
monday_r_3 = "\n\n📐 12:00-13:35\nЛинал(с) 908л"
monday_r_4 = "\n\n📝 13:50-15-25\nМатанализ(с) 908л"

tuesday_r_1 = "📋Расписание на сегодня (Вторник):\n\n📝 8:30-10:05\nМатанализ(с) 1035л"
tuesday_r_2 = "\n\n💁\u200d♂️ 10:15-11:50\nСоциология(с) 619л"
tuesday_r_3 = "\n\n😏 12:00-13:35\nОкно"
tuesday_r_4 = "\n\n🏃 13:50-15:25\nФизра(л) Каф"

wednesday_r_1 = "📋Расписание на сегодня (Среда):\n\n💻 13:50-15:25\nИнформатика(лб)330аю"
wednesday_r_2 = "\n\n📐 15:40-17:15\nЛинал(л) 228л"
wednesday_r_3 = "\n\n📐 17:25-19:00\nЛинал(л) 708л"

thursday_r = "📋Расписание на сегодня (Четверг):\n😏 Весь день балдеем"

friday_r_1 = "📋Расписание на сегодня (Пятница):\n\n🏃 14:05-15:35\nФизра(л) Каф"
friday_r_2 = "\n\n📝 15:40-17:15\nМатанализ(л) 228л"
friday_r_3 = "\n\n📝 17:25-19:00\nМатанализ(л) 228л"

saturday_r_1 = "📋Расписание на сегодня (Суббота):\n\n💻 13:50-15:25\nИнформатика(л) 501ю"
saturday_r_2 = "\n\n📟 15:40-17:15\nАлгоритмы(л) 501ю"

sunday_r = "📋Расписание на сегодня (Воскресенье):\n😏 Весь день балдеем"

adm12 = [155921460, 187086379, 217950314] #админы, то есть те, кто может создавать / удалять события

evs = [] #события

key, server, ts = get_key()
print(key, ts)
while True:
    p = 0
    for i in evs: #проверяем по списку событий, пришло ли время орать
        mes = time.strftime("%H %M %d %m %Y").split()
        aa = []
        try:
            for u in mes:
                aa.append(int(u))
        except BaseException:
            print("взлом жопы 2")
        txx = "Произошло событие, Текст:\n"
        for u in i[5:]:
            txx += u + " "
        if i[:5] == aa:
            evs = evs[1:]
            write_msg_to_conversation(155921460, txx) #вместо 155921460 - peer_id (> 2000000000) беседы, куда орать о событии
    answer, ts = get_events()
    if (ts == -1):
        key, server, ts = get_key()
        continue
    if 'updates' in answer:
        updates = answer['updates']
        for update in updates:
            print(update)
            if update['type'] == 'message_new':
                message = update['object']['message']
                if 'peer_id' in message:
                    peer_id = message['peer_id']
                    text = str(message['text'])
                    if text.lower() == "админы":
                        admlist = "Админы:"
                        for i in adm12:
                            name = get_name_1(i)
                            admlist += "\n" + name["first_name"] + " " + name["last_name"]
                        write_msg_to_conversation(peer_id, admlist)

                    if text.lower() == "помощь":
                        helplist = '⚙️Функции бота:\n1️⃣ Расп или расписание: Выводит расписание пар на сегодня/завтра\n2️⃣ Событие: Создание события, синтаксис: "событие чч мм дд мм гггг текст события".\nПример: "событие 20 00 07 08 2021 лол" 7 августа 2021 в 20:00 бот напишет "лол"\nПримечание: доступно только админам, работает в лс и в беседе\n3️⃣ События: Выводит все события\n4️⃣ Удалить [id]: Удаляет событие с номером id\nПримечание: доступно только админам'
                        write_msg_to_conversation(peer_id, helplist)

                    if (text.startswith("событие ") or text.startswith("Событие ")) and (update['object']['message']['from_id'] in adm12):
                        mes = text.split()
                        aa = []
                        try:
                            for i in mes[1:6]:
                                aa.append(int(i))
                            for i in mes[6:]:
                                aa.append(i)
                        except BaseException:
                            print("взлом жопы")
                        evs.append(aa)

                    if text.lower() == "события":
                        anss = "Поихали:"
                        for i in evs:
                            try:
                                tx = ""
                                for u in i[5:]:
                                    tx += u + " "
                                hour1 = str(i[0])
                                min1 = str(i[1])
                                if 0 < i[0] < 10:
                                    hour1 = "0" + str(i[0])
                                if i[0] == 0:
                                    hour1 = "00"
                                if 0 < i[1] < 10:
                                    min1 = "0" + str(i[1])
                                if i[1] == 0:
                                    min1 = "00"
                                anss += ("\n" + hour1 + ":" + min1 + " " + str(i[2]) + "." + str(i[3]) + "." + str(i[4]) + " " + tx)
                            except BaseException:
                                print("взлом жопы 3")
                        write_msg_to_conversation(peer_id, anss)


                    if text.startswith("удалить ") and (update['object']['message']['from_id'] in adm12):
                        k = text.split()
                        try:
                            evs.pop(int(k[1]) - 1)
                        except BaseException:
                            print("взлом жопы 4")

                    if text.lower() == "расписание" or text.lower() == "расп": # лучше бы этот говнец сделать парсингом страницы с расписанием
                        if time.strftime("%A") == "Monday":
                            nt = int(time.strftime("%H")) * 60 + int(time.strftime("%M"))
                            if (nt < 510):
                                m = monday_r_1 + "⏳" + monday_r_2 + "⏳" + monday_r_3 + "⏳" + monday_r_4 + "⏳"
                            if (510 <= nt < 605):
                                m = monday_r_1 + "🎾" + monday_r_2 + "⏳" + monday_r_3 + "⏳" + monday_r_4 + "⏳"
                            if (605 <= nt < 615):
                                m = monday_r_1 + "⚾" + monday_r_2 + "⏳" + monday_r_3 + "⏳" + monday_r_4 + "⏳"
                            if (615 <= nt < 710):
                                m = monday_r_1 + "⚾" + monday_r_2 + "🎾" + monday_r_3 + "⏳" + monday_r_4 + "⏳"
                            if (710 <= nt < 720):
                                m = monday_r_1 + "⚾" + monday_r_2 + "⚾" + monday_r_3 + "⏳" + monday_r_4 + "⏳"
                            if (720 <= nt < 815):
                                m = monday_r_1 + "⚾" + monday_r_2 + "⚾" + monday_r_3 + "🎾" + monday_r_4 + "⏳"
                            if (815 <= nt < 830):
                                m = monday_r_1 + "⚾" + monday_r_2 + "⚾" + monday_r_3 + "⚾" + monday_r_4 + "⏳"
                            if (830 <= nt < 925):
                                m = monday_r_1 + "⚾" + monday_r_2 + "⚾" + monday_r_3 + "⚾" + monday_r_4 + "🎾"
                            if (925 <= nt):
                                m = tuesday_r_1 + "⏳" + tuesday_r_2 + "⏳" + tuesday_r_3 + "⏳" + tuesday_r_4 + "⏳"
                            write_msg_to_conversation(peer_id, m)
                        if time.strftime("%A") == "Tuesday":
                            nt = int(time.strftime("%H")) * 60 + int(time.strftime("%M"))
                            if (nt < 510):
                                m = tuesday_r_1 + "⏳" + tuesday_r_2 + "⏳" + tuesday_r_3 + "⏳" + tuesday_r_4 + "⏳"
                            if (510 <= nt < 605):
                                m = tuesday_r_1 + "🎾" + tuesday_r_2 + "⏳" + tuesday_r_3 + "⏳" + tuesday_r_4 + "⏳"
                            if (605 <= nt < 615):
                                m = tuesday_r_1 + "⚾" + tuesday_r_2 + "⏳" + tuesday_r_3 + "⏳" + tuesday_r_4 + "⏳"
                            if (615 <= nt < 710):
                                m = tuesday_r_1 + "⚾" + tuesday_r_2 + "🎾" + tuesday_r_3 + "⏳" + tuesday_r_4 + "⏳"
                            if (710 <= nt < 720):
                                m = tuesday_r_1 + "⚾" + tuesday_r_2 + "⚾" + tuesday_r_3 + "⏳" + tuesday_r_4 + "⏳"
                            if (720 <= nt < 815):
                                m = tuesday_r_1 + "⚾" + tuesday_r_2 + "⚾" + tuesday_r_3 + "🎾" + tuesday_r_4 + "⏳"
                            if (815 <= nt < 830):
                                m = tuesday_r_1 + "⚾" + tuesday_r_2 + "⚾" + tuesday_r_3 + "⚾" + tuesday_r_4 + "⏳"
                            if (830 <= nt < 925):
                                m = tuesday_r_1 + "⚾" + tuesday_r_2 + "⚾" + tuesday_r_3 + "⚾" + tuesday_r_4 + "🎾"
                            if (925 <= nt):
                                m = wednesday_r_1 + "⏳" + wednesday_r_2 + "⏳" + wednesday_r_3 + "⏳"
                            write_msg_to_conversation(peer_id, m)
                        if time.strftime("%A") == "Wednesday":
                            nt = int(time.strftime("%H")) * 60 + int(time.strftime("%M"))
                            if (830 > nt):
                                m = wednesday_r_1 + "⏳" + wednesday_r_2 + "⏳" + wednesday_r_3 + "⏳"
                            if (830 <= nt < 925):
                                m = wednesday_r_1 + "🎾" + wednesday_r_2 + "⏳" + wednesday_r_3 + "⏳"
                            if (925 <= nt < 940):
                                m = wednesday_r_1 + "⚾" + wednesday_r_2 + "⏳" + wednesday_r_3 + "⏳"
                            if (940 <= nt < 1035):
                                m = wednesday_r_1 + "⚾" + wednesday_r_2 + "🎾" + wednesday_r_3 + "⏳"
                            if (1035 <= nt < 1045):
                                m = wednesday_r_1 + "⚾" + wednesday_r_2 + "⚾" + wednesday_r_3 + "⏳"
                            if (1045 <= nt < 1140):
                                m = wednesday_r_1 + "⚾" + wednesday_r_2 + "⚾" + wednesday_r_3 + "🎾"
                            if (1140 <= nt):
                                m = wednesday_r_1 + "⚾" + wednesday_r_2 + "⚾" + wednesday_r_3 + "⚾"
                            write_msg_to_conversation(peer_id, m)
                        if time.strftime("%A") == "Thursday":
                            write_msg_to_conversation(peer_id, friday_r_1 + "⏳" + friday_r_2 + "⏳" + friday_r_3 + "⏳")
                        if time.strftime("%A") == "Friday":
                            nt = int(time.strftime("%H")) * 60 + int(time.strftime("%M"))
                            if (nt < 845):
                                m = friday_r_1 + "⏳" + friday_r_2 + "⏳" + friday_r_3 + "⏳"
                            if (845 <= nt < 935):
                                m = friday_r_1 + "🎾" + friday_r_2 + "⏳" + friday_r_3 + "⏳"
                            if (935 <= nt < 940):
                                m = friday_r_1 + "⚾" + friday_r_2 + "⏳" + friday_r_3 + "⏳"
                            if (940 <= nt < 1035):
                                m = friday_r_1 + "⚾" + friday_r_2 + "🎾" + friday_r_3 + "⏳"
                            if (1035 <= nt < 1045):
                                m = friday_r_1 + "⚾" + friday_r_2 + "⚾" + friday_r_3 + "⏳"
                            if (1045 <= nt < 1140):
                                m = friday_r_1 + "⚾" + friday_r_2 + "⚾" + friday_r_3 + "🎾"
                            if (1140 <= nt):
                                m = saturday_r_1 + "⏳" + saturday_r_2 + "⏳"
                            write_msg_to_conversation(peer_id, m)
                        if time.strftime("%A") == "Saturday":
                            nt = int(time.strftime("%H")) * 60 + int(time.strftime("%M"))
                            if (nt < 830):
                                m = saturday_r_1 + "⏳" + saturday_r_2 + "⏳"
                            if (830 <= nt < 925):
                                m = saturday_r_1 + "🎾" + saturday_r_2 + "⏳"
                            if (925 <= nt < 940):
                                m = saturday_r_1 + '⚾' + saturday_r_2 + "⏳"
                            if (940 <= nt < 1035):
                                m = saturday_r_1 + '⚾' + saturday_r_2 + "🎾"
                            if (1035 <= nt):
                                m = saturday_r_1 + '⚾' + saturday_r_2 + "⚾"
                            write_msg_to_conversation(peer_id, m)
                        if time.strftime("%A") == "Sunday":
                            write_msg_to_conversation(peer_id, monday_r_1 + "⏳" + monday_r_2 + "⏳" + monday_r_3 + "⏳" + monday_r_4 + "⏳")