from aiohttp import web
import json
from CourseHolder import CourseHolder
import argparse
import aiohttp
import asyncio
import logging


class Main(CourseHolder):  # main class
    rubles = 0
    euros = 0
    dollars = 0
    aliases = {}

    def __init__(self, course_update_cool_down, rubles, dollars, euros, debug, aliases=None):
        if aliases is None:
            logging.warning('aliases not provide')
            aliases = {'eur': 'eur', 'rub': 'rub', 'usd': 'usd'}
        else:
            if 'eur' not in aliases:
                aliases['eur'] = 'eur'
            if 'rub' not in aliases:
                aliases['rub'] = 'rub'
            if 'usd' not in aliases:
                aliases['usd'] = 'usd'

        self.aliases = aliases
        self.dollars = dollars
        self.euros = euros
        self.rubles = rubles
        logging.info('app started')

        # start server
        self.app = web.Application()
        self.set_routes()
        runner = aiohttp.web.AppRunner(self.app)
        logging.info('server changed to up state')
        asyncio.get_event_loop().run_until_complete(runner.setup())
        site = aiohttp.web.TCPSite(runner)
        asyncio.get_event_loop().run_until_complete(site.start())

        try:
            super().__init__(course_update_cool_down, debug)  # init master-constructor
        except KeyboardInterrupt:
            logging.warning('App closed by user request (Ctrl + C)')
            print('Script killed by user request')
            input()

    def output_info_composer(self):
        return '\n{rub_a}: {rub}\n{usd_a}: {usd}\n{eur_a}: {eur}\n\n'.format(
            rub_a=self.aliases['rub'],
            eur_a=self.aliases['eur'],
            usd_a=self.aliases['usd'],
            rub=self.rubles,
            eur=self.euros,
            usd=self.dollars
        ) + '{rub_usd_a}:  {rub_usd}\n{rub_eur_a}: {rub_eur}\n{usd_eur_a}: {usd_eur}\n\n'.format(
            rub_usd_a=self.aliases['rub'] + '-' + self.aliases['usd'],
            rub_eur_a=self.aliases['rub'] + '-' + self.aliases['eur'],
            usd_eur_a=self.aliases['usd'] + '-' + self.aliases['eur'],
            rub_usd=self.dollars,
            rub_eur=self.eur,
            usd_eur=self.currency_ratio
        ) + 'sum: {rub} {rub_a} / {usd} {usd_a} / {eur} {eur_a}\n'.format(
            rub=self.rubles + self.dollars * self.dollar + self.euros * self.eur,
            usd=self.dollars + self.rubles / self.dollar + self.euros / self.currency_ratio,
            eur=self.euros + self.rubles / self.eur + self.dollars * self.currency_ratio,
            rub_a=self.aliases['rub'],
            eur_a=self.aliases['eur'],
            usd_a=self.aliases['usd']
        )

    def print_course(self):  # overrides course print
        if not self.debug and self.course_changed:
            print(self.output_info_composer())
            self.course_changed = False

    def set_routes(self):
        self.app.router.add_get('/{valuate}/{method}', self.handler)
        self.app.router.add_post('/{valuate}/{method}', self.handler)
        self.app.router.add_post('/{valuate}', self.handler)
        logging.info('routes declared on server')

    async def handler(self, request):
        response = {}
        query = str(request.rel_url)
        if self.debug:
            print('An API request was noticed\nrequest:')
        if request.method == 'GET':
            if self.debug:
                print(request.url)
            if query == '/usd/get':
                response['usd'] = self.dollars
            elif query == '/rub/get':
                response['rub'] = self.rubles
            elif query == '/eur/get':
                response['eur'] = self.euros
            elif query == '/amount/get':
                response = self.output_info_composer()
                return web.Response(text=response, status=200)
        else:
            data = await request.json()
            self.course_changed = True
            if self.debug:
                print(request.url, json.dumps(data))
            response['new_values'] = {}
            if query == '/amount/set':
                if len(data.keys())>0:
                    if 'rub' in data.keys():
                        self.rubles = data['rub']
                        response['new_values']['rub'] = self.rubles
                    if 'usd' in data.keys():
                        self.dollars = data['usd']
                        response['new_values']['usd'] = self.dollars
                    if 'eur' in data.keys():
                        self.euros = data['eur']
                        response['new_values']['eur'] = self.euros
                else:
                    logging.warning('API requested at POST without parameters')
            elif query == '/modify':
                if 'rub' in data.keys():
                    self.rubles += data['rub']
                    response['new_values']['rub'] = self.rubles
                if 'usd' in data.keys():
                    self.dollars += data['usd']
                    response['new_values']['usd'] = self.dollars
                if 'eur' in data.keys():
                    self.euros += data['eur']
                    response['new_values']['eur'] = self.euros
        logging.debug('API requested as '+str(request.method)+' with param '+str(request.rel_url)+' and responded like '
                      + str(response))
        if self.rubles < 0 or self.dollars < 0 or self.euros < 0:
            logging.warning('One or more of the monetary units has taken a negative value')
        if self.debug:
            print('response:\n', json.dumps(response))
        return web.Response(text=json.dumps(response), status=200, headers={'content-type': 'text/plain'})


if __name__ == '__main__':
    logging.basicConfig(filename="C:/Users/gagat/Desktop/ujin_microservice/debug.log", level=logging.DEBUG)
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
