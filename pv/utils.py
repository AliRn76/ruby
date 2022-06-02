from cache.queries import get_pv_members_from_redis, set_pv_users_in_redis
from pv.models import PV


def get_pv_users_from_db(pv_id: int):
    pv = PV.objects.get(id=pv_id)
    return [pv.user1_id, pv.user2_id]


def get_pv_members(pv_id: int) -> list[int]:
    cached_users = get_pv_members_from_redis(pv_id)
    if not cached_users:
        users = get_pv_users_from_db(pv_id)
        set_pv_users_in_redis(pv_id, users)
    else:
        users = cached_users

    return users
