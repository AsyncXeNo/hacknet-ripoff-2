import os
import json

from utils.my_logging import get_logger
from terminal_game import internet


def clean():
    with open('data/generated_ids.json', 'w') as f:
        json.dump([], f, indent=4)
    with open('data/generated_ips.json', 'w') as f:
        json.dump([], f, indent=4)


def main():
    clean()
    
    web = internet.Internet()
    my_os = web.add_os('asyncxeno', '11111111')
    other_os = web.add_os('testing123', 'testing123')

    while True:
        cmd = input(f'{my_os.main_terminal.new_line()}')
        response = my_os.main_terminal.run_command([arg.strip() for arg in cmd.split(' ')])
        print(response['exit_code'])
        print(response['stdout'])
        print(response['stderr'])


if __name__ == '__main__':
    logger = get_logger(__name__)
    main()