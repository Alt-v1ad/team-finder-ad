PROJECT_NAME_MAX_LEN = 200
PROJECT_STATUS_MAX_LEN = 6
PAGINATION_LIMIT = 12


class ProjectStatus:
    OPEN = "open"
    CLOSED = "closed"
    CHOICES = [
        (OPEN, "Open"),
        (CLOSED, "Closed"),
    ]
