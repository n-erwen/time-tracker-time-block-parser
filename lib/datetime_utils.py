import datetime

DATETIME_DATE_FORMAT = '%Y-%m-%d'
DATETIME_TIME_FORMAT = '%H:%M'
DATETIME_ISO_FORMAT = "%Y-%m-%dT%H:%M:%S"


def get_datetime(date_str, time_str):
    try:
        return datetime.datetime.strptime(date_str + ' ' + time_str, DATETIME_DATE_FORMAT + ' ' + DATETIME_TIME_FORMAT)
    except ValueError:
        return None


def get_date_as_datetime(date):
    return datetime.datetime.combine(date, datetime.time(0, 0, 0))


def get_timedelta_as_hours(timedelta):
    return timedelta.seconds/3600


def get_timedelta_as_minutes(timedelta):
    return timedelta.seconds/60


def get_timedelta_as_string(timedelta):
    hours = int(get_timedelta_as_hours(timedelta))
    minutes = int(get_timedelta_as_minutes(timedelta)) - (hours*60)
    return (
            (str(hours) + 'h' if hours > 0 else '')
            + (str(minutes) + 'm' if minutes > 0 or (minutes <= 0 and hours <= 0) else '')
    )
