from utils.my_logging import get_logger
from terminal_game import storage_unit, file, directory, root_dir


def make_file(name, parent):
    fle = file.File(name, parent)
    parent.add(fle)
    return fle


def make_dir(name, parent):
    dr = directory.Directory(name, parent)
    parent.add(dr)
    return dr


def main():
    root = root_dir.RootDir()
    file1 = make_file('testing.py', root)
    dir1 = make_dir('testing', root)

if __name__ == '__main__':
    logger = get_logger(__name__)
    main()