from django_statsd.clients.statsd_proxy import StatsClientProxy

_statsd = None


def get_client():
    return StatsClientProxy()


if not _statsd:
    _statsd = get_client()

statsd = _statsd
