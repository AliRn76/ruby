import orjson as json
from cache.keys import pv_members, group_members, otp_key
from configs.settings import REDIS, PV_EXP_TIME, REDIS_ONLINE_USERS, REDIS_UNREAD_MESSAGES, OTP_EXP_TIME


# # # Online/ Offline
def is_online(user_id: int) -> str:
    """ return user channel_name """
    _is_online = REDIS_ONLINE_USERS.get(user_id) or b''
    return _is_online.decode()

def set_user_offline_in_redis(user_id: int) -> None:
    REDIS_ONLINE_USERS.delete(user_id)

def set_user_online_in_redis(user_id: int, channel_name: str) -> None:
    REDIS_ONLINE_USERS.set(user_id, channel_name)


# # # PV Members
def get_pv_members_from_redis(pv_id: int) -> list[str]:
    members = REDIS.smembers(pv_members(pv_id))
    return [u.decode() for u in members]

def set_pv_users_in_redis(pv_id: int, users: list[int]) -> None:
    REDIS.sadd(pv_members(pv_id), *users)
    REDIS.expire(pv_members(pv_id), PV_EXP_TIME)

# # # Group Members
def get_group_members_from_redis(group_id: int) -> list[str]:
    members = REDIS.smembers(group_members(group_id))
    return [u.decode() for u in members]

def set_group_users_in_redis(pv_id: int, users: list[int]) -> None:
    REDIS.sadd(pv_members(pv_id), *users)
    REDIS.expire(pv_members(pv_id), PV_EXP_TIME)


# # # Unread Messages
def save_unread_message(user_id: int, message: dict) -> None:
    REDIS_UNREAD_MESSAGES.sadd(user_id, json.dumps(message))

def get_unread_messages_from_redis(user_id: int) -> list[str]:
    messages = REDIS_UNREAD_MESSAGES.smembers(user_id)
    REDIS_UNREAD_MESSAGES.delete(user_id)
    return [m.decode() for m in messages]


# # # OTP
def set_otp(user_id: int, otp: str):
    REDIS.set(otp_key(user_id), otp, ex=int(OTP_EXP_TIME))

def get_otp(user_id: int) -> str:
    otp = REDIS.get(otp_key(user_id)) or b''
    return otp.decode()

def remove_otp(user_id: int):
    REDIS.delete(otp_key(user_id)) 
