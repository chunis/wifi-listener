import cmds
from middleware import assemble, write_then_read
from utils import *
import time


# RC (return code)
class RC:
    OK = 0x00
    UNKNOWN = 0x01       # Command unknown
    NOTINIT = 0x03       # Command not initialized
    INVALID = 0x04       # Command parameters invalid
    BUSY = 0x05          # Command cannot be executed now
    FAIL = 0x06          # Command execution failed
    BADCRC = 0x08        # Crc check failed
    BADSIZE = 0x0A       # Size check failed
    FRAMEERROR = 0x0F    # SPI checksum/crc error
    NOTIME = 0x10        # Lose time sync

# event type
class EVENT:
    WIFI = 0x0B
    GNSS = 0x0C
    NOEVENT = 0xFF


def get_version_help():
    print("modem_get_version (no argument)")

def get_event_help():
    print("modem_get_event <data size>")

def get_event_size_help():
    print("modem_get_event_size (no argument)")

def wifi_scan_help():
    pass

def modem_get_version(radio, cmd_val, args):
    data = write_then_read(radio, cmd_val, args)
    if data == None: return
    data = data[1:-1]  # strip RC and CRC
    print('bootloader version: 0x%02x%02x%02x%02x' %(data[0], data[1], data[2], data[3]))
    print('functionality:', data[4])
    print('firmware version: 0x%02x%02x%02x' %(data[5], data[6], data[7]))
    print("lorawan version: 0x%02x%02x" %(data[8], data[9]))


def modem_get_event_size(radio, cmd_val, args):
    data = write_then_read(radio, cmd_val, args)
    if data == None: return
    data = data[1:-1]  # strip RC and CRC
    length = data[0] << 8 | data[1]
    print('event size: %d' %length)
    return length


def modem_get_event(radio, cmd_val, args, ret_len=None):
    data_size = ret_len
    if data_size == None:
        data_size = extract_int_from_str(args[0])
        if data_size == None:
            print("size error!")
            return None

    print("modem_get_event: size = %s" %data_size)
    ret_data = write_then_read(radio, cmd_val, [], ret_len=data_size)
    status = ret_data[0]
    evt_type = ret_data[1]
    miss_event = ret_data[2]
    data = ret_data[3:-1]

    if status != RC.OK:
        print("RC(%s) is not OK, command fails" %status)
        return None

    #print("\n----> Event happened (%s such event missed): %s" %(miss_event, evt_type))
    #print("Return value (%s bytes): %s" %(len(data), [hex(x) for x in data]))
    if evt_type == EVENT.WIFI:
        print("Wi-Fi scan done")
    elif evt_type == EVENT.NOEVENT:
        print("no event")
    else:
        print("event (%s) happened" %evt_type)

    return evt_type


def wifi_passive_scan(radio, cmd_val, args):
    wifi_args = [0x01, 0x04, 0x21, 0x01, 0x0A, 0x08, 0x00, 0x80, 0x01, 0x04]

    ret_data = write_then_read(radio, cmd_val, wifi_args)
    status = ret_data[0]
    if status != RC.OK:
        print('command failed')
    else:
        print('command run. wait for wifi event...')
