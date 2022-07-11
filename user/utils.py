import random
from typing import List

from configs.settings import OTP_LEN, ZOHO_KEY
import requests
import json

def generate_otp() -> str:
    # otp = random.randint(10 ** (OTP_LEN - 1), (10 ** OTP_LEN) - 1)
    otp = 1111
    return str(otp)


def send_otp():
    pass


def send_mail(mails: List[str]):
    url = "https://api.zeptomail.com/v1.1/email"
    payload = {
        'bounce_address': 'noreply@bounce.ruby.alirn.ir',
        'from': {'address': 'noreply@ruby.alirn.ir'},
        'to': [{'email_address': {'address': mail}} for mail in mails],
        # 'to': [
        #     {
        #         'email_address': {'address': 'alirn1997@gmail.com', 'name': 'Ali'}
        #     }
        # ],
        'subject': 'Test Email',
        'htmlbody': '<div><b> Test email sent successfully.  </b></div>'
    }
    headers = {
        'accept': "application/json",
        'content-type': "application/json",
        'authorization': ZOHO_KEY,
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
