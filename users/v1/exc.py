

class InvalidToken(Exception):
    """
    Token is invalid or expired
    """


class UserNotFound(Exception):
    """
    User with such login and password not found
    """


class UserAlreadyExists(Exception):
    """
    User with such name already registered
    """
