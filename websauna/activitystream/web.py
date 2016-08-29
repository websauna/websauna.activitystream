"""Web notification menu."""
from pyramid.renderers import render
from websauna.activitystream.renderer import get_activity_renderer
from websauna.system.http import Request

from .models import Activity


def render_web_notification(request: Request, activity: Activity, template="templates/activitystream/notification.html") -> str:
    """Render a single notification item in notification menu."""

    name = "web"
    renderer = get_activity_renderer(request, activity)
    title = renderer.render_title(request, name)
    html_body = renderer.render_html_body(request, name)
    link = renderer.render_link(request, name)

    context = dict(title=title, html_body=html_body, link=link, activity=activity)

    return render(template, context, request=request)