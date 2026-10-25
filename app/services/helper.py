from datetime import datetime, timezone


def time_ago(dt):
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    seconds = int((datetime.now(timezone.utc) - dt).total_seconds())
    minutes = seconds // 60
    hours = minutes // 60
    days = hours // 24

    if seconds < 60:
        return "just now"

    if minutes < 60:
        return f"{minutes} min ago"

    if hours < 24:
        return f"{hours} hr ago"

    return f"{days} day{'s' if days != 1 else ''} ago"
