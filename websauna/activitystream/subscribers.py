from pyramid.events import subscriber
from websauna.activitystream.channel import get_push_channels
from .events import ActivityCreated


@subscriber(ActivityCreated)
def push_notifications(e: ActivityCreated):
    """Multiplex new activity across all push channels."""

    activity = e.activity
    request = e.request

    channels = get_push_channels(request)
    for channel in channels:
        if channel.is_pushable(activity):
            channel.push_notification(activity)

