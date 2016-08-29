"""Populate template context for notification menu."""

from pyramid.events import BeforeRender
from websauna.activitystream.activity import get_unread_activity_count, get_last_unseen
from websauna.activitystream.web import render_web_notification

from .models import Stream


def get_activity_data(request):
    """Get template context data for notification menu."""

    if not request:
        return None

    user = request.user

    if not user:
        return None

    stream = Stream.get_or_create_user_stream(user)
    unread_count  = get_unread_activity_count(stream)
    last_unseen = get_last_unseen(stream)

    # Render notification items
    notifications = [render_web_notification(request, activity) for activity in last_unseen]

    view_all_link = request.route_url("notification_history")

    return dict(unread_count=unread_count, notifications=notifications, view_all_link=view_all_link)



def includeme(config):

    def on_before_render(event):
        # Augment Pyramid template renderers with these extra variables and deal with JS placement

        request = event["request"]
        event["get_activity_data"] = get_activity_data

    config.add_subscriber(on_before_render, BeforeRender)