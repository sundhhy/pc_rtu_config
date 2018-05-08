'''
实现：
响应外部的配置命令
配置的数据通信处理

提供一个观察者模式
提供超时功能，在本实现中，依赖于pyserial的读超时
串口数据采用同步通信，发送了请求报文之后，直接等待接收
'''
from rtu_conf.exchange import *
from rtu_conf.modbus.modbus_master import *

MDL_NOTIFY_ID       =  0
MDL_NOTIFY_CFG1       =  1

MDL_TIME_OUT        = 2

class MDL_Publisher:
    def __init__(self):
        self._listOfUsers = []

    def attach(self, userObj):
        if userObj not in self._listOfUsers:
            self._listOfUsers.append(userObj)

    def detach(self, userObj):
        self._listOfUsers.remove(userObj)

    def notify(self, *msg):
        for objects in self._listOfUsers:
            objects.notify(*msg)




class Rtu_cfg(MDL_Publisher):
    def __init__(self):
        #self.exchange = get_exchange('cmm')
        #self.exchange.attach(self)
        self.mdb_id = 1
        super(Rtu_cfg, self).__init__()

    def set_com(self, com):
        self.com = com
    '''
    def send(self, exc_type, msg):
    if exc_type != EXC_TYPE_COM:
        return
    self.notify(self.cur_type, b'dddd')
    '''
    def write_id(self, wid):
        #self.com.send_bytes()
        self.mdb_id = wid
        self.notify(MDL_NOTIFY_ID, wid)


    def read_id(self):
        #self.com.send_bytes(b'read_id')
        return self.mdb_id

    def read_cfg1(self):
        self.cur_type = MDL_NOTIFY_CFG1
        pkt = Read_reg_4(self.mdb_id, 0, 1)
        self.com.send_bytes(pkt)

        resp = self.com.read_frame(1, 0)
        print(resp)
        if resp:
            try:
                d = decode_modbus_response(resp, self.mdb_id)
            except:
                self.notify(MDL_NOTIFY_CFG1, b'error')
                return
            self.notify(MDL_NOTIFY_CFG1, d[0])
        else:
            self.notify(MDL_TIME_OUT, None)





global rtu_cfgd

rtu_cfg = Rtu_cfg()

if __name__ == '__main__':
    print("cmm start")