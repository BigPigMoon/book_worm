import logging

from models.user import User


logger = logging.getLogger()


def registration(uid: str):
    """Registrate new user"""

    user = get_current_user(uid)
    if not user:
        User.create(telegram_id=uid)


def get_current_user(uid: str) -> User | None:
    """Get current user from user telegram id"""

    if not uid:
        logger.warning("User id does not exist")
        return None

    try:
        return User.select().where(User.telegram_id == uid).get()
    except User.DoesNotExist:
        return None

    return None
