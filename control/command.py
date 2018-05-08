'''
对模型配置的各种命令
负责将视图中获取到 数据转化成模型能够处理的数据类型
'''
from rtu_conf.Model.rtu_cfg import *

class ICommand():
    def __init__(self, rhs):
        self.rcv = rhs

    def excute(self, *arg):
        pass

class CMD_Write_id(ICommand):
    def excute(self, *arg):
        wr_id = arg[0]
        self.rcv.set_id(wr_id)

class CMD_Read_id(ICommand):
    def excute(self, *arg):
        self.rcv.get_id()


class CMD_Read_cfg1(ICommand):
    def excute(self, *arg):
        self.rcv.read_cfg1()