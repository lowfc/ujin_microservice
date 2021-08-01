from aiohttp import web
import json
from CourseHolder import CourseHolder
import argparse


async def handle(request):
    response = {'status': 'ok'}
    return web.Response(text=json.dumps(response), status=200)


'''
app = web.Application()
app.router.add_get('/', handle)
web.run_app(app)
'''


class Main(CourseHolder):  # main class
    rubles = 0
    euros = 0
    dollars = 0

    def __init__(self, course_update_cool_down, rubles, dollars, euros):
        self.dollars = dollars
        self.euros = euros
        self.rubles = rubles
        super().__init__(course_update_cool_down)  # init master-constructor

    def printCourse(self):  # overrides course print
        print('rub: {}\nusd: {}\neur: {}\n'.format(self.rubles, self.dollars, self.euros))
        print('rub-usd: {}\nrub-eur: {}\nusd-eur: {}\n'.format(
            self.dollar,
            self.eur,
            self.currency_ratio
        ))
        print('sum: {} rub / {} usd / {} eur'.format(
            self.rubles + self.dollars * self.dollar + self.euros * self.eur,
            self.dollars + self.rubles / self.dollar + self.euros / self.currency_ratio,
            self.euros + self.rubles / self.eur + self.dollars * self.currency_ratio,
        ))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--debug',
        type=str,
        default='n',
        help='debug microservice (y/n/1/0/true/false)'
    )
    arguments = parser.parse_args()
    print(arguments.debug)

    #obj = Main(1, 100, 200, 300)
