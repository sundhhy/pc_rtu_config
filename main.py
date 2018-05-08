import wx

import time
import threading

from rtu_conf.CMM_serial import *
from rtu_conf.exchange import *

from rtu_conf.UI.frame_top import *
from rtu_conf.control.control import *





class main_app(wx.App):  # 自定义应用程序对象

    def OnInit(self):
        print("main_app OnInit")

        self.control = Control()
        self.frame = Frame_top(self.control)
        self.control.set_view(self.frame)

        self.exchange = get_exchange('cmm')
        self.exchange.attach(self)
        id = self.frame.GetId()
        print("Frame ID:", id)
        self.frame.Show(True)
        return True

    #使用send名字是因为exchanger的task接口必须是send
    def send(self, exc_type, msg):
        if exc_type == EXC_TYPE_COM:
            print(type(msg))
            print('[root] recv {}'.format(msg))
            self.frame.recv_bytes(msg)
            return

        '''
         if exc_type == 1:
            print('root change frame')
            self.frame.Show(False)
            self.frame = Get_frame(msg)
            self.frame.Show(True)
            return
        '''


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