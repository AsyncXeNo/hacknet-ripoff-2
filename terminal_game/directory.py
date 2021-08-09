from utils.id_generator import IdGenerator
from utils import exceptions
from utils.my_logging import get_logger
from terminal_game.storage_unit import StorageUnit
from terminal_game.file import File


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

    def __init__(self, name: str, contents, parent):
        """Initialized the directory using a name, contents and a parent.
        
        Arguments:
            name -- name of the directory.
            contents -- contents of the file.
            parent -- parent of the directory
        """

        super().__init__(f'DIR-{IdGenerator.generate_id(4)}', name, contents, parent)

    def bfs(self, depth=0):
        """Returns the contents of the directory in tree format."""

        bfs = ''
        for content in self.get_contents():
            bfs += ('|    '*depth)
            bfs += '| -- '
            if isinstance(content, Directory):
                bfs += f'{content.get_name()}\n'
                bfs += content.bfs(depth+1)
            elif isinstance(content, File):
                bfs += f'{content.get_name()}\n'
        return bfs

    def is_sub_su(self, storage_unit):
        """Checks if another storage unit is a sub SU of the current directory."""

        for content in self.get_contents():
            if content == storage_unit:
                return True
            if isinstance(content, Directory):
                return content.is_sub_su(storage_unit)
        return False

    def add(self, storage_unit):
        """Adds an object of type StorageUnit to the contents of the directory."""
        
        self._validate_directory_element(storage_unit)
        self.contents.append(storage_unit)
        storage_unit.set_parent(self)
        logger.info(f'Added storage unit with id {storage_unit.get_id()}, name "{storage_unit.get_name()}" and contents {storage_unit.get_contents()} to {self.__class__.__name__} with id {self.SUID}.')

    def delete(self, storage_unit_name):
        """Deleted the storage unit with the given name"""

        unit = self.get_su_by_name(storage_unit_name)
        self.contents.remove(unit)
        logger.info(f'Deleted storage unit with id {unit.get_id()} from {self.__class__.__name__} with id {self.SUID}.')

    def get_path(self):
        """Returns the absolute path of directory."""

        return f'{self.get_parent().get_path()}{self.get_name()}/'

    def get_su_by_name(self, element_name):
        """Returns element with given name from contents."""
        
        elements = list(filter(lambda e: e.get_name() == element_name, self.contents))
        if len(elements) > 0:
            return elements[0]
        logger.warning(f'SU with name "{element_name}" not found in {self.__class__.__name__} with id {self.SUID}.')
        raise exceptions.SUNotFound(f'SU with name {element_name} not found.', element_name)

    def set_contents(self, contents):
        """Sets the self.contents attribute to contents."""

        self._validate_contents(contents)
        self.contents = []
        for element in contents:
            self._validate_directory_element(element)
            self.contents.append(element)
        logger.info(f'Setting contents for {self.__class__.__name__} with id {self.SUID} to {[content.get_name() for content in self.contents]}.')

    def _validate_contents(self, contents):
        """Raises appropriate exception if directory contents are of invalid type."""

        logger.info(f'Validating contents for {self.__class__.__name__} with id {self.SUID}.')
        if not isinstance(contents, list):
            raise exceptions.SUInvalidContents('Directory contents need to be of type list.', contents)

    def _validate_directory_element(self, storage_unit):
        """Raises appropriate exception if directory element is not of valid type."""

        logger.info(f'Validating storage unit to add it to {self.__class__.__name__} with id {self.SUID}.')        
        if not isinstance(storage_unit, StorageUnit):
            raise exceptions.SUDirectoryElementError('Directory element needs to be of type StorageUnit.', storage_unit)
        if storage_unit.get_name() in [unit.get_name() for unit in self.get_contents()]:
            raise exceptions.SUDirectoryElementError('Another storage unit with this name already exists in this directory.', storage_unit.get_name())

        