from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from tzlocal import get_localzone


def get_environment_description() -> str:
    import platform

    return f"{platform.node()} ({platform.platform()} @ {platform.processor()};{platform.python_implementation()} {platform.python_build()[0]})"


def get_local_timezone():
    try:
        return ZoneInfo(str(get_localzone()))
    except Exception:
        return ZoneInfo("UTC")


def get_local_time():
    return datetime.now(get_local_timezone()).isoformat()
