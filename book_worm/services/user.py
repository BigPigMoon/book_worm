import logging

from models.user import User


logger = logging.getLogger()


def registration(uid: str):
    """Registrate new user."""
    if not uid:
        logger.warning("User id does not exist")
        return

    user: User
    try:
        user = User.select().where(User.telegram_id == uid).get()
    except User.DoesNotExist:
        user = None

    if not user:
        User.create(telegram_id=uid)
