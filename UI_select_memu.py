'''
这是每个界面上都会有的一个用于切换配置界面的菜单。
所以独立出来，让每个界面都可以使用

'''


import wx


#from rtu_conf.UI_frame_factory import FRAME_ROOT, FRAME_MODBUS, Get_frame
import UI_frame_factory
from rtu_conf.frame_id import *

from rtu_conf.exchange import *
# 切换到其他界面


switch_hdl = None

class Select_item:
    global switch_hdl
    def __init__(self, parent_ui):
        self.parent_ui = parent_ui

        self.exchange = get_exchange('cmm')
        parent_ui.CreateStatusBar()  # 创建位于窗口的底部的状态栏，会显示菜单中的helpString
        conf_item_menu = wx.Menu()


        menu_item_1 = conf_item_menu.Append(wx.ID_ABOUT, "Modbus配置", \
                                          " Modbus的参数配置")  # (ID, 项目名称, 状态栏信息)

        menu_return = conf_item_menu.Append(wx.ID_HOME, "返回", \
                                          "返回到主菜单")  # (ID, 项目名称, 状态栏信息)
        conf_item_menu.AppendSeparator()

        # 创建菜单栏
        menuBar = wx.MenuBar()
        menuBar.Append(conf_item_menu, "配置菜单")  # 在菜单栏中添加filemenu菜单
        self.parent_ui.SetMenuBar(menuBar)  # 在frame中添加菜单栏

        # 设置events
        self.parent_ui.Bind(wx.EVT_MENU, self.on_modbus, menu_item_1)
        self.parent_ui.Bind(wx.EVT_MENU, self.on_return, menu_return)

        return

    def switch_frame(self, frame_id):
        print('switch {}'.format(frame_id))
        f = UI_frame_factory.Get_frame(frame_id)

        if f:
            self.parent_ui.Show(False)
            self.exchange.send(1, frame_id)
            f.Show()


    def on_modbus(self, e):
        # 创建一个带"OK"按钮的对话框。wx.OK是wxWidgets提供的标准ID
        '''

        dlg = wx.MessageDialog(self.parent_ui, "A small text editor.", \
            "About Sample Editor", wx.OK)    # 语法是(self, 内容, 标题, ID)
        dlg.ShowModal()    # 显示对话框
        dlg.Destroy()    # 当结束之后关闭对话框
        '''
        self.switch_frame(UI_frame_factory.FRAME_MODBUS)

    def on_return(self, e):
        # 创建一个带"OK"按钮的对话框。wx.OK是wxWidgets提供的标准ID

        '''

        dlg = wx.MessageDialog(self.parent_ui, "A small text editor.", \
            "返回", wx.OK)    # 语法是(self, 内容, 标题, ID)
        dlg.ShowModal()    # 显示对话框
        dlg.Destroy()    # 当结束之后关闭对话框
        :param e:
        :return:
        '''
        self.switch_frame(UI_frame_factory.FRAME_ROOT)






