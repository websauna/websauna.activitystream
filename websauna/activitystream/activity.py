from uuid import UUID

from sqlalchemy.orm import Session

from websauna.system.http import Request
from websauna.system.user.models import User
from websauna.utils.time import now

from .events import ActivityCreated
from .models import Activity
from .models import Stream


def create_activity(request: Request, msg_id: str, msg_context: dict, object_id: UUID, user: User):
    """Creates a new activity.

    The caller is responsible for firing events.

    :param request:
    :param msg_id:
    :param msg_context:
    :param object_id:
    :param user:
    :return:
    """
    dbsession = Session.object_session(user)

    stream = Stream.get_or_create_user_stream(user)

    a = Activity()
    a.object_id = object_id
    a.msg_id = msg_id
    a.msg_context = msg_context

    stream.activities.append(a)
    dbsession.flush()

    return a


def get_unread_activity_count(user: User):
    """Get number of unseen activities"""

    stream = Stream.get_or_create_user_stream(user)
    return stream.activities.filter(Activity.seen_at == None).count()


def mark_seen(user: User, object_id: UUID):
    stream = Stream.get_or_create_user_stream(user)
    unread = stream.activities.filter(Activity.object_id== object_id)
    unread.update(values=dict(seen_at=now()))