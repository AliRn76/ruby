def pv_members(pv_id: int) -> str: return f'pv_{pv_id}'

def group_members(group_id: int) -> str: return f'group_{group_id}'

def otp_key(user_id: int) -> str: return f'otp_{user_id}'

def forget_password_otp_key(user_id: int) -> str: return f'forget_password_otp_{user_id}'
