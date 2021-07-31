from utils.my_logging import get_logger


logger = get_logger(__name__)


class Terminal(object):
    def __init__(self, os, opened_by):
        self.name = 'Terminal'
        self.os = os
        self.current_dir = self.os.root

        self.opened_by = opened_by
        self.connected_to = None

        self.commands = {
            '_test': self._test
        }

    def run_command(self, args):
        self.os.verify_system_integrity()
        command = args.pop(0)
        return self.commands[command](args)

    def _test(self, args):
        if len(args) < 1:
            raise Exception()
        path = args[0]

        return self.os.parse_path(path, self.current_dir).get_name()