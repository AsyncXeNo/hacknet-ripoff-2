from terminal_game import directory
from terminal_game.directory import Directory
from terminal_game.file import File
from utils.my_logging import get_logger
from utils import exceptions


logger = get_logger(__name__)


class Terminal(object):
    """Terminal class for the Operating system.
    
    This class represents a terminal of an operating system
    inside the virtual internet. It can run a variety of commands.

    Attributes:
        os -- Operating system that the terminal belongs to.
        current_dir -- Current directory of the terminal.
        opened_by -- The operating system that opened the terminal (may differ from the OS the terminal belongs to).
        connected_to -- An operating system's terminal that the current terminal is connected to.
        commands -- dictionary with all the commands available.
    """
    def __init__(self, os, opened_by):
        """Initializes the terminal using os and opened_by.
        
        Arguments:
            os -- Operating system that the terminal belongs to.
            opened_by -- The operating system that opened the terminal (may differ from the OS the terminal belongs to).
        """

        self.os = os
        self.current_dir = self.os.root

        self.opened_by = opened_by
        self.connected_to = None

        self.commands = {
            'mv': self.mv,
            'cp': self.cp,
            'tree': self.tree,
        }

    def run_command(self, args):
        """Runs a command if it is supported in the terminal. Returns the result of the command."""

        self.os.verify_system_integrity()
        command = args.pop(0)
        try:
            return self.commands[command](args)
        except KeyError:
            return self.response(1, None, 'command not found.')

    def tree(self, _):
        return self.response(0, self.current_dir.bfs(), None)

    def mv(self, args):
        if len(args) < 2:
            return self.response(1, None, 'Invalid arguments.\nSyntax: mv <oldpath> <newpath>')

        check_type = None

        old = args[0]
        new = args[1]
        new = new.split('/')
        if new[-1] == '':
            new.pop()
            check_type = Directory
        new = '/'.join(new)

        try:
            old = self.os.parse_path(old, relative_to=self.current_dir)
        except exceptions.OSInvalidPath as e:
            return self.response(1, None, e.message)
        
        try:
            new = self.os.parse_path(new, relative_to=self.current_dir)
        except exceptions.OSInvalidPath as e:
            try:
                new_dir = self.os.parse_path(new, relative_to=self.current_dir, parent_dir=True)
            except exceptions.OSInvalidPath as e:
                return self.response(1, None, e.message)
            if check_type:
                if not isinstance(old, Directory):
                    return self.response(1, None, 'Cannot put a file as a directory.')
            if isinstance(old, Directory):
                if old.is_sub_su(new_dir) or old == new_dir:
                    return self.response(1,'Cannot move a directory to a subdirectory of itself.' ,None)
            try:
                old.set_name(new.split('/')[-1])
            except exceptions.SUNameError as e:
                return self.response(1, None, e.message)
            old.get_parent().delete(old.get_name())
            new_dir.add(old)
            return self.response(0, None, None)
        else:
            if not isinstance(new, Directory):
                return self.response(1, None, f'A {new.__class__.__name__} with that name already exists in the destination path.')
            else:
                if isinstance(old, Directory):
                    if old.is_sub_su(new) or old == new:
                        return self.response(1,'Cannot move a directory to a subdirectory of itself.' ,None)
                old.get_parent().delete(old.get_name())
                new.add(old)
                return self.response(0, None, None)

    def cp(self, args):
        if len(args) < 2:
            return self.response(1, None, 'Invalid arguments.\nSyntax: cp <oldpath> <newpath>')

        check_type = None

        old = args[0]
        new = args[1]
        new = new.split('/')
        if new[-1] == '':
            new.pop()
            check_type = Directory
        new = '/'.join(new)

        try:
            old = self.os.parse_path(old, relative_to=self.current_dir)
            logger.warning(len(old.get_contents()))
        except exceptions.OSInvalidPath as e:
            return self.response(1, None, e.message)
        
        try:
            new = self.os.parse_path(new, relative_to=self.current_dir)
        except exceptions.OSInvalidPath as e:
            try:
                new_dir = self.os.parse_path(new, relative_to=self.current_dir, parent_dir=True)
            except exceptions.OSInvalidPath as e:
                return self.response(1, None, e.message)
            if check_type:
                if not isinstance(old, Directory):
                    return self.response(1, None, 'Cannot put a file as a directory.')
            try:
                if isinstance(old, File):
                    new_su = self.os.make_file(new.split('/')[-1], old.get_contents(), new_dir)
                else:
                    new_su = self.os.make_dir(new.split('/')[-1], old.get_contents(), new_dir)
            except exceptions.SUNameError as e:
                return self.response(1, None, e.message)
            return self.response(0, None, None)
        else:
            if not isinstance(new, Directory):
                return self.response(1, None, f'A {new.__class__.__name__} with that name already exists in the destination path.')
            else:
                if isinstance(old, File):
                    new_su = self.os.make_file(old.get_name(), old.get_contents(), new)
                else:
                    new_su = self.os.make_dir(old.get_name(), old.get_contents(), new)
                return self.response(0, None, None)

    def response(self, exit_code, stdout, stderr):
        return {
            'exit_code': exit_code,
            'stdout': stdout,
            'stderr': stderr
        }
