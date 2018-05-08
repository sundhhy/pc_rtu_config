'''
这是配置modbus通信的界面
在进入本界面的时候，串口接收线程关闭。
'''

import wx
from rtu_conf.CMM_serial import *

from rtu_conf.control.command import *
from rtu_conf.UI.data_item import *



MDB_PRIEX = '[MDB] '
class Panel_modbus(wx.Panel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""

        self.control = parent.control
        self.cmd_write_id = CMD_Write_id(self.control)
        self.cmd_read_id = CMD_Read_id(self.control)
        self.cmd_read_cfg1 = CMD_Read_cfg1(self.control)

        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(800, 300),
                          style=wx.TAB_TRAVERSAL)
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        fgSizer1 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer1.SetFlexibleDirection(wx.BOTH)
        fgSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

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

        fgSizer1.Add(bSizer2, 1, wx.EXPAND, 5)

        bSizer3 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText2 = wx.StaticText(self, wx.ID_ANY, u"配置1", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)
        bSizer3.Add(self.m_staticText2, 0, wx.ALL, 5)

        self.txt_cfg_1 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer3.Add(self.txt_cfg_1, 0, wx.ALL, 5)

        self.btn_rd_cfg1 = wx.Button(self, wx.ID_ANY, u"读取", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer3.Add(self.btn_rd_cfg1, 0, wx.ALL, 5)

        self.btn_wr_cfg1 = wx.Button(self, wx.ID_ANY, u"写入", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer3.Add(self.btn_wr_cfg1, 0, wx.ALL, 5)

        fgSizer1.Add(bSizer3, 1, wx.EXPAND, 5)

        self.SetSizer(fgSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        # 对事件进行绑定
        self.Bind(wx.EVT_BUTTON, self.read_id, self.btn_rd_addr)
        self.Bind(wx.EVT_BUTTON, self.write_id, self.btn_wr_addr)

        self.Bind(wx.EVT_BUTTON, self.read_cfg1, self.btn_rd_cfg1)
        self.Bind(wx.EVT_BUTTON, self.write_cfg1, self.btn_wr_cfg1)

        self.com = parent.com

    def enter(self):
        self.com.exit()

    def update(self, data_item=None, data=None):
        if data_item == UI_data.time_out:
            print("time_out")
            return


        print(type(data))
        #print('[mdb rx] ' + data[0].decode() + '\n')
        print(str(data))
        self.focus_text.SetLabel(str(data))
        pass

    def read_id(self, event):
        print("{} read_id".format(MDB_PRIEX))

        self.focus_text = self.txt_addr
        self.focus_text = self.txt_addr
        self.cmd_read_id.excute()


    def write_id(self, event):
        value = self.txt_addr.GetValue()

        if not value.isdigit():
            return
        print(value)
        self.focus_text = self.txt_addr
        self.cmd_write_id.excute(bytes(value, encoding="utf8"))

    def read_cfg1(self, event):
        self.focus_text = self.txt_cfg_1
        self.cmd_read_cfg1.excute()
        pass

    def write_cfg1(self, event):
        pass

    def exit(self):
        self.com.exit()
