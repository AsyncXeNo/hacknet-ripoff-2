from utils import exceptions
from utils.my_logging import get_logger
from terminal_game.storage_unit import StorageUnit


logger = get_logger(__name__)


class File(StorageUnit):
    """Class representing a file in the virtual file system.
    
    This class represents a file in the virtual file system.
    It needs to have a name, contents and a parent.

    Attributes:
        name: string representing the name of the file.
        contents: represent the contents of the file.
        parent: Directory which the file belongs to.
    """

    def __init__(self, name: str, parent):
        """Inits the file using name and a parent.
        
        Arguments:
            name -- name of the file.
            parent -- parent of the file (must be a Directory).
        """
        
        super().__init__(name, "", parent)

    def set_name(self, name: str):
        """Splits name into filename and extension and stores them."""

        self._validate_name(name)
        namesplit = name.split('.')
        self.filename = namesplit[0] if len(namesplit) == 1 else '.'.join(namesplit[0:-1])
        self.extension = None if len(namesplit) == 1 else namesplit[-1]
        logger.debug(f'Setting name for file with id {self.SUID} to {name}.')

    def get_name(self):
        """returns the name of the file."""

        return f'{self.filename}.{self.extension}' if self.extension else self.filename

    def _validate_contents(self, contents):
        """Raises appropriate exception if file contents are of invalid type."""

        super()._validate_contents(contents)
        logger.debug(f'Validating contents for file with id {self.SUID}.')
        if isinstance(contents, list):
            raise exceptions.SUInvalidContents('File contents need to be of type str or bytes.')
        