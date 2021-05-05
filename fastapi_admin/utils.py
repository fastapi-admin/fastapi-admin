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
