class LoadFileWarning(Warning):
    """
    # LoadWarning
    Low-level errors while parsing wL.
    """
    pass

class LoadFileError(Exception):
    """
    # LoadError
    High-level errors while parsing wL.
    """
    def __init__(self, message : str):
        self.message = message
        super().__init__(message)
