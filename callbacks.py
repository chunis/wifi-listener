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
    print("wifi_passive_scan wifi_type chan_mask acq_mode nb_max_result nb_scan_per_channel timeout abort_on_timeout")
    print("wifi_type: b | g | n | a")
    print("acq_mode: beacon | beacon+packet")
    print("abort_on_timeout: true | false")
    print("for example: wifi_passive_scan b 0x421 beacon 10 8 0x0080 true")
    print("         or: wifi_passive_scan b 0x421 beacon+packet 16 8 0x0080 false")


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
        # wifi result format is basic (9 bytes): wifi_type, channelInfo, RSSI, MAC6..MAC1
        wifi_data = bytearray()  # save for geolocation solving
        wifi_data.append(0x01)  # 0x00: MAC only; 0x01: MAC+RSSI
        for n in range(0, len(data), 9):
            rssi = to_sign_value(data[n+2])
            print('rssi: %s, MAC: %s' %(rssi, bytes2hexstr(data[n+3:n+9])))

            wifi_data.append(data[n+2])
            for x in data[n+3:n+9]:
                wifi_data.append(x)
        print('wifi_data:', wifi_data.hex().upper())

    elif evt_type == EVENT.NOEVENT:
        print("no event")
    else:
        print("event (%s) happened" %evt_type)

    return evt_type


def wifi_passive_scan(radio, cmd_val, args):
    if len(args) != 7:
        print("number of arguments wrong, should be 7")
        print("for example: wifi_passive_scan b 0x421 beacon 10 8 0x0080 true")
        return

    wifi_args = []  # collect converted bytes

    wifi_type = args[0]
    chan_mask = args[1]
    acq_mode = args[2]
    nb_max_res = args[3]
    nb_scan_per_ch = args[4]
    timeout = args[5]
    abort_on_tm = args[6]

    wifi_supported_types = ['b', 'g', 'n', 'a']  # a = 'all' = bgn
    if wifi_type in wifi_supported_types:
        wifi_args.append(wifi_supported_types.index(wifi_type) + 1)
    else:
        print("wifi_type error, valid value: b, g, n, a")
        return

    chan_mask = extract_int_from_str(chan_mask)
    wifi_args.extend([(chan_mask >> 8) & 0xFF, chan_mask & 0xFF])

    valid_acq_modes = ['beacon', 'beacon+packet']
    if acq_mode in valid_acq_modes:
        wifi_args.append(1 << valid_acq_modes.index(acq_mode))
    else:
        print("acq_mode error, valid value: beacon, beacon+packet")
        return

    # Note: ignore error check here to simplify code
    wifi_args.append(extract_int_from_str(nb_max_res))
    wifi_args.append(extract_int_from_str(nb_scan_per_ch))
    timeout = extract_int_from_str(timeout)
    wifi_args.extend([(timeout >> 8) & 0xFF, timeout & 0xFF])

    if abort_on_tm == 'true':
        wifi_args.append(1)
    else:
        wifi_args.append(0)

    # acq_mode = 'beacon' or 'beacon+packet', and result_format = 'basic'
    wifi_args.append(0x4)

    print("wifi_args:", bytes2hexstr(wifi_args))

    ret_data = write_then_read(radio, cmd_val, wifi_args)
    status = ret_data[0]
    if status != RC.OK:
        print('command failed')
        return

    print('command run. wait for wifi event...')
    while True:
        time.sleep(1.6)
        length = modem_get_event_size(radio, cmds.CMD_MODEM_GET_EVENT_SIZE, [])
        if length:
            evt_type = modem_get_event(radio, cmds.CMD_MODEM_GET_EVENT, [], length)
            if evt_type == EVENT.WIFI:
                print("wifi result printed.")
                return
