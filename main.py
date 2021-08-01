from logging.config import IDENTIFIER
import os
import json

from utils.my_logging import get_logger
from terminal_game import internet


def main():
    web = internet.Internet()
    my_os = web.add_os('asyncxeno', '11111111')
    while True:
        try:
            for file in os.listdir('data/input/'):
                with open(f'data/input/{file}', 'r') as f: inp = json.load(f)
                if inp['func'] == 'new':
                    temp_id = inp['info']['temp_id']
                    username = inp['info']['username']
                    password = inp['info']['password']
                    try:
                        v_os = web.add_os(username, password)
                    except Exception as e:
                        with open(f'data/output/{file}', 'w') as f: json.dump({"id": temp_id, "response_type": "error", "response": e.message}, f, indent=4)
                    else:
                        with open(f'data/output/{file}', 'w') as f: json.dump({"id": temp_id, "response_type": "success", "response": v_os.IP}, f, indent=4)
                elif inp['func'] == 'cmd':
                    ip = inp['info']['id']
                    cmd = inp['info']['input']
                    try:
                        response = web.get_os_by_ip(ip).main_terminal.run_command([arg.strip() for arg in cmd.split(' ')])
                        response.update({'new_line': web.get_os_by_ip(ip).main_terminal.new_line()})
                    except Exception as e:
                        with open(f'data/output/{file}', 'w') as f: json.dump({"id": ip, "response_type": "error", "response": f"No os with ip {ip}"}, f, indent=4)
                    else:
                        with open(f'data/output/{file}', 'w') as f: json.dump({"id": ip, "response_type": "success", "response": response}, f, indent=4)
                os.remove(f'data/input/{file}')
        except:
            continue


if __name__ == '__main__':
    logger = get_logger(__name__)
    main()