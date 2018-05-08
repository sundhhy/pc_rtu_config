'''
这个文件提供modbus报文的组包和报分的解析功能。


'''

import struct
from rtu_conf.modbus.modbus_utils import *
from rtu_conf.modbus.modbus_define import *



def Build_read_pkt(slave_addr, function_code, start_addr, num_reg):

    pdu = struct.pack(">BBHH",slave_addr, function_code, start_addr, num_reg)
    crc = calculate_crc(pdu)
    b_crc = struct.pack(">H", crc)
    return pdu + b_crc





def Read_reg_1(salve_id, start_addr, num_reg):
    return Build_read_pkt(salve_id, READ_COILS, start_addr, num_reg)

def Read_reg_2(salve_id, start_addr, num_reg):
    return Build_read_pkt(salve_id, READ_DISCRETE_INPUTS, start_addr, num_reg)

def Read_reg_3(salve_id, start_addr, num_reg):
    return Build_read_pkt(salve_id, READ_HOLDING_REGISTERS, start_addr, num_reg)

def Read_reg_4(salve_id, start_addr, num_reg):
    return Build_read_pkt(salve_id, READ_INPUT_REGISTERS, start_addr, num_reg)


def Write_reg_1_single(salve_id, start_addr, output_value):
    pdu = struct.pack(">BBHH", salve_id, WRITE_SINGLE_COIL, start_addr, output_value)
    crc = struct.pack(">H", calculate_crc(pdu))
    return pdu + crc

def Write_reg_1_multiple(salve_id, start_addr, wr_val, output_value ):
    byte_count = len(output_value) // 8
    if (len(output_value) % 8) > 0:
        byte_count += 1
    pdu = struct.pack(">BBHHB", salve_id, WRITE_MULTIPLE_COILS, start_addr, len(output_value), byte_count)
    i, byte_value = 0, 0
    for j in output_value:
        if j > 0:
            byte_value += pow(2, i)
        if i == 7:
            pdu += struct.pack(">B", byte_value)
            i, byte_value = 0, 0
        else:
            i += 1
    if i > 0:
        pdu += struct.pack(">B", byte_value)

    crc = struct.pack(">H", calculate_crc(pdu))
    return pdu + crc

def Write_reg_4_single(salve_id, start_addr, output_value):
    pdu = struct.pack(">BBHH", salve_id, WRITE_SINGLE_REGISTER, start_addr, output_value)
    crc = struct.pack(">H", calculate_crc(pdu))
    return pdu + crc

def Write_reg_4_multiple(salve_id, start_addr, output_value):
    byte_count = 2 * len(output_value)
    pdu = struct.pack(">BBHHB", salve_id, WRITE_MULTIPLE_REGISTERS, start_addr, byte_count // 2, byte_count)
    
    for j in output_value:
        fmt = "H" if j >= 0 else "h"
        pdu += struct.pack(">" + fmt, j)

    crc = struct.pack(">H", calculate_crc(pdu))
    return pdu + crc

############################################################
#应答报文处理
############################################################

def read_coils(pdu, crc):
    pass

def read_discrete_inputs(pdu, crc):
    pass

def read_input_registers(pdu, crc):
    byte_num = pdu[0]
    pdu = pdu[1:]
    read_crc = struct.unpack(">H", pdu[byte_num:byte_num + 2])[0]
    if crc != read_crc:
        raise CRC_ERR
    datas = ()
    count = int(byte_num / 2)
    for i in range(count):
        data = struct.unpack('>H',pdu[i*2: i*2 + 2])
        datas += data

    return datas


def read_holding_registers(pdu, crc):
    pass

def write_single_coil(pdu, crc):
    pass

def write_single_register(pdu, crc):
    pass

def write_multiple_coils(pdu, crc):
    pass

def write_multiple_registers(pdu, crc):
    pass

fn_code_map = {
            READ_COILS: read_coils,
            READ_DISCRETE_INPUTS: read_discrete_inputs,
            READ_INPUT_REGISTERS: read_input_registers,
            READ_HOLDING_REGISTERS: read_holding_registers,
            WRITE_SINGLE_COIL: write_single_coil,
            WRITE_SINGLE_REGISTER: write_single_register,
            WRITE_MULTIPLE_COILS: write_multiple_coils,
            WRITE_MULTIPLE_REGISTERS: write_multiple_registers,
        }


#返回值：错误代码，存放结果的数组
def decode_modbus_response(rsp, match_id):
    (addr, fun_code) = struct.unpack('BB', rsp[0:2])
    if match_id != addr:
        raise SALVE_ID_ERR

    if fun_code not in fn_code_map:
        raise ILLEGAL_FUNCTION

    rsp_data = rsp[2:]
    cal_crc = calculate_crc(rsp[:-2])
    ret = fn_code_map[fun_code](rsp_data, cal_crc)
    return ret
