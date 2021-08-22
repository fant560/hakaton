# Встроенные импорты.
import asyncio
import datetime
import json
import random
import time
import uuid

import requests
# Импорты сторонних библиотек.
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from dateutil import parser

from .models import AudioRecord
from .models import Document
from .storage import write


class DocumentSocketListener(AsyncJsonWebsocketConsumer):

    async def connect(self):
        print('Соединение установлено')
        await self.accept()


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
