from utils import exceptions
from utils.my_logging import get_logger
from terminal_game.directory import Directory


logger = get_logger(__name__)


class RootDir(Directory):
    """Class representing a Root Directory.
    
    This class represents the root directory of the virtual file system.
    It has no name and no parent.
    """

    def __init__(self, contents):
        """Initialized the root directory using contents."""
        
        super().__init__("", contents, None)

    def get_path(self):
        """Returns path of the root dir"""

        return '/'

    def _validate_name(self, name: str):
        """Raises exception if there is a name."""

        logger.info(f'Validating name for {self.__class__.__name__} with id {self.SUID}')
        if name != "":
            raise exceptions.RootDirException('Cannot assign a name to root directory.', name)
    
    def _validate_parent(self, parent):
        """Raises exception if there is a parent."""
        
        logger.info(f'Validating parent for {self.__class__.__name__} with id {self.SUID}')
        if parent:
            raise exceptions.RootDirException('Cannot assign a parent to root directory.', parent)