




#from rtu_conf.UI_select_memu import *


from rtu_conf.exchange import *



import wx
import UI_select_memu

from rtu_conf.CMM_serial import *




class Frame_root(wx.Frame):
    _instance = None
    __first_init = True
    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(Frame_root, cls).__new__(cls, *args, **kw)
        return cls._instance
    def __init__(self, parent):

        if not self.__first_init:
            return

        self.__first_init = False

        self.ser_state = 0
        self.com = cmm_manager()

        wx.Frame.__init__(self, parent, -1, 'EBB COM', size=(600, 600))  # 窗口标题栏和大小


        self.select_nemu = UI_select_memu.Select_item(self)

        list_com_name = SER_Get_available_com_name()
        list_baud = ['300', '600', '1200', '2400', '4800', '9600', '19200', '38400'
            , '43000', '56000', '57600', '115200']

        # 串口操作的部分

        self.baudratelistctr = wx.Choice(self, -1, choices=list_baud)
        self.Bind(wx.EVT_CHOICE, self.baud_click, self.baudratelistctr)  # 波特率下拉列表响应函数

        self.baudratelistctr.SetSelection(11)
        self.comlistctr = wx.Choice(self, -1, choices=list_com_name)
        self.Bind(wx.EVT_CHOICE, self.com_click, self.comlistctr)  # com下拉列表响应函数
        self.comlistctr.SetSelection(0)



        self.switch_btn = wx.Button(self, -1, u'打开')  # 发送按钮
        sizer_serial = wx.BoxSizer(wx.VERTICAL)
        sizer_serial.Add(self.comlistctr, 1, wx.EXPAND)  # wx.GROW, wx.EXPAND or wx.SHAPED
        sizer_serial.Add(self.baudratelistctr, 1, wx.EXPAND)
        sizer_serial.Add(self.switch_btn, 1, wx.EXPAND)
        self.Bind(wx.EVT_BUTTON, self.switch_btn_click, self.switch_btn)

        # 数据发送部分
        self.send_btn = wx.Button(self, -1, u'发送')  # 发送按钮
        self.sendctr = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        sizer_send = wx.BoxSizer(wx.HORIZONTAL)
        sizer_send.Add(self.send_btn, 0, wx.EXPAND)
        sizer_send.Add(self.sendctr, 1, wx.GROW)
        self.Bind(wx.EVT_BUTTON, self.send_click, self.send_btn)

        # 数据接收显示
        self.recctr = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_READONLY )

        sizer = wx.GridBagSizer(1, 4)
        sizer.Add(sizer_serial, (0, 0), wx.DefaultSpan, wx.ALIGN_LEFT)
        sizer.Add(self.recctr, (0, 1), wx.DefaultSpan, wx.EXPAND)

        sizer.Add(sizer_send, (1, 1), (2, 1), wx.GROW)

        sizer.AddGrowableRow(0)
        sizer.AddGrowableCol(1)

        # sizer.AddGrowableRow(1)
        # sizer.AddGrowableCol(1)
        self.SetSizerAndFit(sizer)
        self.Centre()

        self.com.start_thread()


    def recv_bytes(self, data):
        self.recctr.AppendText('[rx] ' + data.decode() + '\n')

    def switch_btn_click(self, event):
        # 打开串口
        # 打开按钮的文字替换成关闭
        port_index = self.comlistctr.GetSelection()
        ComNum = self.comlistctr.GetString(port_index)  # 获取com口
        if self.ser_state == 0:
            index = self.baudratelistctr.GetSelection()
            BaudRate = self.baudratelistctr.GetString(index)  # 获取波特率

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
        #self.recctr.Value = ''

    def baud_click(self, event):
        index = self.baudratelistctr.GetSelection()
        BaudRate = self.baudratelistctr.GetString(index)  # 获取波特率
        self.com.set_baud(BaudRate)

    def com_click(self, event):
        index = self.comlistctr.GetSelection()
        ComNum = self.comlistctr.GetString(index)  # 获取com口

        self.com.change_port(ComNum)


    def send_click(self, event):  # 发送处理程序
        value = self.sendctr.GetValue()
        print(value)
        self.com.send_bytes(bytes(value, encoding="utf8"))
        #n = mycom.write(bytes(value, encoding="utf8"))

    def exit(self):
        self.com.exit()