
class SUInvalidParent(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
            self.info = args[1:] if len(args) > 1 else None
        else:
            self.message = None
            self.info = None


class SUInvalidContents(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
            self.info = args[1:] if len(args) > 1 else None
        else:
            self.message = None
            self.info = None


class SUDirectoryElementError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
            self.info = args[1:] if len(args) > 1 else None
        else:
            self.message = None
            self.info = None


class SUNameError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
            self.info = args[1:] if len(args) > 1 else None
        else:
            self.message = None
            self.info = None


class RootDirException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
            self.info = args[1:] if len(args) > 1 else None
        else:
            self.message = None
            self.info = None
