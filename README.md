# Wi-Fi Listener

`wifi_listener` is a small MicroPython tool basing on **LoRa Basics™ Modem-E
API Reference Manual**. It only implements the wifi passive scan function.
It currently runs on either STM32L476 or esp32 but can be easily ported to
other MicroPython platforms.

## Usage

First flash the latest micropython firmware to STM32L476 and import all of
the 6 Python scripts. Then call `wifi_listener.py` by import it from the REPL
interface. An example output shows as below:
```shell
>>> import wifi_listener

Welcome to use Wi-Fi Listener based on Modem-E v1.x
Input 'help' for help.

>> help
arguments are seperated by whitespace.

Available commands are:
modem_get_event
modem_get_event_size
modem_get_version
wifi_passive_scan

>> wifi_passive_scan
number of arguments wrong, should be 7
for example: wifi_passive_scan b 0x421 beacon 10 8 0x0080 true
>> wifi_passive_scan -h
wifi_passive_scan wifi_type chan_mask acq_mode nb_max_result nb_scan_per_channel timeout abort_on_timeout
wifi_type: b | g | n | a
acq_mode: beacon | beacon+packet
abort_on_timeout: true | false
for example: wifi_passive_scan b 0x421 beacon 10 8 0x0080 true
         or: wifi_passive_scan b 0x421 beacon+packet 16 8 0x0080 false
>> wifi_passive_scan b 0x421 beacon 10 8 0x0080 true
wifi_args: 0x01 0x04 0x21 0x01 0x0A 0x08 0x00 0x80 0x01 0x04
command run. wait for wifi event...
event size: 38
modem_get_event: size = 38
Wi-Fi scan done
rssi: -91, MAC: 0x4C 0x50 0x77 0x50 0x57 0x20
rssi: -78, MAC: 0x00 0xD4 0xF6 0x71 0xFC 0xFC
rssi: -78, MAC: 0x68 0xDD 0xB7 0xA1 0xFC 0x94
rssi: -83, MAC: 0xCC 0xBB 0xFE 0xDA 0xED 0x44
wifi_data: 01A54C5077505720B200D4F671FCFCB268DDB7A1FC94ADCCBBFEDAED44
wifi result printed.
>>
```

This project is specific developed for my book 《IoT全栈剖析》.
