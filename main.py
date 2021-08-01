import sys

from utils.my_logging import get_logger
from terminal_game import file, directory, root_dir
from terminal_game import internet


def main():
    web = internet.Internet()
    my_os = web.add_os('asyncxeno', '11111111')
    while True:
        cmd = input('command:')
        response = my_os.main_terminal.run_command([arg.strip() for arg in cmd.split()])
        print(f'code {response["exit_code"]}\n{response["stdout"]}\n{response["stderr"]}')


if __name__ == '__main__':
    logger = get_logger(__name__)
    main()