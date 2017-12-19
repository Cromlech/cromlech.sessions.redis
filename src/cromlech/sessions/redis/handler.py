# -*- coding: utf-8 -*-

from datetime import timedelta
from itertools import zip_longest
from cromlech.session import SessionHandler
from cromlech.marshallers import PickleMarshaller


class RedisSessionHandler(SessionHandler):
    """Redis based HTTP session.
    """

    def __init__(self, redis, delta, prefix='session:',
                 marshaller=PickleMarshaller):
        self.delta = delta  # timedelta in seconds.
        self.redis = redis
        self.marshaller = marshaller
        self.prefix = prefix

    def __iter__(self):
        for key in self.redis.scan_iter('%s*' % self.prefix):
            yield str(key[len(self.prefix):], 'utf-8')

    def get(self, sid):
        key = self.prefix + sid
        data = self.redis.get(key)
        if data is None:
            return self.new()
        session = self.marshaller.loads(data)            
        return session

    def set(self, sid, session):
        key = self.prefix + sid
        assert isinstance(session, dict)
        data = self.marshaller.dumps(session)
        self.redis.setex(key, timedelta(seconds=self.delta), data)

    def clear(self, sid):
        key = self.prefix + sid
        self.redis.delete(key)

    def touch(self, sid):
        key = self.prefix + sid
        self.redis.expire(key, timedelta(seconds=self.delta))

    def flush_expired_sessions(self):
        """We don't need this method, since redis has a builtin expiration.
        """
        raise NotImplementedError
