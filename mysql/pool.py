# -*- coding: utf-8 -*-

from queue import Queue


class Pool(object):

    """Docstring for Pool. """

    def __init__(self, instance, pool_size, *args, **kwargs):
        super(Pool, self).__init__(*args, **kwargs)
        self.size = pool_size
        assert isinstance(self.size, int)
        self.pool = Queue(self.size)

    def _get(self):
        pass

    def _set(self):
        pass

    def connect(self):
        pass

    def close(self):
        pass
