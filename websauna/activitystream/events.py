

class ActivityEvent:

    def __init__(self, request, activity):
        self.request = request
        self.activity = activity


class ActivityCreated(ActivityEvent):
    pass


class ActivitySeen(ActivityEvent):
    pass