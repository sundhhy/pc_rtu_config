'''
这是配置modbus通信的界面
'''

import wx
from rtu_conf.CMM_serial import *
#from rtu_conf.modbus_master import *

from rtu_conf.Model.rtu_cfg import *
from rtu_conf.Model.command import *


MDB_PRIEX = '[MDB] '
class Panel_modbus(wx.Panel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent, pos=wx.DefaultPosition , size=wx.DefaultSize)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
        self.cmd_write_id = CMD_Write_id(rtu_cfg)

        bSizer2 = wx.BoxSizer(wx.HORIZONTAL)

        self.stxt_addr = wx.StaticText(self, wx.ID_ANY, u"地址", wx.DefaultPosition, wx.DefaultSize, 0)
        self.stxt_addr.Wrap(-1)
        self.stxt_addr.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INFOTEXT))
        self.stxt_addr.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        bSizer2.Add(self.stxt_addr, 0, wx.ALL, 5)


        self.txt_addr = wx.TextCtrl(self, wx.ID_ANY, u"1", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.txt_addr, 0, wx.ALL, 5)

        self.btn_rd_addr = wx.Button(self, 1, u"读取", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.btn_rd_addr, 0, wx.ALL, 5)

        self.btn_wr_addr = wx.Button(self, wx.ID_ANY, u"写入", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.btn_wr_addr, 0, wx.ALL, 5)

        self.SetSizer(bSizer2)
        self.Layout()

        self.Centre(wx.BOTH)

        # 对事件进行绑定
        self.Bind(wx.EVT_BUTTON, self.read_id, self.btn_rd_addr)
        self.Bind(wx.EVT_BUTTON, self.write_id, self.btn_wr_addr)
        self.com = parent.com



    def update(self, data):
        print(type(data))
        print('[mdb rx] ' + data.decode() + '\n')
        self.focus_text.SetLabel(data.decode())
        pass

    def read_id(self, event):
        print("{} read_id".format(MDB_PRIEX))

        self.focus_text = self.txt_addr

        #pdu = Read_reg_1(1, 0, 1)

        #self.com.send_bytes(pdu)

    def write_id(self, event):
        value = self.txt_addr.GetValue()

        if not value.isdigit():
            return
        print(value)

        self.cmd_write_id.excute(value)

        #self.com.send_bytes(bytes(value, encoding="utf8"))
        self.focus_text = self.txt_addr

    def exit(self):
        self.com.exit()
