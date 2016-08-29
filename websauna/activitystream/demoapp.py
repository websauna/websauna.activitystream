import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as psql
from sqlalchemy import orm

from pyramid.config import Configurator
from websauna.system.core.route import simple_route
from websauna.system.model.meta import Base

from .renderer import DefaultActivityRenderer, register_activity_renderer


class DemoMessageRenderer(DefaultActivityRenderer):

    def render_title(self, request, channel_name):
        return "This is a test notification {}!".format(self.activity.msg_context.get("param"))

    def render_html_body(self, request, channel_name):
        return "This is HTML formatted <strong>{}</strong>".format(self.activity.msg_context.get("param"))

    def render_link(self, request, channel_name):
        return request.route_url("view_demo", id=self.activity.object_id)


class DemoModel(Base):
    """A simple model holding string content."""

    __tablename__ = "activitystream_demo"

    id = sa.Column(psql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()"), )

    text = sa.Column(sa.String(256))


@simple_route("/view-demo/{id}")
def create_demo_instance(request):
    pass


@simple_route("/view-demo/{id}", route_name="view_demo")
def view_demo_instance(request):
    pass

