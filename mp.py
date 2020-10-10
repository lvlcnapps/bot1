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


class Event:
    def __init__(self, peer_id: int):
        self.peer_id = peer_id
        self.done = False
        pass

    def __call__(self, *args, **kwargs):
        pass

    def __bool__(self):
        return (not self.done) and True

    @staticmethod
    def try_parse(data, peer_id):
        return Event(peer_id)


def get_key():
    response = vk.method('groups.getLongPollServer', {'group_id': str_your_group_id})
    return response['key'], response['server'], response['ts']


def get_events(server, key, ts, events: list[Event]):
    response = rq.get(f'{server}?act=a_check&key={key}&ts={ts}&wait=25').json()
    if "updates" in response and "ts" in response:
        for update in response["updates"]:
            if update['type'] == 'message_new':
                new_message = update['object']['message']
                if 'peer_id' in new_message:
                    try:
                        peer_id = int(new_message['peer_id'])
                        text = str(new_message['text'])
                        for event_type in Events.EVENT_TYPES:
                            event = event_type.try_parse(text, peer_id)
                            if event:
                                events.append(event)
                    except Exception as e:
                        print(e)
        return events
    else:
        return events


def get_name_by_id(user_id):
    return vk.method('users.get', {'user_ids': user_id})[0]


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.randint(0, 1e10)})
    return


def write_msg_to_conversation(peer_id, message):
    vk.method('messages.send', {'peer_id': peer_id, 'message': message, 'group_id': your_group_id,
                                'random_id': random.randint(0, 10e10), 'v': '5.110'})


class EchoEvent(Event):
    def __init__(self, date: time.struct_time, response: str, peer_id: int):
        super().__init__(peer_id)
        self.date = date
        self.response = response

    def __call__(self, *args, **kwargs):
        self.done = True
        return f"Произошло событие: {' '.join(self.response)}\n"

    def __bool__(self):
        return time.localtime()[:5] == self.date[:5]

    @staticmethod
    def try_parse(data: str, peer_id: int):
        data = data.split()
        if "событие" in data[0].lower():
            try:
                date = time.strptime(' '.join(data[1:6]), "%H %M %d %m %Y")
            except Exception as e:
                print(e)
                return None
            response = data[6:]
            return EchoEvent(date, ' '.join(response), peer_id)
        else:
            return None


class TimeTableEvent(Event):
    DAY = {
        0: "Понедельник",
        1: "Вторник",
        2: "Среда",
        3: "Четверг",
        4: "Пятница",
        5: "Суббота",
        6: "Воскресенье"
    }
    timetable_path = "./timetable.json"

    def __init__(self, peer_id: int):
        super().__init__(peer_id)
        self.date = time.localtime()
        self.timetable = []
        self.load_timetable()

    def load_timetable(self):
        timetable = {}
        with open(TimeTableEvent.timetable_path, 'r') as data:
            timetable = json.load(data)
        timetable = timetable["timetable"][TimeTableEvent.DAY[self.date.tm_wday]]
        for lesson in timetable:
            data = lesson.split('\n')
            index = next(i for i, x in enumerate(data[0]) if '0' <= x <= '9')
            date = data[0][index:].split('-')
            self.timetable.append((
                time.strptime(date[0], "%H:%M"),  # start date
                time.strptime(date[1], "%H:%M"),  # end date
                data[1]  # description
            ))

    def __call__(self, *args, **kwargs):
        response = f"📋Расписание на сегодня ({TimeTableEvent.DAY[self.date.tm_wday]}):\n\n"
        for lesson in self.timetable:
            if self.date[3:5] > lesson[2]:
                response += f"⚾ {lesson[0]}\n\n"
            elif self.date[3:5] < lesson[1]:
                response += f"⏳ {lesson[0]}\n\n"
            else:
                response += f"🎾 {lesson[0]}\n\n"
        self.done = True
        return response

    @staticmethod
    def try_parse(data: str, peer_id: int):
        data = data.split()
        if "расп" in data[0].lower():
            return TimeTableEvent(peer_id)
        else:
            return None


