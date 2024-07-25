from callbacks import *

# -1 means result size needs to be provided dynamically
CMD_MODEM_GET_EVENT       = [[0x06, 0x00], 0, -1, modem_get_event, get_event_help]
CMD_MODEM_GET_EVENT_SIZE  = [[0x06, 0x33], 0, 2, modem_get_event_size, get_event_size_help]

CMD_MODEM_GET_VERSION = [[0x06, 0x01], 0, 12, modem_get_version, get_version_help]
CMD_WIFI_PASSIVE_SCAN = [[0x03, 0x30], 10,  0, wifi_passive_scan, wifi_scan_help]
