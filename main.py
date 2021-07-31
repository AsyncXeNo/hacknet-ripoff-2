from utils.my_logging import get_logger
from terminal_game import file, directory, root_dir
from terminal_game import internet


def main():
    web = internet.Internet()
    my_os = web.add_os('asyncxeno', '11111111')
    logger.info(my_os.main_terminal.name)

if __name__ == '__main__':
    logger = get_logger(__name__)
    main()