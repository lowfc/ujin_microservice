from abc import ABCMeta, abstractmethod
import requests
import asyncio


class CourseHolder:
    __metaclass__ = ABCMeta
    eur = 0
    dollar = 0
    course_update_cool_down = 0  # in minutes
    currency_ratio = 0

    def __init__(self, course_update_cool_down):
        self.course_update_cool_down = course_update_cool_down
        self.check_course_stream = asyncio.get_event_loop()
        tasks = asyncio.wait([self.check_course_stream.create_task(self.check_course()),
                              self.check_course_stream.create_task(self.show_course())])
        self.check_course_stream.run_until_complete(tasks)

    async def check_course(self):
        print('requested cc')
        response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')  # check course
        self.eur = response.json()['Valute']['EUR']['Value']
        self.dollar = response.json()['Valute']['USD']['Value']
        self.currency_ratio = self.dollar / self.eur
        await asyncio.sleep(self.course_update_cool_down )
        await self.check_course_stream.create_task(self.check_course())

    @abstractmethod
    def print_course(self):
        pass
    #todo no clodes while stream awaiting
    async def show_course(self):
        print('fc')
        self.print_course()
        await asyncio.sleep(2)
        await self.check_course_stream.create_task(self.show_course())
