

'''
顶层的界面
其中的pannel可以切换，实现不同的界面切换效果
'''


#from rtu_conf.UI_select_memu import *


from rtu_conf.exchange import *
from rtu_conf.frame_id import *


import wx

import UI_select_memu

from rtu_conf.CMM_serial import *
from rtu_conf.UI_panel_home import *
from rtu_conf.UI_panel_modbus import *


class Frame_top(wx.Frame):
    def __init__(self):








        #wx.Frame.__init__(self, None, wx.ID_ANY, 'EBB COM', (800, 800))  # 窗口标题栏和大小
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          "Panel Switcher Tutorial")
        self.select_nemu = UI_select_memu.Select_item(self)
        self.com = cmm_manager()



        self.panel_home = Panel_home(self)
        self.panel_modbus = Panel_modbus(self)

        self.panel_modbus.Hide()

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.panel_home, 1, wx.EXPAND)
        self.sizer.Add(self.panel_modbus, 1, wx.EXPAND)
        self.SetSizer(self.sizer)



        self.cur_panel = self.panel_home

    def switch_hmi(self, id):
        print("switch_hmi : {}".format(id))
        if id == FRAME_ROOT:
            self.panel_modbus.Hide()
            self.panel_home.Show()
            self.cur_panel = self.panel_home

        if id == FRAME_MODBUS:
            if not self.com.Ser.is_open:
                dlg = wx.MessageDialog(self, "请先打开串口.", "错误", wx.OK)  # 语法是(self, 内容, 标题, ID)
                dlg.ShowModal()  # 显示对话框
                dlg.Destroy()  # 当结束之后关闭对话框
                return
            self.panel_home.Hide()
            self.panel_modbus.Show()
            self.cur_panel = self.panel_modbus

        self.Layout()

    def recv_bytes(self, data):
        self.cur_panel.update(data)

    def exit(self):
        self.panel_home.exit()