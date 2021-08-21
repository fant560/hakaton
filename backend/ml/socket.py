# Встроенные импорты.
import datetime
import json
import random
import uuid
import time
from dateutil import parser

# Импорты сторонних библиотек.
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from .models import Document


class DocumentSocketListener(AsyncJsonWebsocketConsumer):

    async def connect(self):
        print('Соединение установлено')
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        document = await self.save()
        await self.send(text_data=json.dumps({
            "id": document.id,
            "title": document.title,
            "state": document.state,
            "date_of_creation": await self.get_date_string(parser.parse(document.date_of_creation))
        }))

    async def get_date_string(self, date):
        day = date.day
        if day < 10:
            day = '0' + str(day)
        else:
            day = str(day)
        month = date.month
        if month < 10:
            month = '0' + str(month)
        else:
            month = str(month)
        return day + '.' + month + '.' + str(date.year)

    async def disconnect(self, code):
        print('Соединение закрыто')

    @database_sync_to_async
    def save(self):
        return Document.objects.create(uuid=str(uuid.uuid4()),
                                       audio_record_id=None,
                                       date_of_recording=datetime.datetime.now(),
                                       date_of_creation=self.random_date("7/21/2021 1:30 PM", "8/21/2021 1:30 PM",
                                                                         random.random()),
                                       state='Обработано',
                                       storage_link='/home/user/test',
                                       title=self.get_random_title())

    @staticmethod
    def get_random_title():
        titles = ['Стенограмма заседания МГУ по вопросам финансирования региональных отделений',
                  'Встреча собственников многоквартирного дома в Кудрово',
                  'Запись защиты докторской дисстертации СПБГУ',
                  'Использование функции map в Python',
                  'Внеклассные занятия младшеклассников в Тверской муниципальной школе №83']
        return titles[random.randint(0, len(titles) - 1)]

    @staticmethod
    def str_time_prop(start, end, time_format, prop):
        stime = time.mktime(time.strptime(start, time_format))
        etime = time.mktime(time.strptime(end, time_format))

        ptime = stime + prop * (etime - stime)

        return time.strftime('%Y-%m-%d %H:%M', time.localtime(ptime))

    def random_date(self, start, end, prop):
        return self.str_time_prop(start, end, '%m/%d/%Y %I:%M %p', prop)
