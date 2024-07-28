#!/usr/bin/python

# Chunis Deng (chunchengfh@gmail.com)


import time
from machine import SoftSPI
from utils import *

import sys
if sys.platform == 'pyboard':
    from pyb import Pin
elif sys.platform == 'esp32':
    from machine import Pin


class SPILink:
    def __init__(self):
        if sys.platform == 'pyboard':
            self.nss   = Pin(Pin.board.PA8, Pin.OUT, value=1)
            self.reset = Pin(Pin.board.PA0, Pin.OUT, value=1)
            self.irq   = Pin(Pin.board.PB4, Pin.IN)
            self.busy  = Pin(Pin.board.PB3, Pin.IN)
            self.spi   = SoftSPI(baudrate=1000000, polarity=0, phase=0, bits=8,
                          sck=Pin.board.PA5, mosi=Pin.board.PA7, miso=Pin.board.PA6)
        elif sys.platform == 'esp32':
            self.nss   = Pin(8, Pin.OUT, value=1)
            self.reset = Pin(12, Pin.OUT, value=1)
            self.irq   = Pin(14, Pin.IN)
            self.busy  = Pin(13, Pin.IN)
            self.spi   = SoftSPI(baudrate=1000000, polarity=0, phase=0, bits=8,
                          sck=Pin(9), mosi=Pin(10), miso=Pin(11))


    def send_packet(self, data, ret_size):
        self.wait_busy(0)
        self.nss.value(0)

        self.spi.write(bytearray(data))

        self.nss.value(1)
        self.wait_busy(1)
        self.nss.value(0)

        buf = bytearray(ret_size)
        self.spi.readinto(buf, 0)
        self.nss.value(1)
        return buf

    def wait_busy(self, status):
        while self.busy.value() != status:
            time.sleep(0.001)

    def wakeup(self):
        self.nss.value(0)
        self.nss.value(1)

    def close(self):
        self.spi.deinit()


def write_read_cmd(radio, data, ret_size, print_flag=True):
    radio.wakeup()
    data_to_send = data + [crc(data)]
    data_read = radio.send_packet(data_to_send, ret_size+2)  # the extra 2 bytes: [0] = RC, [-1] = CRC
    if print_flag:
        print("==>:", bytes2hexstr(data_to_send))
        print("<==:", bytes2hexstr(data_read))
    return data_read
