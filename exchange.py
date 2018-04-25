'''
发布订阅模式
用于串口线程和GUI线程间通讯
任何有send方法的类都可以作为task
'''

from contextlib import contextmanager
from collections import defaultdict

EXC_TYPE_COM    = 0

class Exchange:
    def __init__(self):
        self._subscribers = set()

    def attach(self, task):
        self._subscribers.add(task)

    def detach(self,task):
        self._subscribers.remove(task)

    def subscribe(self, *tasks):
        for task in tasks:
            self.attach(task)
        try:
            yield
        finally:
            for task in tasks:
                self.detach(task)

    def send(self, type=0, msg=None):
        for subcriber in self._subscribers:
            subcriber.send(type, msg)


_exchanges = defaultdict(Exchange)

def get_exchange(name):
    return _exchanges[name]