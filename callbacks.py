import cmds
from middleware import assemble, write_then_read
from utils import *
import time

def get_version_help():
    print("modem_get_version (no argument)")

def modem_get_version(radio, cmd_val, args):
    data = write_then_read(radio, cmd_val, args)
    if data == None: return
    data = data[1:-1]  # strip RC and CRC
    print('bootloader version: 0x%02x%02x%02x%02x' %(data[0], data[1], data[2], data[3]))
    print('functionality:', data[4])
    print('firmware version: 0x%02x%02x%02x' %(data[5], data[6], data[7]))
    print("lorawan version: 0x%02x%02x" %(data[8], data[9]))
