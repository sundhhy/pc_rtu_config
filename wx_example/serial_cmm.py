import wx
import serial
import serial.tools.list_ports
import time
import threading


def SER_Get_available_com_name():
    plist = list(serial.tools.list_ports.comports())
    name_list = []
    for list_ in plist:
        available_com = list_[0]
        name_list.append(available_com)

    return name_list

class serial_comm():
    serial_instance = None

    def open_ser(self, com, baud):
        print(com)
        try:
            serial_instance = serial.Serial(com, baud, timeout=1)
        except:
            serial_instance = None

            raise

    def close_ser(self, com):
        serial_instance.close()
        return


class MyFrame(wx.Frame):

    def __init__(self,parent, serial_comm):

        self.ser_state = 0
        self.com = serial_comm

        wx.Frame.__init__(self, parent, -1, 'EBB COM', size=(1600, 1600))  # 窗口标题栏和大小


        list_com_name = SER_Get_available_com_name()
        list_baud = ['300', '600', '1200', '2400', '4800', '9600', '19200', '38400'
            , '43000', '56000', '57600', '115200']



        #串口操作的部分

        self.baudratelistctr = wx.Choice(self, -1, choices=list_baud)
        #self.Bind(wx.EVT_CHOICE, self.OnbaudrateCH, self.baudratelistctr)  # 波特率下拉列表响应函数
        self.baudratelistctr.SetSelection(11)
        self.comlistctr = wx.Choice(self, -1, choices=list_com_name)
        #self.Bind(wx.EVT_CHOICE, self.OncomlistCH, self.comlistctr)  # com下拉列表响应函数
        self.comlistctr.SetSelection(0)
        self.switch_btn = wx.Button(self, -1, u'打开')  # 发送按钮

        sizer_serial = wx.BoxSizer(wx.VERTICAL)
        sizer_serial.Add(self.comlistctr, 1, wx.EXPAND)       #wx.GROW, wx.EXPAND or wx.SHAPED
        sizer_serial.Add( self.baudratelistctr, 1, wx.EXPAND)
        sizer_serial.Add(self.switch_btn, 1, wx.EXPAND)

        self.Bind(wx.EVT_BUTTON, self.switch_btn_click, self.switch_btn)

        #数据发送部分
        self.send_btn = wx.Button(self, -1, u'发送')  # 发送按钮
        self.sendctr = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        sizer_send = wx.BoxSizer(wx.HORIZONTAL)
        sizer_send.Add(self.send_btn, 0, wx.EXPAND)
        sizer_send.Add(self.sendctr, 1, wx.GROW)



        #数据接收显示
        self.recctr = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_CENTER)

        sizer = wx.GridBagSizer(1, 4)
        sizer.Add(sizer_serial, (0, 0), wx.DefaultSpan, wx.ALIGN_LEFT)
        sizer.Add(self.recctr, (0, 1), wx.DefaultSpan, wx.EXPAND)

        sizer.Add(sizer_send, (1, 1), (2,1), wx.GROW)


        sizer.AddGrowableRow(0)
        sizer.AddGrowableCol(1)

        #sizer.AddGrowableRow(1)
        #sizer.AddGrowableCol(1)
        self.SetSizerAndFit(sizer)
        self.Centre()

        t = threading.Timer(0.1, self.myreceive)
        t.start()



    def switch_btn_click(self, event):
        # 打开串口
        # 打开按钮的文字替换成关闭
        if self.ser_state == 0:
            index = self.comlistctr.GetSelection()
            ComNum = self.comlistctr.GetString(index)  # 获取com口
            index = self.baudratelistctr.GetSelection()
            BaudRate = self.baudratelistctr.GetString(index)  # 获取波特率

            try:
                self.com.open_ser(ComNum, BaudRate)
                self.ser_state = 1
                event.GetEventObject().SetLabel("关闭")
            except:
                wx.MessageBox('open com fail', 'error')

        else:
            try:
                self.com.close_ser(ComNum)
                self.ser_state = 0
                event.GetEventObject().SetLabel("打开")
            except:
                wx.MessageBox('close com fail', 'error')



    def myreceive(self):

        if not self.com:
            time.sleep(1)
            t = threading.Timer(0.1, self.myreceive)
            t.start()
            return

        try:
            n=self.com.inWaiting()
            print(n)
        except:
            return None
        if n!=0:
            str1=self.com.read(n)
            print(str1)
            self.recctr.Value=str1
        t = threading.Timer(0.1,self.myreceive)
        t.start()
    def OnClearRec(self,event):
        self.recctr.Value=''
    
    def OnbaudrateCH(self,event):
        global mycom
        index=self.baudratelistctr.GetSelection()
        BaudRate=self.baudratelistctr.GetString(index)#获取波特率
        mycom.setBaudrate(BaudRate)
        print(mycom.inWaiting)               
    def OncomlistCH(self,event):
        global mycom
        index=self.comlistctr.GetSelection()
        ComNum=self.comlistctr.GetString(index)#获取com口
        
        try:
            mycom.setPort(ComNum)
        except:
            wx.MessageBox('change port fail','error')
            return None
        print(mycom.inWaiting)
    def OnSend(self,event):                    #发送处理程序
        value=self.sendctr.GetValue()
        print(value)
        n=mycom.write(bytes(value, encoding = "utf8") )


class main_app(wx.App): #自定义应用程序对象
    ser = serial_comm()
    def OnInit(self):
        print("main_app OnInit")
        print(type(self.ser))
        self.frame = MyFrame(None, self.ser)
        id=self.frame.GetId()
        print("Frame ID:",id)
        self.frame.Show(True)
        return True
    def OnExit(self):
        print("main_app OnExit")
        
        #mycom.close()
        
        time.sleep(2)        



if __name__ == '__main__': 
    print("Main start")
    
    app = main_app() #使用从wx.App继承的子类
    print("Before MainLoop")
    app.MainLoop()
    print("After MainLoop")