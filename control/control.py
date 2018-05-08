'''
模型和视图的中介模块
模型如果发生了更新，通过观察者模式来通知控制器


'''

from rtu_conf.control.command import *
from rtu_conf.UI.data_item import *
from rtu_conf.UI.frame_top import *
class Control():

    def __init__(self):
        self.model = rtu_cfg
        self.model.attach(self)


    def set_view(self, view):
        self.view = view

    def set_com(self, com):
        rtu_cfg.set_com(com)

    def get_id(self):
        return self.model.read_id()

    def set_id(self, new_id):
        self.model.write_id(new_id)

    def read_cfg1(self):
        self.model.read_cfg1()
        pass

    def notify(self, *msg):
        type, *data = msg
        self.view.update(mdl_to_view_data_item(type), data)


def mdl_to_view_data_item(mdl_type):
    return {
        MDL_NOTIFY_ID:UI_data.address,
        MDL_NOTIFY_CFG1:UI_data.cfg1,
        MDL_TIME_OUT:UI_data.time_out,
    }[mdl_type]

