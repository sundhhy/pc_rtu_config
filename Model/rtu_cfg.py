'''
实现：
响应外部的配置命令
配置的数据通信处理



'''
from rtu_conf.exchange import *

class Rtu_cfg():
    def __init__(self):
        self.exchange = get_exchange('cmm')
        self.exchange.attach(self)

    def set_com(self, com):
        self.com = com

    def send(self, exc_type, msg):
        if exc_type != EXC_TYPE_COM:
            return

    def write_id(self, wid):
        self.com.send_bytes(bytes(wid, encoding="utf8"))



global rtu_cfg

rtu_cfg = Rtu_cfg()

if __name__ == '__main__':
    print("cmm start")