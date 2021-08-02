#!venv/bin/python

import json

from types import new_class
from utils import exceptions
from utils.my_logging import get_logger
from flask import Flask
from flask_restful import Api, Resource, reqparse
from utils.my_logging import get_logger
from terminal_game import internet


logger = get_logger(__name__)

web = internet.Internet()

app = Flask(__name__)
api = Api(app)


class Commands(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('func', required=True)
        parser.add_argument('info', required=True)
        
        args = parser.parse_args()

        print(args)
        func = args['func']
        info = json.loads(args['info'])
        
        if func == 'new':
            return self.new_os(info), 200
        elif func == 'cmd':
            return self.cmd(info), 200
        elif func == 'new_line':
            return self.new_line(info), 200

    def new_os(self, info):
        temp_id = info['temp_id']
        try:
            v_os = web.add_os(info['username'], info['password'])
        except Exception as e:
            return {
                'id': temp_id,
                'response_type': 'error',
                'response': e.message
            }
        else:
            return {
                'id': temp_id,
                'response_type': 'success',
                'response': v_os.IP
            }

    def cmd(self, info):
        ip = info['id']
        inp = info['input']

        try:
            v_os = web.get_os_by_ip(ip)
        except exceptions.OSNotFound as e:
            return {
                'id': ip,
                'response_type': 'error',
                'response': e.message
            }
        else:
            return {
                'id': ip,
                'response_type': 'success',
                'response': v_os.main_terminal.run_command([arg.strip() for arg in inp.split(' ')])
            }

    def new_line(self, info):
        ip = info['id']

        try:
            v_os = web.get_os_by_ip(ip)
        except exceptions.OSNotFound as e:
            return {
                'id': ip,
                'response_type': 'error',
                'response': e.message
            }
        else:
            return {
                'id': ip,
                'response_type': 'success',
                'response': v_os.main_terminal.new_line()
            }


api.add_resource(Commands, '/commands')

if __name__ == '__main__':
    app.run(port=5555)