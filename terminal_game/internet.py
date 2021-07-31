from utils.my_logging import get_logger
from terminal_game.system import System


logger = get_logger(__name__)


class Internet(object):
    def __init__(self):
        self.operating_systems = []

    def add_os(self, username, password):
        os = System(self, username, password)
        self.operating_systems.append(os)
        return os