import json
from os import system
import pickle
from logging import log

from typing import Type
from utils.parser import Parser
from utils.ip_generator import IpGenerator
from utils import exceptions
from utils.my_logging import get_logger
from terminal_game import directory, root_dir, file, storage_unit
from terminal_game import terminal


logger = get_logger(__name__)


class System(object):
    """Class representing an operating system in the virtual internet.
    
    This class represents an operating system in the virtual internet.
    It is permanently connected to the internet, needs a username and a password to initialize.

    Attributes:
        internet: Internet class containing all the operating systems in the game.
        username: username of the owner of the operating system.
        password: password of the owner of the operating system.
    """

    def __init__(self, internet, username, password):
        """Initializes the System class using internet, username and password.
        
        Arguments:
            internet -- an instance of the Internet class storing all operating systems.
            username -- string representing the username of the owner.
            password -- string representing the password of the owner.
        """
        self.IP = IpGenerator.generate_ip()
        logger.info(f'Initializing OS with IP {self.IP}.')

        self.set_internet(internet)
        self.set_username(username)
        self.set_password(password)

        self._init()

        self.terminals = []
        self.main_terminal = self.get_terminal()

    def get_terminal(self):
        """Tries to get a terminal, stored in the system files. Raises exception if data is corrupt or file not found."""

        try:
            system_data = self.root.get_element_by_name('system').get_element_by_name('system.dat')
        except Exception as e:
            raise exceptions.OSCorrupted(e.message)

        try:
            terminal_class = pickle.loads(system_data.get_contents())
        except Exception as e:
            raise exceptions.OSCorrupted('The terminal found in system.dat is not safe or corrupted.')
        
        if terminal_class != terminal.Terminal:
            raise exceptions.OSCorrupted('The terminal found in system.dat is not safe or corrupted.')

        term = terminal_class()
        self.terminals.append(term)
        return term

    def set_internet(self, internet):
        """Sets the internet for the operating system."""
        
        self._validate_internet(internet)
        self.internet = internet
        logger.info(f'Setting internet for OS with ip {self.IP}.')

    def set_username(self, username):
        """Sets the username for the operating system."""

        self._validate_username(username)
        self.username = username
        logger.info(f'Setting username for OS with ip {self.IP}.')

    def set_password(self, password):
        """Sets the password for the operating system."""

        self._validate_password(password)
        self.password = password
        logger.info(f'Setting password for OS with ip {self.IP}.')

    def make_dir(self, name, contents, parent):
        """Makes a directory using name and parent and adds it to the parent."""

        dr = directory.Directory(name, contents, parent)
        parent.add(dr)
        return dr

    def make_file(self, name, contents, parent):
        """Makes a file using name and parent and adds it to the parent."""

        fl = file.File(name, contents, parent)
        parent.add(fl)
        return fl

    def parse_path(self, path):
        """Parses a given path and returns the SU found. Raises SUNotFound exception if no SU found."""

        pass

    def _init(self):
        """Performs all the initialization steps to make the operating system usable."""

        with open('res/os_root.json', 'r') as f:
            self.root = Parser.parse_root(json.load(f))
        logger.info(f'Setting root directory for OS with ip {self.IP}.')

        try:
            system_dr = self.root.get_element_by_name('system')
        except exceptions.SUNotFound:
            system_dr = self.make_dir('system', [], self.root)

        try:
            system_data = system_dr.get_element_by_name('system.dat')
        except exceptions.SUNotFound:
            system_data = self.make_file('system.dat', "", system_dr)

        system_data.set_contents(pickle.dumps(terminal.Terminal))
        logger.info(f'Initialization complete for OS with ip {self.IP}.')

    def _validate_internet(self, internet):
        """Raises exception if internet is not of valid type."""

        logger.info(f'Validating internet for OS with ip {self.IP}.')
        from terminal_game.internet import Internet
        if not isinstance(internet, Internet):
            raise exceptions.OSInvalidInternet('internet variable needs to be of type Internet.', internet)

    def _validate_username(self, username):
        """Raises exception if username is not of valid format."""

        logger.info(f'Validating username for OS with ip {self.IP}.')
        if not isinstance(username, str):
            raise exceptions.OSInvalidUsername('username needs to be of type str.', username)
        elif len(username) < 3:
            raise exceptions.OSInvalidUsername('username cannot be less than 3 characters long.', username)
        elif len(username) > 50:
            raise exceptions.OSInvalidUsername('username cannot be more than 50 characters long.', username)

    def _validate_password(self, password):
        """Raises exception if password is of invalid format."""

        logger.info(f'Validating password for OS with ip {self.IP}.')
        if not isinstance(password, str):
            raise exceptions.OSInvalidPassword('password needs to be of type str.', password)
        elif len(password) < 8:
            raise exceptions.OSInvalidPassword('password cannot be less than 8 characters long.', password)
        elif len(password) > 30:
            raise exceptions.OSInvalidPassword('password cannot be more than 30 characters long.', password)
        