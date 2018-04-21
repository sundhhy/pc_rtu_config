'''

'''

#from rtu_conf.UI_cfg_modbus import *
#from rtu_conf.UI_frame_root import *
from rtu_conf.frame_id import *

import UI_cfg_modbus
import UI_frame_root

frame_root = None
#frame_cfg_modbus = None


def Get_frame(fid):
    global frame_root
    global frame_cfg_modbus

    if fid == FRAME_ROOT:
        if frame_root == None:
            frame_root = UI_frame_root.Frame_root(None)
        return frame_root

    if fid == FRAME_MODBUS:
        return UI_cfg_modbus.Fram_cfg_modbus(frame_root)



    return None