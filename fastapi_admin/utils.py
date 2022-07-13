import random
import string

import bcrypt


def generate_random_str(
        length: int,
        is_digit: bool = True,
):
    if is_digit:
        all_char = string.digits
    else:
        all_char = string.ascii_letters + string.digits
    return "".join(random.sample(all_char, length))


def check_password(password: str, password_hash: str):
    return bcrypt.checkpw(password.encode(), password_hash.encode())


def hash_password(password: str):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def localtime(value, timezone=None):
    """
    Convert an aware datetime.datetime to local time.
    Local time is defined by the current time zone, unless another time zone
    is specified.
    """
    # Emulate the behavior of astimezone() on Python < 3.6.
    if value.utcoffset() is None:
        return value
    return value.astimezone(timezone) if timezone else value.astimezone()
