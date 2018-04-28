'''
对模型配置的各种命令
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
        self.rcv.write_id(wr_id)
