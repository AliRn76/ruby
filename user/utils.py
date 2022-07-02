import random
from configs.settings import OTP_LEN


def generate_otp() -> str:
    # otp = random.randint(10 ** (OTP_LEN - 1), (10 ** OTP_LEN) - 1)
    otp = 1111
    return str(otp)


def send_otp():
    pass
