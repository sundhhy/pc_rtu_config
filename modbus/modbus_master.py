'''
这个文件提供modbus报文的组包和报分的解析功能。


'''

import struct
from rtu_conf.modbus_utils import *
from rtu_conf.modbus_define import *



def Build_read_pkt(slave_addr, function_code, start_addr, num_reg):

    pdu = struct.pack(">BBHH",slave_addr, function_code, start_addr, num_reg)
    crc = struct.pack(">H", calculate_crc(pdu))
    return pdu + crc





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