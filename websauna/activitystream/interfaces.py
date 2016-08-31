from zope.interface import Interface


class IActivity(Interface):
    """Marker interface for Activity classes."""


class IActivityRenderer(Interface):
    """Interface to register different renderers"""

    def render_title() -> str:
        pass


    def render_html_body() -> str:
        pass


class IPushChannelProvider(Interface):
    """A factory function that returns list of Channel instances for push messages."""


class NoRendererRegistered(Exception):
    pass