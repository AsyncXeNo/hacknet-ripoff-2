from utils.id_generator import IdGenerator
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

    def __init__(self, name: str, contents, parent):
        """Inits the file using name and a parent.
        
        Arguments:
            name -- name of the file.
            parent -- parent of the file (must be a Directory).
        """
        
        super().__init__(f'FIL-{IdGenerator.generate_id(4)}', name, contents, parent)

    def set_name(self, name: str):
        """Splits name into filename and extension and stores them."""

        self._validate_name(name)
        namesplit = name.split('.')
        self.filename = namesplit[0] if len(namesplit) == 1 else '.'.join(namesplit[0:-1])
        self.extension = None if len(namesplit) == 1 else namesplit[-1]
        logger.info(f'Setting name for {self.__class__.__name__} with id {self.SUID} to "{name}".')

    def get_name(self):
        """returns the name of the file."""

        return f'{self.filename}.{self.extension}' if self.extension else self.filename

    def replace(self, old: str, new: str, count=None):
        """Replaces a part of the contents with something else.
        
        Arguments:
            old -- The part of the contents you wish to replace.
            new -- What you want to replace it with.
        """

        if isinstance(self.get_contents(), bytes):
            raise TypeError('Cannot replace contents of a byte file.')
        if not (isinstance(old, str) and isinstance(new, str)):
            raise TypeError('Both arguments need to be of type str.', old, new)

        self.get_contents().replace(old, new, count) if count else self.get_contents().replace(old, new)
        logger.info(f'Replaced "{old}" with "{new}" in the contents of {self.__class__.__name__} with id {self.SUID}.')

    def _validate_contents(self, contents):
        """Raises appropriate exception if file contents are of invalid type."""

        super()._validate_contents(contents)
        logger.info(f'Validating contents for {self.__class__.__name__} with id {self.SUID}.')
        if isinstance(contents, list):
            raise exceptions.SUInvalidContents('File contents need to be of type str or bytes.', contents)
        