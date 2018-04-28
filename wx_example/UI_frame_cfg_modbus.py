'''
这个界面上都是MODBU的一些参数的配置
'''


import wx



from rtu_conf.CMM_serial import *
from rtu_conf.exchange import *
from rtu_conf.UI_select_memu import *


MDB_PRIEX = '[MDB] '

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

        #wx.Frame.__init__(self, None, -1, '配置Modbus', size=(600, 600))  # 窗口标题栏和大小
        wx.Frame.__init__(self, root, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(500, 300), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.root = root
        self.com = root.com
        self.select_nemu = Select_item(self)
        ##wxbuild创建的界面部分
        self.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer2 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText2 = wx.StaticText(self, wx.ID_ANY, u"ID", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)
        self.m_staticText2.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INFOTEXT))
        #self.m_staticText2.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWFRAME))
        bSizer2.Add(self.m_staticText2, 0, wx.ALL, 5)

        self.m_textCtrl2 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.m_textCtrl2, 0, wx.ALL, 5)

        self.m_button2 = wx.Button(self, wx.ID_ANY, u"读取", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.m_button2, 0, wx.ALL, 5)


        self.m_button3 = wx.Button(self, wx.ID_ANY, u"配置", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.m_button3, 0, wx.ALL, 5)


        #对事件进行绑定
        self.Bind(wx.EVT_BUTTON, self.read_id, self.m_button2)
        self.Bind(wx.EVT_BUTTON, self.write_id, self.m_button3)

        self.SetSizer(bSizer2)
        self.Layout()

        self.Centre(wx.BOTH)





        if not self.root.com.Ser.is_open:
            dlg = wx.MessageDialog(self, "请先打开串口.", "配置Modbus", wx.OK)  # 语法是(self, 内容, 标题, ID)
            dlg.ShowModal()  # 显示对话框
            dlg.Destroy()  # 当结束之后关闭对话框

    def recv_bytes(self, data):
        print('[rx] ' + data.decode() + '\n')
        self.focus_text.SetLabel(data.decode())
        pass

    def read_id(self, event):
        print("{} read_id".format(MDB_PRIEX))
        self.focus_text = self.m_textCtrl2
        self.com.send_bytes(b'read id')

    def write_id(self, event):
        print("{} write_id".format(MDB_PRIEX))
        self.focus_text = self.m_textCtrl2
        self.com.send_bytes(b'write_id')

    def exit(self):
        self.com.exit()

