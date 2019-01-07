from functools import wraps
from .factories import AuthenticatorFactory


def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        return AuthenticatorFactory.get_instance().authenticate(
            f, *args, **kwargs)
    return decorated_function


def authorize(required_permissions=[]):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            return AuthenticatorFactory.get_instance().authorize(
                required_permissions, f, *args, **kwargs)
        return decorated_function
    return decorator
