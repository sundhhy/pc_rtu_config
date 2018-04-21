'''
这个界面上都是MODBU的一些参数的配置
'''


import wx



from rtu_conf.CMM_serial import *
from rtu_conf.exchange import *
from rtu_conf.UI_select_memu import *



class Fram_cfg_modbus(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, '配置Modbus', size=(600, 600))  # 窗口标题栏和大小

        self.select_nemu = Select_item(self)

