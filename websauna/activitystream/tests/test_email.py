"""An example py.test functional test case."""
from uuid import uuid4

import pytest
import transaction

from sqlalchemy.orm.session import Session

from pyramid.registry import Registry
from pyramid_mailer.mailer import DummyMailer
from websauna.activitystream.interfaces import NoRendererRegistered
from websauna.system.http.utils import make_routable_request
from websauna.system.mail.utils import get_mailer
from websauna.system.user.models import User

from websauna.activitystream.activity import create_activity
from websauna.tests.utils import create_user, make_dummy_request

from ..channel import Email


@pytest.fixture
def user_id(dbsession, registry):
    with transaction.manager:
        user = create_user(dbsession, registry)
        return user.id



def test_push_no_renderer(dbsession: Session, user_id):
    """Create a new activity, but we do not have renderer for it yet."""

    request = make_dummy_request(dbsession, Registry())

    with transaction.manager:
        u = dbsession.query(User).get(user_id)

        # This will trigger email on transaction commit
        a = create_activity(request, "demo_msg", {}, uuid4(), u)

        channel = Email(request)
        with pytest.raises(NoRendererRegistered):
            channel.push_notification(a)


def test_push_render_email(dbsession: Session, registry, user_id):
    """Create a new activity and generates rendered email notification.."""

    # Create a request with route_url()
    request = make_routable_request(dbsession, registry)

    # Reset test mailer at the beginnign of the test
    mailer = get_mailer(registry)

    # Check we got a right type of mailer for our unit test
    assert isinstance(mailer, DummyMailer)
    assert len(mailer.outbox) == 0

    with transaction.manager:
        u = dbsession.query(User).get(user_id)

        # Create an activity
        a = create_activity(request, "demo_msg", {"text": "foobar"}, uuid4(), u)

        # Push it through notification channel
        channel = Email(request)
        channel.push_notification(a)

        # DummyMailer updates it outbox immediately, no need to wait transaction.commit
        assert len(mailer.outbox) == 1



