import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# time format
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT_MOMENT = "YYYY-MM-DD HH:mm:ss"
DATE_FORMAT_MOMENT = "YYYY-MM-DD"

# redis cache
CAPTCHA_ID = "captcha:{captcha_id}"
LOGIN_ERROR_TIMES = "login_error_times:{ip}"
LOGIN_USER = "login_user:{token}"
