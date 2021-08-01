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
    debug = False

    def __init__(self, course_update_cool_down, rubles, dollars, euros, debug):
        '''if debug.lower() in ('1', 'true', 'y'):
            self.debug = True
        else:
            self.debug = False'''
        self.dollars = dollars
        self.euros = euros
        self.rubles = rubles
        super().__init__(course_update_cool_down)  # init master-constructor

    def print_course(self):  # overrides course print
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
    parser.add_argument(
        '--rub',
        type=int,
        default=0,
        help='rubles'
    )
    parser.add_argument(
        '--usd',
        type=int,
        default=0,
        help='united states dollars'
    )
    parser.add_argument(
        '--eur',
        type=int,
        default=0,
        help='euro'
    )
    parser.add_argument(
        '--period',
        type=float,
        default=1,
        help='server request period'
    )
    arguments = parser.parse_args()
    instance = Main(arguments.period, arguments.rub, arguments.usd, arguments.eur, arguments.debug)
