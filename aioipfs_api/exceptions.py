class VersionMismatchError(Exception):
    """
    Thrown when there is a mismatch between what this library supports
    and the server the client is connecting to.
    """
