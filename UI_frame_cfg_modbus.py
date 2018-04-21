'''
这个界面上都是MODBU的一些参数的配置
'''


import wx



from rtu_conf.CMM_serial import *
from rtu_conf.exchange import *
from rtu_conf.UI_select_memu import *



class Fram_cfg_modbus(wx.Frame):
    _instance = None
    __first_init = True

    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(Fram_cfg_modbus, cls).__new__(cls, *args, **kw)
        return cls._instance


    def __init__(self, root):
        if not self.__first_init:
            return

        self.__first_init = False

        wx.Frame.__init__(self, root, -1, '配置Modbus', size=(600, 600))  # 窗口标题栏和大小
        self.root = root
        self.select_nemu = Select_item(self)





        if not self.root.com.Ser.is_open:
            dlg = wx.MessageDialog(self, "请先打开串口.", "配置Modbus", wx.OK)  # 语法是(self, 内容, 标题, ID)
            dlg.ShowModal()  # 显示对话框
            dlg.Destroy()  # 当结束之后关闭对话框

    def recv_bytes(self, data):
        #print('[rx] ' + data.decode() + '\n')
        pass


