from django.conf import settings

try:
    from importlib import import_module
except ImportError:
    from django.utils.importlib import import_module


def get(name, default):
    try:
        return getattr(settings, name, default)
    except ImportError:
        return default


def setup_client():
    client = get('STATSD_CLIENT', 'statsd.client')
    host = get('STATSD_HOST', 'localhost')
    port = get('STATSD_PORT', 8125)
    prefix = get('STATSD_PREFIX', None)
    return import_module(client).StatsClient(host, port, prefix)


class StatsClientProxy(object):
    def __init__(self):
        self.client = setup_client()
        self.default_rate = get('STATSD_DEFAULT_RATE', 1)

    def timer(self, stat, rate=None):
        if rate is None:
            rate = self.default_rate
        return self.client.timer(stat, rate=rate)

    def timing(self, stat, delta, rate=None):
        if rate is None:
            rate = self.default_rate
        return self.client.timing(stat, delta, rate=rate)

    def incr(self, stat, count=1, rate=None):
        if rate is None:
            rate = self.default_rate
        return self.client.incr(stat, count, rate=rate)

    def decr(self, stat, count=1, rate=None):
        if rate is None:
            rate = self.default_rate
        return self.client.decr(stat, count, rate=rate)

    def gauge(self, stat, value, rate=None, delta=False):
        if rate is None:
            rate = self.default_rate
        return self.client.gauge(stat, value, rate=rate, delta=delta)

    def set(self, stat, value, rate=None):
        if rate is None:
            rate = self.default_rate
        return self.client.set(stat, value, rate=rate)

    def __getattr__(self, key):
        return getattr(self.client, key)
