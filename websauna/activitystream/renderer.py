"""Render activity message in different formats."""
from pyramid.interfaces import IRequest
from pyramid.registry import Registry
from websauna.system.http import Request
from zope.interface import implementer

from .models import Activity
from .interfaces import IActivityRenderer, IActivity, NoRendererRegistered


@implementer(IActivityRenderer)
class DefaultActivityRenderer:

    def __init__(self, activity: Activity):
        self.activity = activity

    def render_title(self, request, channel_name) -> str:
        raise NotImplementedError()

    def render_html_body(self, request, channel_name) -> str:
        raise NotImplementedError()

    def render_link(self, request, channel_name) -> str:
        raise NotImplementedError()


def get_activity_renderer(request: Request, a: Activity) -> DefaultActivityRenderer:
    renderer = request.registry.queryAdapter(a, interface=IActivityRenderer, name=a.msg_id)
    if not renderer:
        raise NoRendererRegistered("No activity renderer registered for {}".format(a.msg_id))

    return renderer


def register_activity_renderer(registry: Registry, cls: type, name: str):
    registry.registerAdapter(factory=cls, required=(IActivity,), provided=IActivityRenderer, name=name)