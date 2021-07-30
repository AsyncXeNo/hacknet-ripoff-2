from utils import exceptions
from utils.my_logging import get_logger
from utils.id_generator import IdGenerator


logger = get_logger(__name__)


class StorageUnit(object):
    """Storage unit of a file system.

    This class represents a storage unit of the virtual file system.
    This class cannot be used on it's own.
    It can be used either as a File or a Directory.

    Attributes:
        name: string representing the name of the storage unit.
        contents: stores the contents of the storage unit. 
        parent: Directory which the storage unit belongs to.       
    """

    def __init__(self, suid, name: str, contents, parent):
        """Inits StorageUnit using name, contents and a parent.
        
        Arguments:
            name -- name of the storage unit.
            contents -- contents of the storage unit.
            parent -- Directory which the storage unity belongs to.
        """

        self.SUID = suid
        logger.debug(f'Initializing {self.__class__.__name__} with id {self.SUID}.')

        self.set_parent(parent)
        self.set_name(name)
        self.set_contents(contents)

    def set_name(self, name: str):
        """Sets the self.name attribute to name."""

        self._validate_name(name)
        self.name = name
        logger.debug(f'Set name for {self.__class__.__name__} with id {self.SUID} to "{name}".')

    def set_contents(self, contents):
        """Sets the self.contents attribute to contents."""

        self._validate_contents(contents)
        self.contents = contents
        logger.debug(f'Setting contents for {self.__class__.__name__} with id {self.SUID}.')

    def set_parent(self, parent):
        """Sets the self.parent attribute to parent"""

        self._validate_parent(parent)
        self.parent = parent
        logger.debug(f'Setting parent for {self.__class__.__name__} with id {self.SUID}.')

    def get_id(self):
        """Returns the id of the storage unit."""

        return self.SUID

    def get_name(self):
        """Returns the name of the storage unit."""
        
        return self.name

    def get_contents(self):
        """Returns the contents of the storage unit."""
        
        return self.contents

    def get_parent(self):
        """Returns the parent of the storage unit."""

        return self.parent

    def get_path(self):
        """Returns the absolute path of the storage unit."""

        return f'{self.get_parent().get_path()}/{self.get_name()}'

    def _validate_name(self, name: str):
        """Raises appropriate exception if a name is not of valid format."""

        logger.debug(f'Validating name for {self.__class__.__name__} with id {self.SUID}.')
        if not isinstance(name, str):
            raise TypeError('Name has to be of type string.')
        if name in [unit.get_name() for unit in self.get_parent().get_contents()]:
            raise exceptions.SUNameError('Another storage unit with this name already exists in the parent directory.')
        if len(name) < 1:
            raise exceptions.SUNameError('Name cannot be empty.')
        if len(name) > 50:
            raise exceptions.SUNameError('Name is too long.')
        for letter in name:    
            if letter in ['<', '>', ':', '"', '/', '\\', '|', '?', '*']:
                raise exceptions.SUNameError(f'{name} is not a valid name.')

    def _validate_contents(self, contents):
        """Raises appropriate exception if contents are not of valid format."""

        logger.debug(f'Validating contents for storage unit with id {self.SUID}.')
        if not (isinstance(contents, str) or isinstance(contents, bytes) or isinstance(contents, list)):
            raise exceptions.SUInvalidContents(f'Contents cannot be of type {type(contents)}')

    def _validate_parent(self, parent):
        """Raises appropriate exception if parent is not of valid type."""
        
        logger.debug(f'Validating parent for {self.__class__.__name__} with id {self.SUID}.')
        from terminal_game.directory import Directory
        if not isinstance(parent, Directory):
            raise exceptions.SUInvalidParent('Parent needs to be of type Directory')
