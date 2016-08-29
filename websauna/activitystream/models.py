"""Place your SQLAlchemy models in this file."""

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as psql
from sqlalchemy import orm

from websauna.activitystream.interfaces import IActivity
from websauna.system.model.columns import UTCDateTime
from websauna.system.model.json import NestedMutationDict
from websauna.system.model.meta import Base
from websauna.system.user.models import User
from websauna.utils.time import now
from zope.interface import implementer


class Stream(Base):
    """User activity stream."""

    __tablename__ = "activity_stream"

    id = sa.Column(psql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()"), )

    user_id = sa.Column(sa.ForeignKey("users.id"), nullable=False)
    user = orm.relationship(User,
                        backref=orm.backref("activity_stream",
                                        uselist=False,
                                        cascade="all, delete-orphan",
                                        single_parent=True, ),)


    @classmethod
    def get_or_create_user_stream(cls, user: User):
        stream = user.activity_stream
        if not stream:
            dbsession = orm.Session.object_session(user)
            stream = Stream(user=user)
            dbsession.add(stream)
            dbsession.flush()
        return stream


@implementer(IActivity)
class Activity(Base):
    """One activity in user stream."""

    __tablename__ = "activity"

    id = sa.Column(psql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()"), )

    stream_id = sa.Column(sa.ForeignKey("activity_stream.id"), nullable=False, primary_key=True)
    stream = orm.relationship("Stream", uselist=False,
                              backref=orm.backref("activities", lazy="dynamic"))

    #: The object this activity is targeted for. This is our key to mark activities seen.
    object_id = sa.Column(psql.UUID(as_uuid=True), nullable=False)

    #: When this was created
    created_at = sa.Column(UTCDateTime, default=now, nullable=False)

    #: When this data was updated last time
    updated_at = sa.Column(UTCDateTime, onupdate=now)

    #: When the user marked this activity seen
    seen_at = sa.Column(UTCDateTime, default=None, nullable=True)

    #: We use this as a key to look up different activity renderers.
    activity_type = sa.Column(sa.String(64), nullable=False)

    #: Template variables passed to the message renderer
    msg_context = sa.Column(NestedMutationDict.as_mutable(psql.JSONB), default=dict)

    __mapper_args__ = {
        "order_by": created_at.desc()
    }


