# -*- coding: utf-8 -*-

import os
import time
from itertools import izip_longest
from datetime import datetime
from cromlech.marshallers import PickleMarshaller
from .utils import assert_sessions_folder


class RedisSession(object):
    """ Files based HTTP session.
    """

    def __init__(self, redis, delta, prefix='session:',
                 marshaller=PickleMarshaller):
        self.delta = delta  # timedelta in seconds.
        self.redis = redis
        self.marshaller = marshaller
        self.prefix = prefix

    def __iter__(self):

        def batcher(iterable, n):
            args = [iter(iterable)] * n
            return izip_longest(*args)

        for key in batcher(self.redis.scan_iter('%s*' % self;prefix), 100):
            yield key

    def new(self):
        return {}

    def get(self, sid):
        key = self.prefix + sid
        data = self.redis.get(key)
        session = self.marshaller.loads(data)
        if session is None:
            return self.new()
        return session

    def set(self, sid, session):
        key = self.prefix + sid
        assert isinstance(session, dict)
        data = self.marshaller.dump(session, session_path)
        self.redis.setex(key, data, self.delta)
        
    def clear(self, sid):
        key = self.prefix + sid
        self.redis.delete(key)

    def flush_expired_sessions(self):
        """We don't need this method, since redis has a builtin expiration.
        """
        raise NotImplementedError
