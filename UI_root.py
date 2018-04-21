import wx

import time
import threading

from rtu_conf.CMM_serial import *
from rtu_conf.exchange import *

from rtu_conf.UI_frame_factory import *







class main_app(wx.App):  # 自定义应用程序对象

    def OnInit(self):
        print("main_app OnInit")
        self.frame = Get_frame(FRAME_ROOT)
        self.exchange = get_exchange('cmm')
        self.exchange.attach(self)
        id = self.frame.GetId()
        print("Frame ID:", id)
        self.frame.Show(True)
        return True

    #使用send名字是因为exchanger的task接口必须是send
    def send(self, type, msg):



        if type == 0:
            print('recv {}'.format(msg))
            self.frame.recv_bytes(msg)
            return

        if type == 1:
            self.frame = Get_frame(msg)
            return

        pass

    def OnExit(self):
        print("main_app OnExit")
        self.exchange.detach(self)
        self.frame.exit()
        time.sleep(1)

        return 0






if __name__ == '__main__':
    print("Main start")

    app = main_app()  # 使用从wx.App继承的子类
    app.MainLoop()
    print("After MainLoop")