class HelpEvent(Event):
    def __init__(self, peer_id: int):
        super().__init__(peer_id)
        pass

    def __call__(self, *args, **kwargs):
        self.done = True
        return '⚙️Функции бота:\n' \
               '1️⃣ Расп или расписание: Выводит расписание пар на сегодня/завтра\n' \
               '2️⃣ Событие: Создание события, синтаксис: "событие чч мм дд мм гггг текст события".\n' \
               'Пример: "событие 20 00 07 08 2021 лол" 7 августа 2021 в 20:00 бот напишет "лол"\n' \
               'Примечание: доступно только админам, работает в лс и в беседе\n' \
               '3️⃣ События: Выводит все события\n' \
               '4️⃣ Удалить [id]: Удаляет событие с номером id\n' \
               'Примечание: доступно только админам'

    @staticmethod
    def try_parse(data: str, peer_id: int):
        data = data.split()
        if "помощь" in data[0].lower():
            return HelpEvent(peer_id)
        else:
            return None


class DeleteEchoEvent(Event):
    def __init__(self, index: int, peer_id: int):
        super().__init__(peer_id)
        self.index = index

    def __call__(self, events: list[Event]):
        self.done = True
        index = 0
        for i, event in enumerate(events):
            if isinstance(event, EchoEvent):
                if index == self.index - 1:
                    events[i].done = True
                    break
                index += 1
        return None, events

    @staticmethod
    def try_parse(data: str, peer_id: int):
        data = data.split()
        if "удалить" in data[0].lower():
            try:
                index = int(data[1])
                return DeleteEchoEvent(index, peer_id)
            except Exception as e:
                print(e)
                return None
        else:
            return None


class ShowEchoEvent(Event):
    def __init__(self, peer_id):
        super().__init__(peer_id)

    def __call__(self, events: list[Event]):
        response = "Поихали:\n"
        index = 1
        for event in events:
            if isinstance(event, EchoEvent):
                response += f"{index}.{' '.join(event.response)}\n"
                index += 1
        self.done = True
        return response, events

    @staticmethod
    def try_parse(data: str, peer_id: int):
        data = data.split()
        if "события" in data[0].lower():
            return ShowEchoEvent(peer_id)
        else:
            return None


class ShowAdminsEvent(Event):
    ADMIN_LIST = [155921460, 187086379, 217950314]

    def __init__(self, peer_id: int):
        super().__init__(peer_id)

    def __call__(self):
        response = "Админы:\n"
        for admin in ShowAdminsEvent.ADMIN_LIST:
            name = get_name_by_id(admin)
            response += "{} {}\n".format(name["first_name"], name["last_name"])
        self.done = True
        return response

    @staticmethod
    def try_parse(data: str, peer_id: int):
        data = data.split()
        if "админы" in data[0].lower():
            return ShowAdminsEvent(peer_id)
        else:
            return None


class Events:
    EVENT_TYPES = (
        EchoEvent,
        ShowAdminsEvent,
        ShowEchoEvent,
        HelpEvent,
        TimeTableEvent,
        DeleteEchoEvent
    )

    def __init__(self):
        self.events = []
        self.key, self.server, self.ts = get_key()

    def append(self, event: Event):
        if not event.done:
            self.events.append(event)

    def update(self):
        self.events = [event for event in self.events if not event.done]
        self.events = get_events(self.server, self.key, self.ts, self.events)

    def __iter__(self):
        self.gen = iter(self.events)
        return self

    def __next__(self):
        return next(self.gen)


def main():
    events = Events()
    while True:
        for event in events:
            if event:
                if isinstance(event, (HelpEvent, EchoEvent, TimeTableEvent)):
                    write_msg_to_conversation(
                        event.peer_id,
                        event()
                    )
                elif isinstance(event, (DeleteEchoEvent, ShowEchoEvent)):
                    response, events = event(events.events)
                    if response:
                        write_msg_to_conversation(
                            event.peer_id,
                            response
                        )

        events.update()


if __name__ == "__main__":
    main()
