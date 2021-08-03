from abc import ABCMeta, abstractmethod
import requests
import asyncio
import datetime
import logging


class CourseHolder:
    __metaclass__ = ABCMeta
    eur = 0
    dollar = 0
    course_update_cool_down = 0  # in minutes
    currency_ratio = 0
    debug = False
    course_changed = False

    def __init__(self, course_update_cool_down, debug):
        if debug.lower() in ('1', 'true', 'y'):
            self.debug = True
        else:
            self.debug = False
        if not self.debug:
            print('Application started')
        self.course_update_cool_down = course_update_cool_down
        self.check_course_stream = asyncio.get_event_loop()
        tasks = asyncio.wait([self.check_course_stream.create_task(self.check_course()),
                              self.check_course_stream.create_task(self.show_course())])
        logging.debug('check course stream started')
        self.check_course_stream.run_until_complete(tasks)
        self.check_course_stream.close()

    async def check_course(self):
        logging.debug('valuate course requested from API')
        last_course = (self.eur, self.dollar)
        try:
            response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')  # check course
            self.eur = response.json()['Valute']['EUR']['Value']
            self.dollar = response.json()['Valute']['USD']['Value']
            self.currency_ratio = self.dollar / self.eur
        except Exception as e:
            logging.warning('The request on course API was receive with errors, the exchange rate was not replaced '
                            '. Error: ' + str(e))
        if (self.eur, self.dollar) != last_course:
            self.course_changed = True
        if not self.debug:
            print('Valuate course updated at', datetime.datetime.now())
        await asyncio.sleep(self.course_update_cool_down * 60)
        await self.check_course_stream.create_task(self.check_course())

    @abstractmethod
    def print_course(self):
        pass

    async def show_course(self):
        self.print_course()
        await asyncio.sleep(60)
        await self.check_course_stream.create_task(self.show_course())
