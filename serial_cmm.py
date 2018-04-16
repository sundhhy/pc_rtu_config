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

class MyFrame(wx.Frame):

    def __init__(self,parent):




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

        self.com = None
        t = threading.Timer(0.1, self.myreceive)
        t.start()

    '''
     print("MyFrame __init__")
        plist = list(serial.tools.list_ports.comports())
        print(type(plist))
        print(plist)
        if len(plist) <= 0:
            print("没有发现端口!")
        else:
            plist_0 = list(plist[0])
            serialName = plist_0[0]
            #serialFd = serial.Serial(serialName, 9600, timeout=60)
            print("可用端口名>>>", serialName)

        wx.Frame.__init__(self,parent,-1,'EBB COM',size=(500,500))#窗口标题栏和大小

        panel=wx.Panel(self)
        sizer=wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(sizer)

        self.sendtxt=wx.StaticText(panel,-1,u'发送',(20,50),(50,15))#发送静态文本框 
        self.rectxt=wx.StaticText(panel,-1,u'接收',(20,200),(50,15))#接收静态文本框
        self.baudratetxt=wx.StaticText(panel,-1,u'波特率',(20,320),(50,15))#波特率静态文本框
        self.comtxt=wx.StaticText(panel,-1,'com',(20,350),(50,15))#com口静态文本框
        baudratelist=['300','600','1200','2400','4800','9600','19200','38400'
                     ,'43000','56000','57600','115200']

        comlist = []
        for list_ in plist:
            available_com = list_[0]
            comlist.append(available_com)

        self.baudratelistctr=wx.Choice(panel, -1, (70, 320), choices=baudratelist)
        self.Bind(wx.EVT_CHOICE,self.OnbaudrateCH,self.baudratelistctr)#波特率下拉列表响应函数
        self.comlistctr=wx.Choice(panel, -1, (70, 350), choices=comlist)
        self.Bind(wx.EVT_CHOICE,self.OncomlistCH,self.comlistctr)#com下拉列表响应函数
        self.baudratelistctr.SetSelection(11)
        self.comlistctr.SetSelection(0)
        self.sendctr = wx.TextCtrl(panel, -1,              
                    pos = (100, 50), size = (200, 100),
                    style=wx.TE_MULTILINE|wx.TE_CENTER)
        self.recctr = wx.TextCtrl(panel, -1,              
                    pos = (100, 200), size = (300, 100),
                    style=wx.TE_MULTILINE|wx.TE_CENTER)
        
        self.sendbutton=wx.Button(panel,-1,u'发送',pos=(350,50))#发送按钮
        self.Bind(wx.EVT_BUTTON,self.OnSend,self.sendbutton)
        self.ClearRecbutton=wx.Button(panel,-1,u'清空接收列表',pos=(350,200))
        self.Bind(wx.EVT_BUTTON,self.OnClearRec,self.ClearRecbutton)
       
        index=self.baudratelistctr.GetSelection()
        BaudRate=self.baudratelistctr.GetString(index)#获取波特率
        index=self.comlistctr.GetSelection()
        #index = 1
        ComNum=self.comlistctr.GetString(index)#获取com口
        t = threading.Timer(0.1,self.myreceive)
        t.start()
        self.Centre()
        global mycom
    
        try:  
            mycom= serial.Serial(ComNum,BaudRate,timeout=1)
                
        except:
            wx.MessageBox('open com fail','error')
            return None
    
    '''

        

        
        
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


class MyApp(wx.App): #自定义应用程序对象

    def OnInit(self):
        print("MyApp OnInit")
        self.frame = MyFrame(None)
        id=self.frame.GetId()
        print("Frame ID:",id)
        self.frame.Show(True)
        return True
    def OnExit(self):
        print("MyApp OnExit")
        
        #mycom.close()
        
        time.sleep(2)        



if __name__ == '__main__': 
    print("Main start")
    
    app = MyApp() #使用从wx.App继承的子类
    print("Before MainLoop")
    app.MainLoop()
    print("After MainLoop")