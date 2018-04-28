'''

'''

#from rtu_conf.UI_cfg_modbus import *
#from rtu_conf.UI_frame_root import *
from rtu_conf.frame_id import *

import UI_frame_cfg_modbus
import UI_frame_root




def Get_frame(fid):

    if fid == FRAME_ROOT:
        return UI_frame_root.Frame_root(None)

    if fid == FRAME_MODBUS:
        return UI_frame_cfg_modbus.Fram_cfg_modbus(UI_frame_root.Frame_root(None))



    return None