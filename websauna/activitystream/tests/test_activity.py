"""An example py.test functional test case."""
from uuid import uuid4

import pytest
import transaction

from sqlalchemy.orm.session import Session

from pyramid.registry import Registry
from splinter.driver import DriverAPI
from websauna.system import DemoInitializer
from websauna.system.user.models import User

from websauna.tests.utils import create_user, make_dummy_request
from websauna.tests.utils import EMAIL
from websauna.tests.utils import PASSWORD

from websauna.activitystream.activity import create_activity, get_unread_activity_count, mark_seen


@pytest.fixture()
def test_request(dbsession):
    r =  Registry()
    return make_dummy_request(dbsession, r)


@pytest.fixture
def user_id(dbsession, registry):
    with transaction.manager:
        user = create_user(dbsession, registry)
        return user.id


def test_create(dbsession: Session, user_id, test_request):
    """Create new activity."""

    with transaction.manager:
        u = dbsession.query(User).get(user_id)
        create_activity(test_request, "foobar", {}, uuid4(), u)


def test_unread(dbsession: Session, user_id, test_request):
    """Get unread activity count."""

    with transaction.manager:
        u = dbsession.query(User).get(user_id)

        assert get_unread_activity_count(u) == 0
        object_id = uuid4()
        activity = create_activity(test_request, "foobar", {}, object_id, u)

        assert get_unread_activity_count(u) == 1

        mark_seen(u, object_id)
        assert get_unread_activity_count(u) == 0


