from pyramid.httpexceptions import HTTPFound
from websauna.activitystream.web import render_web_notification
from websauna.system.core.route import simple_route

from .models import Stream
from .activity import get_all_activities


@simple_route("/notification-history", route_name="notification_history", renderer="activitystream/history.html")
def history(request):
    if not request.user:
        return HTTPFound(request.route_url("home"))

    stream = Stream.get_or_create_user_stream(request.user)
    activities = get_all_activities(stream)
    activities = [render_web_notification(request, a, template="activitystream/notification_full.html") for a in activities]

    return locals()




