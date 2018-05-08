import wx

from rtu_conf.CMM_serial import *

'''
这是主界面
包括串口的控制
'''

class Panel_home(wx.Panel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""

        self.ser_state = 0
        self.com = parent.com
        list_com_name = SER_Get_available_com_name()
        list_baud = ['300', '600', '1200', '2400', '4800', '9600', '19200', '38400'
            , '43000', '56000', '57600', '115200']

        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(500, 300),
                          style=wx.TAB_TRAVERSAL)



        #wxFormBuilder
        sz_top = wx.BoxSizer(wx.HORIZONTAL)

        sz_items = wx.BoxSizer(wx.VERTICAL)

        sz_com = wx.BoxSizer(wx.HORIZONTAL)

        chc_comChoices = list_com_name
        self.chc_com = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, chc_comChoices, 0)
        self.chc_com.SetSelection(0)
        sz_com.Add(self.chc_com, 0, wx.ALL, 5)

        chc_baudChoices = list_baud
        self.chc_baud = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, chc_baudChoices, 0)
        self.chc_baud.SetSelection(0)
        sz_com.Add(self.chc_baud, 0, wx.ALL, 5)

        self.btn_switch = wx.Button(self, wx.ID_ANY, u"打开", wx.DefaultPosition, wx.DefaultSize, 0)
        sz_com.Add(self.btn_switch, 0, wx.ALL, 5)

        sz_items.Add(sz_com, 1, wx.EXPAND, 5)

        sz_send = wx.BoxSizer(wx.HORIZONTAL)

        self.btn_send = wx.Button(self, wx.ID_ANY, u"发送", wx.DefaultPosition, wx.DefaultSize, 0)
        sz_send.Add(self.btn_send, 0, wx.ALL, 5)

        self.txt_send = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        sz_send.Add(self.txt_send, 0, wx.ALL, 5)

        sz_items.Add(sz_send, 1, wx.SHAPED, 5)

        #sz_items.Add((0, 0), 1, wx.EXPAND, 5)

        sz_top.Add(sz_items, 1, wx.ALL, 5)

        self.txt_serial_data = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(100, 100),
                                           wx.TE_MULTILINE)
        self.txt_serial_data.SetToolTip(u"串口数据")

        sz_top.Add(self.txt_serial_data, 0, wx.ALL|wx.EXPAND, 10)

        self.SetSizer(sz_top)
        self.Layout()
        #事件
        self.Bind(wx.EVT_CHOICE, self.com_click, self.chc_com)  # com下拉列表响应函数
        self.Bind(wx.EVT_CHOICE, self.baud_click, self.chc_baud)  # 波特率下拉列表响应函数
        self.Bind(wx.EVT_BUTTON, self.switch_btn_click, self.btn_switch)
        self.Bind(wx.EVT_BUTTON, self.send_click, self.btn_send)

        self.com.start_thread()

    def enter(self):
        self.com.start_thread()

    def update(self, data_item=None, data=None):
        self.txt_serial_data.AppendText('[rx] ' + data.decode() + '\n')

    def switch_btn_click(self, event):
        # 打开串口
        # 打开按钮的文字替换成关闭
        port_index = self.chc_com.GetSelection()
        ComNum = self.chc_com.GetString(port_index)  # 获取com口
        if self.ser_state == 0:
            index = self.chc_baud.GetSelection()
            BaudRate = self.chc_baud.GetString(index)  # 获取波特率

            try:
                self.com.open(str(port_index), ComNum, BaudRate)
                event.GetEventObject().SetLabel("关闭")
                self.ser_state = 1
            except:
                wx.MessageBox('open com fail', 'error')

        else:
            try:
                self.com.close(ComNum)
                self.ser_state = 0
                event.GetEventObject().SetLabel("打开")
            except:
                wx.MessageBox('close com fail', 'error')

    def OnClearRec(self, event):
        print('OnClearRec')
        # self.recctr.Value = ''

    def baud_click(self, event):
        index = self.chc_baud.GetSelection()
        BaudRate = self.chc_baud.GetString(index)  # 获取波特率
        self.com.set_baud(BaudRate)

    def com_click(self, event):
        index = self.chc_com.GetSelection()
        ComNum = self.chc_com.GetString(index)  # 获取com口

        self.com.change_port(ComNum)

    def send_click(self, event):  # 发送处理程序
        value = self.txt_send.GetValue()
        print(value)
        self.com.send_bytes(bytes(value, encoding="utf8"))
        # n = mycom.write(bytes(value, encoding="utf8"))


    def exit(self):
        self.com.exit()