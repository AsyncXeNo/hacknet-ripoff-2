from utils import exceptions
from utils.my_logging import get_logger
from terminal_game.storage_unit import StorageUnit


logger = get_logger(__name__)


class Directory(StorageUnit):
    """Class representing a Directory in the virtual file system.

    This class represents a Directory in the virtual file system.
    It needs to have a name, contents and a parent.

    Attributes:
        name: string representing the name of the directory.
        contents: list representing the contents of the directory.
        parent: directory which the current directory belongs to
    """

    def __init__(self, name: str, parent):
        """Initialized the directory using a name and a parent.
        
        Arguments:
            name -- name of the directory.
            parent -- parent of the directory
        """

        super().__init__(name, [], parent)

    def add(self, storage_unit):
        """Adds an object of type StorageUnit to the contents of the directory."""
        
        self._validate_directory_element(storage_unit)
        self.contents.append(storage_unit)
        storage_unit.set_parent(self)
        logger.debug(f'Added storage unit with id {storage_unit.get_id()} to directory with id {self.SUID}.')

    def delete(self, storage_unit_name):
        """Deleted the storage unit with the given name"""

        unit = self.get_element_by_name(storage_unit_name)
        self.contents.remove(unit)
        logger.debug(f'Deleted storage unit with id {unit.get_id()} from directory with id {self.SUID}.')

    def get_element_by_name(self, element_name):
        """Returns element with given name from contents."""
        
        return list(filter(self.contents, lambda e: e.get_name() == element_name))[0]

    def _validate_contents(self, contents):
        """Raises appropriate exception if directory contents are of invalid type."""

        logger.debug(f'Validating contents for directory with id {self.SUID}.')
        super()._validate_contents(contents)
        if not isinstance(contents, list):
            raise exceptions.SUInvalidContents('Directory contents need to be of type list.')
        for element in contents:
            self._validate_directory_element(element)

    def _validate_directory_element(self, storage_unit):
        """Raises appropriate exception if directory element is not of valid type."""

        logger.debug(f'Validating storage unit to add it to directory with id {self.SUID}.')        
        if not isinstance(storage_unit, StorageUnit):
            raise exceptions.SUDirectoryElementError('Directory element needs to be of type StorageUnit.')
        if storage_unit.get_name() in [unit.get_name() for unit in self.get_contents()]:
            raise exceptions.SUDirectoryElementError('Another storage unit with this name already exists in this directory.')

        