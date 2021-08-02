import shlex

from terminal_game.root_dir import RootDir
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
            'connect': self._connect,
            'disconnect': self._disconnect,
            'cd': self._cd,
            'mv': self._mv,
            'cp': self._cp,
            'tree': self._tree,
            'ls': self._ls,
            'echo': self._echo,
            'ip': self._ip,
            'cat': self._cat,
            'mkdir': self._mkdir,
            'touch': self._touch,
            'rm': self._rm,
            'write': self._write,
            'replace': self._replace,
        }

    def new_line(self):
        """Returns a new line."""

        if self.connected_to: return self.connected_to.new_line()
        name = self.os.username if self.opened_by == self.os else f'{self.opened_by.IP}(guest)'
        return f'{name}:{self.current_dir.get_path()}$ '


    def run_command(self, args):
        """Runs a command if it is supported in the terminal. Returns the result of the command."""
    
        try:
            self.os.verify_system_integrity()
        except exceptions.OSCorrupted as e:
            if self.opened_by != self.os:
                self._disconnect(args)
            return self._response(1, None, e.message)

        if self.connected_to:
            return self.connected_to.run_command(args)

        # if self.sub_command:
        #     self.sub_command(args)
            
        command = args.pop(0)
        try:
            return self.commands[command](args)
        except KeyError:
            return self._response(1, None, 'command not found.')

    def _connect(self, args):
        if len(args) < 1: return self._response(1, None, 'Too few arguments.\nSyntax: connect <ip>')

        if self.opened_by != self.os:
            return self._response(1, None, 'You are not the root user and hence cannot use this command.')

        try:
            os = self.os.internet.get_os_by_ip(args[0])
        except exceptions.OSNotFound:
            return self._response(1, None, f'No system found with IP {args[0]}.')

        self.connected_to = os.get_terminal(self.os)
        logger.info(f'connected to {args[0]}')
        return self._response(0, None, None)

    def _disconnect(self, _):
        if self.opened_by == self.os:
            return self._response(1, None, 'Not connected to any system.')
        self.opened_by.main_terminal.connected_to = None
        self._close()
        return self._response(0, f'Disconnect from {self.os.IP}.', None)

    def _echo(self, args):
        return self._response(0, ' '.join(args), None)

    def _ip(self, _):
        return self._response(0, self.os.IP, None)

    def _tree(self, _):
        return self._response(0, self.current_dir.bfs(), None)

    def _ls(self, _):
        return self._response(0, '\n'.join([content.get_name() for content in self.current_dir.get_contents()]), None)

    def _cat(self, args):
        if len(args) < 1: return self._response(1, None, 'Too few arguments.\n Syntax: cat <path>')
        
        try:
            su = self.os.parse_path(args[0], self.current_dir)
        except exceptions.OSInvalidPath as e:
            return self._response(1, None, e.message)

        if not isinstance(su, File):
            return self._response(1, None, 'Argument must be a file.')
        return self._response(0, str(su.get_contents()), None) 

    def _rm(self, args):
        if len(args) < 1: return self._response(1, None, 'Too few arguments.\nSyntax: rm <path>')
        
        try:
            target = self.os.parse_path(args[0], self.current_dir)
        except exceptions.OSInvalidPath as e:
            return self._response(1, None, e.message)

        target.get_parent().delete(target.get_name())
        return self._response(0, None, None)

    def _mkdir(self, args):
        if len(args) < 1: return self._response(1, None, 'Too few arguments.\nSyntax: mkdir <path>')
        path = args[0].split('/')
        name = path.pop()
        if name == '': name = path.pop()
        if len(path) > 0:
            try:
                destination = self.os.parse_path('/'.join(path), relative_to=self.current_dir)
            except exceptions.OSInvalidPath as e:
                return self._response(1, None, e.message)
            if not isinstance(destination, Directory):
                return self._response(1, None, 'Cannot add directory to a file.')
        else:
            destination = self.current_dir
        try:
            self.os.make_dir(name, [], destination)
        except Exception as e:
            return self._response(1, None, e.message)
        return self._response(0, None, None)

    def _touch(self, args):
        if len(args) < 1: return self._response(1, None, 'Too few arguments.\nSyntax: touch <path>')
        path = args[0].split('/')
        name = path.pop()
        if name == '': return self._response(1, None, 'You need to provide a file name.')
        if len(path) > 0:
            try:
                destination = self.os.parse_path('/'.join(path), relative_to=self.current_dir)
            except exceptions.OSInvalidPath as e:
                return self._response(1, None, e.message)
            if not isinstance(destination, Directory):
                return self._response(1, None, 'Cannot add file to a file.')
        else:
            destination = self.current_dir
        try:
            self.os.make_file(name, '', destination)
        except Exception as e:
            return self._response(1, None, e.message)
        return self._response(0, None, None)

    def _cd(self, args):
        path = '/' if len(args) < 1 else args[0]
        try:
            destination = self.os.parse_path(path, relative_to=self.current_dir)
        except exceptions.OSInvalidPath as e:
            return self._response(1, None, e.message)
        if not isinstance(destination, Directory): return self._response(1, None, 'Cannot move into a file.')
        self.current_dir = destination
        return self._response(0, None, None)

    def _write(self, args):
        if len(args) < 2: return self._response(1, None, 'Too few arguments.\nSyntax: write <file> <contents/file>')
        try:
            file_to_write = self.os.parse_path(args[0], self.current_dir)
            if not isinstance(file_to_write, File):
                raise Exception('Path is not a file.')
        except Exception as e:
            return self._response(1, None, e.message)
        try:
            file_to_read = self.os.parse_path(args[1], self.current_dir)
            if not isinstance(file_to_read, File):
                raise exceptions.OSInvalidPath()
        except exceptions.OSInvalidPath:
            file_to_write.set_contents(' '.join(args[1:]))
            return self._response(0, None, None)
        file_to_write.set_contents(file_to_read.get_contents())
        return self._response(0, None, None)

    def _replace(self, args):
        if len(args) < 3: return self._response(1, None, 'Too few arguments.\nSyntax: replace <file> "<old>" "<new>" <count(optional)>\nfile -- the file you wish to make changes to (in quotes).\nold -- what you wish to replace (in quotes).\nnew -- what you wish to replace it with.\ncount -- how many of <old> to replace by <new> (all by default).')
        args = shlex.split(" ".join(args))
        file_to_write_path = args[0]
        old = args[1]
        new = args[2]
        count = args[3] if len(args) > 3 and isinstance(args[3], int) else None

        try:
            file_to_write = self.os.parse_path(file_to_write_path, self.current_dir)
            if not isinstance(file_to_write, File):
                raise Exception('Path is not a file.')
        except Exception as e:
            return self._response(1, None, e.message)
        try:
            file_to_read = self.os.parse_path(new, self.current_dir)
            if (not isinstance(file_to_read, File)) or (not isinstance(file_to_read.get_contents(), str)):
                raise exceptions.OSInvalidPath()
        except exceptions.OSInvalidPath:
            file_to_write.replace(old, new, count)
            return self._response(0, None, None)
        try:
            file_to_write.replace(old, file_to_read.get_contents(), count)
        except TypeError as e:
            return self._response(1, None, e.message)
        return self._response(0, None, None)

    def _mv(self, args):
        if len(args) < 2:
            return self._response(1, None, 'Too few arguments.\nSyntax: mv <oldpath> <newpath>')

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
            return self._response(1, None, e.message)
        
        try:
            new = self.os.parse_path(new, relative_to=self.current_dir)
        except exceptions.OSInvalidPath as e:
            try:
                new_dir = self.os.parse_path(new, relative_to=self.current_dir, parent_dir=True)
            except exceptions.OSInvalidPath as e:
                return self._response(1, None, e.message)
            if check_type:
                if not isinstance(old, Directory):
                    return self._response(1, None, 'Cannot put a file as a directory.')
            if isinstance(old, Directory):
                if old.is_sub_su(new_dir) or old == new_dir:
                    return self._response(1,'Cannot move a directory to a subdirectory of itself.' ,None)
            try:
                old.set_name(new.split('/')[-1])
            except exceptions.SUNameError as e:
                return self._response(1, None, e.message)
            old.get_parent().delete(old.get_name())
            new_dir.add(old)
            return self._response(0, None, None)
        else:
            if not isinstance(new, Directory):
                return self._response(1, None, f'A {new.__class__.__name__} with that name already exists in the destination path.')
            else:
                if isinstance(old, Directory):
                    if old.is_sub_su(new) or old == new:
                        return self._response(1,'Cannot move a directory to a subdirectory of itself.' ,None)
                old.get_parent().delete(old.get_name())
                new.add(old)
                return self._response(0, None, None)

    def _cp(self, args):
        if len(args) < 2:
            return self._response(1, None, 'Too few arguments.\nSyntax: cp <oldpath> <newpath>')

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
            if isinstance(old, RootDir):
                return self._response(1, None, 'Cannot copy root directory into itself.')
        except exceptions.OSInvalidPath as e:
            return self._response(1, None, e.message)
        
        try:
            new = self.os.parse_path(new, relative_to=self.current_dir)
        except exceptions.OSInvalidPath as e:
            try:
                new_dir = self.os.parse_path(new, relative_to=self.current_dir, parent_dir=True)
            except exceptions.OSInvalidPath as e:
                return self._response(1, None, e.message)
            if check_type:
                if not isinstance(old, Directory):
                    return self._response(1, None, 'Cannot put a file as a directory.')
            try:
                if isinstance(old, File):
                    self.os.make_file(new.split('/')[-1], old.get_contents(), new_dir)
                else:
                    self.os.make_dir(new.split('/')[-1], old.get_contents(), new_dir)
            except exceptions.SUNameError as e:
                return self._response(1, None, e.message)
            return self._response(0, None, None)
        else:
            if not isinstance(new, Directory):
                return self._response(1, None, f'A {new.__class__.__name__} with that name already exists in the destination path.')
            else:
                if isinstance(old, File):
                    self.os.make_file(old.get_name(), old.get_contents(), new)
                else:
                    self.os.make_dir(old.get_name(), old.get_contents(), new)
                return self._response(0, None, None)

    def _response(self, exit_code, stdout, stderr):
        return {
            'exit_code': exit_code,
            'stdout': stdout,
            'stderr': stderr
        }

    def _close(self):
        self.os.close_terminal(self)
