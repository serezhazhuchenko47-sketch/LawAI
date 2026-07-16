ADMINS = {
    329968861,
}


def is_admin(user_id: int) -> bool:
    return user_id in ADMINS

broadcast_mode = {}

