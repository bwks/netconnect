class Error(Exception):
    """Base class for other exceptions"""
    pass


class LoginTimeoutError(Error):
    """Raised when the input value is too small"""
    pass


class LoginCredentialsError(Error):
    """Raised when the input value is too large"""
    pass


class EnablePasswordError(Error):
    """Raised when the input value is too large"""
    pass
