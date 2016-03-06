class NoFixupException(Exception):
    pass


class BadData(NoFixupException):
    """
    A class was instantiated with missing or bad data from the API / hook.
    """
