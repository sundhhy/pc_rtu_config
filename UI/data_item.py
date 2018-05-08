'''
这个文件提供了界面上需要显示的数据的类型枚举
用于与控制器之间通信时，指定数据
'''

from enum import Enum

class UI_data(Enum):
    error = 0,
    address = 1,
    cfg1 = 2,
    time_out = 3,
