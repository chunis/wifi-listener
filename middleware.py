#!/usr/bin/python

# Chunis Deng (chunchengfh@gmail.com)


from utils import bytes2hexstr
from interface import *


# index to each of the CMD list
cmds_idx_ids = 0   # [id, cmd]
cmds_idx_len = 1   # cmd_nbytes
cmds_idx_rtn = 2   # return_nbytes
cmds_idx_func = 3  # command callback function
cmds_idx_help = 4  # command help function


def assemble(cmd, data):
    require_len = cmd[cmds_idx_len]
    if len(data) == require_len:
        return cmd[0] + data

    print("Error: number of arguments is wrong")
    print("valid value = %s, got %s" %(require_len, len(data)))
    return None


def write_then_read(radio, cmd, data=[], ret_len=None, print_flag=False):
    full_data = assemble(cmd, data)
    if not full_data:
        print("command does not run")
        return None

    read_data_len = cmd[cmds_idx_rtn]
    if ret_len:
        read_data_len = ret_len

    ret_data = write_read_cmd(radio, full_data, read_data_len, print_flag)
    status = ret_data[0]
    crc = ret_data[-1]
    result = ret_data[1:-1]
    if status != 0:
        print("Error! return value wrong (status = 0x%x)" %status)

    if result and print_flag:
        print("Result:", bytes2hexstr(result))

    return ret_data
