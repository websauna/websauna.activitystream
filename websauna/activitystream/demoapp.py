import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as psql
from sqlalchemy import orm

import requests
from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPFound
from websauna.activitystream.activity import create_activity, mark_seen, mark_seen_by_user
from websauna.activitystream.events import ActivityCreated
from websauna.system.core import messages
from websauna.system.core.route import simple_route
from websauna.system.model.meta import Base

from .renderer import DefaultActivityRenderer, register_activity_renderer


class DemoMessageRenderer(DefaultActivityRenderer):

    def render_title(self, request, channel_name):
        text = self.activity.msg_context.get("text")
        text = text[0:32] + "..."
        return "{}!!".format(text)

    def render_html_body(self, request, channel_name):
        text = self.activity.msg_context.get("text")
        return "This is the full HTML text: <strong>{}</strong>".format(text)

    def render_link(self, request, channel_name):
        return request.route_url("view_demo_instance", id=self.activity.object_id)


class DemoModel(Base):
    """A simple model holding string content."""

    __tablename__ = "activitystream_demo"

    id = sa.Column(psql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()"), )

    text = sa.Column(sa.String(256))


@simple_route("/create-notification", route_name="create_notification")
def create_notification(request):

    if not request.user:
        messages.add(request, kind="error", msg="You need to be logged in")
        return HTTPFound(request.route_url("home"))

    # Create target object.
    resp = requests.get("https://baconipsum.com/api/?type=all-meat&paras=2&start-with-lorem=1")
    text = resp.json()[0][0:255]

    demo = DemoModel(text=text)
    request.dbsession.add(demo)
    request.dbsession.flush()

    # Create notification
    context = {"text": text}
    a = create_activity(request, "demo_msg", context, demo.id, request.user)
    request.registry.notify(ActivityCreated(request, a))

    messages.add(request, kind="info", msg="New demo object and notification created")
    return HTTPFound(request.route_url("home"))


@simple_route("/view-demo/{id}", route_name="view_demo_instance", renderer="testpage.html")
def view_demo_instance(request):
    id = request.matchdict["id"]
    demo = request.dbsession.query(DemoModel).get(id)
    mark_seen_by_user(request.user, demo.id)
    return locals()

