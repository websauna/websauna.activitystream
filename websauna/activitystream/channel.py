from typing import List

from websauna.system.http import Request
from websauna.system.mail import send_templated_mail
from .models import Activity

from .renderer import get_activity_renderer


class Channel:
    """Abstract base class for all push notification channels."""


class Email(Channel):

    __name__ = "email"

    def __init__(self, request: Request):
        self.request = request

    def is_pushable(self, a: Activity):
        """Should this activity be pushed over this channel."""
        return True

    def push_notification(self, a: Activity):

        user = a.stream.user

        # No email configured
        if not user.email:
            return

        renderer = get_activity_renderer(self.request, a)
        title = renderer.render_title(self.request, self.__name__)
        html_body = renderer.render_html_body(self.request, self.__name__)
        link = renderer.render_link(self.request, self.__name__)

        send_templated_mail(self.request, [user.email], "activitystream/email/notification", context={title: title, html_body: html_body, link: link})


def get_push_channels(request: Request) -> List[Channel]:
    """Get all channels where a notification is pushed."""
    return [Email(request)]



